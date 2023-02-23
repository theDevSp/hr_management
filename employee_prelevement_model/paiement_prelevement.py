# -*- coding: utf-8 -*-

from odoo import fields, models, api

class paiement_prelevement(models.Model):
    _name = "hr.paiement.prelevement"
    _description = "Paiement Prelevement"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    period_id = fields.Many2one("account.month.period", string = "Période")
    #prelevement_id = fields.Many2one("hr.prelevement", string = "Prélèvement")
    prelevement_id = fields.Many2one("hr.prelevement", string = "Prélèvement", ondelete="cascade")
    currency_id = fields.Many2one("res.currency", string = "Symbole Monétaire")
    montant_a_payer = fields.Monetary("Échéance", currency_field = "currency_id")
    state  = fields.Selection([
        ("paye","Payé"),
        ("non_paye","Non Payé"),
        ("annule","Annulé"),
        ],"Status", 
        default="non_paye",
    )       

    def calculer_prelevement_montant_reste(self):
        if self.state == "non_paye":
            # self.state = "paye"
            self.prelevement_id.montant_paye = self.prelevement_id.montant_paye + self.montant_a_payer
            self.prelevement_id.reste_a_paye = self.prelevement_id.montant_total_prime - self.prelevement_id.montant_paye
        else : 
            # self.state = "non_paye"
            self.prelevement_id.montant_paye = self.prelevement_id.montant_paye - self.montant_a_payer
            self.prelevement_id.reste_a_paye = self.prelevement_id.montant_total_prime + self.prelevement_id.montant_paye

    def to_annuler(self):
        self.state = "annule"

    @api.model
    def create(self, vals):
        return super(paiement_prelevement, self).create(vals)

    def write(self, vals):
        if vals.get("state"):
            if self.prelevement_id and vals["state"] == "paye":
                self.prelevement_id.montant_paye = self.prelevement_id.montant_paye + self.montant_a_payer
                self.prelevement_id.reste_a_paye = self.prelevement_id.montant_total_prime - self.prelevement_id.montant_paye
            elif self.prelevement_id and vals["state"] == "non_paye": 
                self.prelevement_id.montant_paye = self.prelevement_id.montant_paye - self.montant_a_payer
                self.prelevement_id.reste_a_paye = self.prelevement_id.montant_total_prime + self.prelevement_id.montant_paye
        return super(paiement_prelevement, self).write(vals)
    
    