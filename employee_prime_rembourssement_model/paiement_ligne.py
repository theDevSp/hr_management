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
        ("reportee","Reporté"),
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
        count_lines = len(self.prime_id.paiement_prime_ids)
        if self == self.prime_id.paiement_prime_ids[count_lines-1]:
            self.reporter_date(observations)
        else:
            somme = 0
            nv_tableau = []
            period_ids_lignes = []
            self.state = "reportee"
            self.observations = observations

            for ligne in self.prime_id.paiement_prime_ids:
                if ligne.id > self.id:
                    period_ids_lignes.append(ligne.period_id.id)
                    if ligne.state !="non_paye":
                        nv_tableau.append(
                            {
                                "period_id" : ligne.period_id.id,
                                "prime_id" : ligne.prime_id.id,
                                "montant_a_payer" : ligne.montant_a_payer,
                                "state": ligne.state,
                                "observations": ligne.observations,
                            }
                        )
                    elif ligne.state == "non_paye":
                        somme = somme + ligne.montant_a_payer
            res = somme / self.prime_id.echeance
            nbr_periodes = ceil(res)
            print(period_ids_lignes)
            self.recompute_alimenter_paiement(nbr_periodes,somme,nv_tableau,period_ids_lignes)


    def recompute_alimenter_paiement(self,nbr_periodes,somme,nv_tableau,period_ids_lignes):
        for rec in self:
            chaine = ""
            for id in period_ids_lignes:
                chaine += str(id) +","
            chaine = chaine[:-1]
            query = """
                    SELECT id from account_month_period
                    WHERE id > '%s'
                    AND id NOT IN (%s)
                    LIMIT %s
                """  % (rec.period_id.id, chaine ,nbr_periodes)
            print(query)
            rec.env.cr.execute(query)
            res = rec.env.cr.fetchall()
            paiement_lines=[]
            reste = 0
            for id in res:
                var = somme - reste
                paiement_lines.append(
                    {
                        "period_id" : id[0],
                        "prime_id" : rec.prime_id.id,
                        "montant_a_payer" : rec.prime_id.echeance if (var >= rec.prime_id.echeance) else var,
                        "state": "non_paye",
                    }
                )
                reste += rec.prime_id.echeance
                print(paiement_lines)

            nv_tableau.append(paiement_lines)

            # for ligne in self.prime_id.paiement_prime_ids:
            #         ligne.unlink()
       
       
            self.recreate_paiement(nv_tableau)


    def recreate_paiement(self,paiement_lines):
        for rec in paiement_lines:
            self.env["hr.paiement.ligne"].create(rec)


    def open_wizard_reporte_dates(self):
        view = self.env.ref('hr_management.wizard_reporter_dates_form')
        return {
            'name': ("Reporter le paiement de : \"" + self.prime_id.type_prime.name + "  " + str(self.period_id.code) + "\""),
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


    
    def reporter_date(self,observations):
        print("reporterdate")
        print(observations)

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

        echeance_reportee = self.montant_a_payer
        self.prime_id.paiement_prime_ids[nbr_lignes-1].montant_a_payer = echeance_reportee
        self.state="reportee"
    
        nouvelle_ligne_qui_est_reportee =  {
            "period_id" : nouvelle_periode,
            "prime_id" : self.prime_id.id,
            "montant_a_payer" : last_echeance,
            "state": "non_paye"
        }
        self.env["hr.paiement.ligne"].create(nouvelle_ligne_qui_est_reportee)
        self.observations = observations
        #self.montant_a_payer = self.prime_id.paiement_prime_ids[0].montant_a_payer

    def annuler_reporter_date(self):
        nbr_lignes = len(self.prime_id.paiement_prime_ids)
        last_echeance = self.prime_id.paiement_prime_ids[nbr_lignes-1].montant_a_payer
        self.prime_id.paiement_prime_ids[nbr_lignes-1].unlink()
        nbr_lignes_final = len(self.prime_id.paiement_prime_ids)
        self.prime_id.paiement_prime_ids[nbr_lignes_final-1].montant_a_payer = last_echeance
        self.state = "non_paye"
        # if self.montant_a_payer == last_echeance:
        #     self.montant_a_payer = self.prime_id.paiement_prime_ids[0].montant_a_payer