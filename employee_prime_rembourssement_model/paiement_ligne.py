# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError

class paiement_ligne(models.Model):
    _name = "hr.paiement.ligne"
    _description = "Paiement Ligne"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    period_id = fields.Many2one("account.month.period", string = "Période")
    #prime_id = fields.Many2one("hr.prime", string = "Prime")
    prime_id = fields.Many2one("hr.prime", string = "Prime", ondelete="cascade")
    currency_id = fields.Many2one("res.currency", string = "Symbole Monétaire")
    montant_a_payer = fields.Monetary("Échéance", currency_field = "currency_id")
    state  = fields.Selection([
        ("paye","Payé"),
        ("non_paye","Non Payé"),
        ("annule","Annulé"),
        ],"Status", 
        default="non_paye",
    )

    def calculer_prime_montant_reste(self):
        if self.state == "non_paye":
            # self.state = "paye"
            self.prime_id.montant_paye = self.prime_id.montant_paye + self.montant_a_payer
            self.prime_id.reste_a_paye = self.prime_id.montant_total_prime - self.prime_id.montant_paye
        else : 
            # self.state = "non_paye"
            self.prime_id.montant_paye = self.prime_id.montant_paye - self.montant_a_payer
            self.prime_id.reste_a_paye = self.prime_id.montant_total_prime + self.prime_id.montant_paye

    def to_annuler(self):
        self.state = "annule"

    @api.model
    def create(self, vals):
        return super(paiement_ligne, self).create(vals)

    def write(self, vals):
        if vals.get("state"):
            if self.prime_id and vals["state"] == "paye":
                self.prime_id.montant_paye = self.prime_id.montant_paye + self.montant_a_payer
                self.prime_id.reste_a_paye = self.prime_id.montant_total_prime - self.prime_id.montant_paye
            elif self.prime_id and vals["state"] == "non_paye": 
                self.prime_id.montant_paye = self.prime_id.montant_paye - self.montant_a_payer
                self.prime_id.reste_a_paye = self.prime_id.montant_total_prime + self.prime_id.montant_paye
        return super(paiement_ligne, self).write(vals)