# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from math import *
from dateutil.relativedelta import relativedelta


class paiement_prelevement(models.Model):
    _name = "hr.paiement.prelevement"
    _description = "Paiement Prelevement"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    period_id = fields.Many2one("account.month.period", string = "Période")
    prelevement_id = fields.Many2one("hr.prelevement", string = "Prélèvement", ondelete="cascade")
    montant_a_payer = fields.Float("Échéance")
    state  = fields.Selection([
        ("paye","Payé"),
        ("non_paye","Non Payé"),
        ("annule","Annulé"),
        ("reportee","Décalé"),
        ],"Status", 
        default="non_paye",
    )       
    observations = fields.Char("Observations")
    stc_id = fields.Many2one("hr.stc", string = "STC", required=False)

    def to_annuler(self):
        self.state = "annule"
    
    def payer(self):
        self.state = "paye"
        
    def unpayer(self):
        self.state = "non_paye"

    @api.model
    def create(self, vals):
        return super(paiement_prelevement, self).create(vals)

    def write(self, vals):
        if vals.get("state"):
            if self.prelevement_id and vals["state"] == "paye":
                self.prelevement_id.montant_paye = self.prelevement_id.montant_paye + self.montant_a_payer
                self.prelevement_id.reste_a_paye = self.prelevement_id.montant_total_prime - self.prelevement_id.montant_paye
            elif self.prelevement_id and vals["state"] == "non_paye" and self.state == "paye": 
                self.prelevement_id.montant_paye = self.prelevement_id.montant_paye - self.montant_a_payer
                self.prelevement_id.reste_a_paye = self.prelevement_id.montant_total_prime + self.prelevement_id.montant_paye
        return super(paiement_prelevement, self).write(vals)
    

    def open_wizard_reporte_dates_prelevement(self):
        view = self.env.ref('hr_management.wizard_reporter_dates_form')
        return {
            'name': ("Décaler le paiement de : \"" + str(self.period_id.code) + "\""),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard_reporter_dates',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context' : {
                'line_id' : self.id,
                'current_model' : "prelevement"
            },
        }

    def open_wizard_details_prelevement(self):
        view = self.env.ref('hr_management.paiement_prelevement_view_form')
        return {
            'name': ("Détails du paiement de : \"" + str(self.period_id.code) + "\""),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.paiement.prelevement',
            'views': [(view.id, 'form')],
            'view_id': view.id, 
            'target': 'target',
            'res_id' : self.id,
        }
    

    def recompute_prelevement(self,observations):
        self.reporter_date_prelevement()
        somme,reste,echeance = 0,0,self.prelevement_id.echeance
        self.state = "reportee"
        self.observations = observations
        for ligne in self.prelevement_id.paiement_prelevement_ids:
            if ligne.id >= self.id and ligne.state == 'non_paye':
                somme += ligne.montant_a_payer
        for ligne in self.prelevement_id.paiement_prelevement_ids:
            if ligne.id >= self.id and ligne.state == 'non_paye':
                var = somme - reste
                ligne.write({
                    'montant_a_payer':echeance if var >= echeance else var
                })
                reste += echeance


    def reporter_date_prelevement(self):
        nbr_lignes = len(self.prelevement_id.paiement_prelevement_ids)
        last_periode = self.prelevement_id.paiement_prelevement_ids[nbr_lignes-1].period_id
        last_echeance = self.prelevement_id.paiement_prelevement_ids[nbr_lignes-1].montant_a_payer
        
        nouvelle_periode_id = self.env['account.month.period'].search_read([('date_start','=',last_periode.date_start + relativedelta(months=+1))],['id'])

        self.prelevement_id.paiement_prelevement_ids[nbr_lignes-1].write({'montant_a_payer' : self.montant_a_payer})

        nouvelle_ligne_qui_est_reportee =  {
            "period_id" : nouvelle_periode_id[0]['id'],
            "prelevement_id" : self.prelevement_id.id,
            "montant_a_payer" : last_echeance,
            "state": "non_paye",
        }
        self.env["hr.paiement.prelevement"].create(nouvelle_ligne_qui_est_reportee)

    def annuler_reporter_date_prelevement(self):
        nbr_lignes = len(self.prelevement_id.paiement_prelevement_ids)
        derniere_ligne = self.prelevement_id.paiement_prelevement_ids[nbr_lignes-1]
        message = ""
        last_period_non_paye = -1

        if derniere_ligne.state == "non_paye":
            message = "Attention! Voulez vous vraiment annuler le décalage du paiement du \"" + str(self.period_id.code) + "\" ? "
            last_line_non_paye = derniere_ligne
        else:
            for ligne in self.prelevement_id.paiement_prelevement_ids:
                if ligne.id > self.id and ligne.state == "non_paye":
                    last_period_non_paye = ligne.period_id.code
                    last_line_non_paye = ligne
            if self == derniere_ligne:
                raise ValidationError("Erreur, Ce paiement est le dernier, vous ne pouvez pas annuler le décalage de cette période.")
            elif last_period_non_paye == -1:
                raise ValidationError("Erreur, Vous ne pouvez pas annuler le décalage du paiement, parceque les paiements qui suivent cette période sont différents du statut \"Non Payé\".")
            else:
                #dict fetch option from value
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
            'name': ("Annuler le décalage du paiement de : \"" + str(self.period_id.code) + "\""),
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
                'current_model' : "prelevement"
            },
        }

    def annuler_reporter_date_apres_confirmation_prelevement(self,last_line_non_paye_objet):
        somme,reste,echeance = 0,0,self.prelevement_id.echeance
        for ligne in self.prelevement_id.paiement_prelevement_ids:
            if ligne.id  > self.id and ligne.state == "non_paye":
                somme += ligne.montant_a_payer
        last_line_non_paye_objet.unlink()
        self.state = "non_paye"
        for ligne in self.prelevement_id.paiement_prelevement_ids:
            if ligne.id >= self.id and ligne.state == "non_paye":
                var = somme - reste
                ligne.write({
                    'montant_a_payer':echeance if var >= echeance else var
                })
                reste += echeance