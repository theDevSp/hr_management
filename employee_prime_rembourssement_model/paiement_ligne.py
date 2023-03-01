# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from math import *
 
class paiement_ligne(models.Model):
    _name = "hr.paiement.ligne"
    _description = "Paiement Ligne"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    period_id = fields.Many2one("account.month.period", string = "Période")
    prime_id = fields.Many2one("hr.prime", string = "Prime", ondelete="cascade")
    currency_id = fields.Many2one("res.currency", string = "Symbole Monétaire")
    montant_a_payer = fields.Monetary("Échéance", currency_field = "currency_id")
    state  = fields.Selection([
        ("paye","Payé"),
        ("non_paye","Non Payé"),
        ("annule","Annulé"),
        ("reportee","Décalé"),
        ],"Status", 
        default="non_paye",
    )
    observations = fields.Text("Observations")

    def to_annuler(self):
        self.state = "annule"

    @api.model
    def create(self, vals):
        return super(paiement_ligne, self).create(vals)

    def write(self, vals):
        if vals.get("state"):
            if self.prime_id and vals["state"] == "paye" and self.state == "non_paye":
                self.prime_id.montant_paye = self.prime_id.montant_paye + self.montant_a_payer
                self.prime_id.reste_a_paye = self.prime_id.montant_total_prime - self.prime_id.montant_paye
            elif self.prime_id and vals["state"] == "non_paye" and self.state == "paye": 
                self.prime_id.montant_paye = self.prime_id.montant_paye - self.montant_a_payer
                self.prime_id.reste_a_paye = self.prime_id.montant_total_prime + self.prime_id.montant_paye
        return super(paiement_ligne, self).write(vals)
    

    def recompute_prime(self,observations):
        self.reporter_date()
        somme,reste,echeance = 0,0,self.prime_id.echeance
        self.state = "reportee"
        self.observations = observations
        for ligne in self.prime_id.paiement_prime_ids:
            if ligne.id >= self.id and ligne.state == 'non_paye':
                somme += ligne.montant_a_payer
        for ligne in self.prime_id.paiement_prime_ids:
            if ligne.id >= self.id and ligne.state == 'non_paye':
                var = somme - reste
                ligne.write({
                    'montant_a_payer':echeance if var >= echeance else var
                })
                reste += echeance


    def open_wizard_reporte_dates(self):
        view = self.env.ref('hr_management.wizard_reporter_dates_form')
        return {
            'name': ("Décaler le paiement de : \"" + self.prime_id.type_prime.name + "  " + str(self.period_id.code) + "\""),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard_reporter_dates',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context' : {
                'line_id' : self.id,
            },
        }


    def open_wizard_details(self):
        view = self.env.ref('hr_management.paiement_ligne_view_form')
        return {
            'name': ("Détails du paiement : \"" + self.prime_id.type_prime.name + "  " + str(self.period_id.code) + "\""),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.paiement.ligne',
            'views': [(view.id, 'form')],
            'view_id': view.id, 
            'target': 'target',
            'res_id' : self.id,
        }


    def reporter_date(self):
        nbr_lignes = len(self.prime_id.paiement_prime_ids)
        last_periode = self.prime_id.paiement_prime_ids[nbr_lignes-1].period_id.id
        last_echeance = self.prime_id.paiement_prime_ids[nbr_lignes-1].montant_a_payer
        query_nouvelle_periode = """
                SELECT id
                FROM account_month_period
                WHERE id > %s
                LIMIT 1;
            """  % (last_periode)
        self.env.cr.execute(query_nouvelle_periode)
        res_2 = self.env.cr.fetchall()
        nouvelle_periode = res_2[0][0]
        self.prime_id.paiement_prime_ids[nbr_lignes-1].montant_a_payer = self.montant_a_payer
        nouvelle_ligne_qui_est_reportee =  {
            "period_id" : nouvelle_periode,
            "prime_id" : self.prime_id.id,
            "montant_a_payer" : last_echeance,
            "state": "non_paye",
        }
        self.env["hr.paiement.ligne"].create(nouvelle_ligne_qui_est_reportee)

    def annuler_reporter_date(self):
        nbr_lignes = len(self.prime_id.paiement_prime_ids)
        derniere_ligne = self.prime_id.paiement_prime_ids[nbr_lignes-1]
        message = ""
        last_period_non_paye = -1

        if derniere_ligne.state == "non_paye":
            message = "Attention! Voulez vous vraiment annuler de décalage du paiement du \"" + str(self.period_id.code) + "\" ? "
            last_line_non_paye = derniere_ligne
        else:
            for ligne in self.prime_id.paiement_prime_ids:
                if ligne.id > self.id and ligne.state == "non_paye":
                    last_period_non_paye = ligne.period_id.code
                    last_line_non_paye = ligne
            if self == derniere_ligne:
                raise ValidationError("Erreur, Ce paiement est le dernier, vous ne pouvez pas annuler le décalage de cette période.")
            elif last_period_non_paye == -1:
                raise ValidationError("Erreur, Vous ne pouvez pas annuler le décalage du paiement, parceque les paiements qui suivent cette période sont différents du statut \"Non Payé\".")
            else:
                if derniere_ligne.state == "paye":
                    statut = "Payé"
                elif derniere_ligne.state == "non_paye":
                    statut = "Non Payé"
                elif derniere_ligne.state == "annule":
                    statut = "Annulé"
                elif derniere_ligne.state == "reportee":
                    statut = "Décalé"
            message = "Attention! Normalement le paiement du \"" + str(derniere_ligne.period_id.code) + "\" qui doit être supprimé, mais ce paiement est \"" + str(statut) + "\". Donc vous êtes en train de supprimer la dernière ligne \"Non Payé\" qui correspond à la période \"" + str(last_period_non_paye) + "\", voulez-vous continuer?"

        view = self.env.ref('hr_management.wizard_annuler_reporter_date_form')
        return {
            'name': ("Annuler le décalage du paiement de : \"" + self.prime_id.type_prime.name + "  " + str(self.period_id.code) + "\""),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard_confirmer_annuler_reporter_date',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context' : {
                "default_message" : message,
                "current_line": self.id,
                "last_line_non_paye": last_line_non_paye.id,
            },
        }

    def annuler_reporter_date_apres_confirmation(self,last_line_non_paye_objet):
        somme,reste,echeance = 0,0,self.prime_id.echeance
        for ligne in self.prime_id.paiement_prime_ids:
            if ligne.id  > self.id and ligne.state == "non_paye":
                somme += ligne.montant_a_payer
        last_line_non_paye_objet.unlink()
        self.state = "non_paye"
        for ligne in self.prime_id.paiement_prime_ids:
            if ligne.id >= self.id and ligne.state == "non_paye":
                var = somme - reste
                ligne.write({
                    'montant_a_payer':echeance if var >= echeance else var
                })
                reste += echeance