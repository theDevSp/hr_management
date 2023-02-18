# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError

class paiementPrime(models.Model):
    _name = "hr.paiement.prime"
    _description = "Paiement Prime"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    period_id = fields.Many2one("account.month.period", string = "Période")
    prime_id = fields.Many2one("hr.prime", string = "Prime")
    currency_id = fields.Many2one("res.currency", string = "Symbole Monétaire")
    montant_a_payer = fields.Monetary("Échéance", currency_field = "currency_id")
    state  = fields.Selection([
        ("paye","Payé"),
        ("non_paye","Non Payé"),
        ("annule","Annulé"),
        ],"Status", 
        default="non_paye",
    )

    def changer_status(self):
        if self.state == "non_paye":
            self.state = "paye"
            self.prime_id.montant_paye = self.prime_id.montant_paye + self.montant_a_payer
            self.prime_id.reste_a_paye = self.prime_id.montant_total_prime - self.prime_id.montant_paye
        else : 
            self.state = "non_paye"
            self.prime_id.montant_paye = self.prime_id.montant_paye - self.montant_a_payer
            self.prime_id.reste_a_paye = self.prime_id.montant_total_prime + self.prime_id.montant_paye

    def to_annuler(self):
        self.state = "annule"