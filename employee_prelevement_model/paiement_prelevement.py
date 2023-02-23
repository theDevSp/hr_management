# -*- coding: utf-8 -*-

from odoo import fields, models, api

class paiement_prelevement(models.Model):
    _name = "hr.paiement.prelevement"
    _description = "Paiement Prelevement"
    _inherit = ["hr.paiement.ligne"]

    prelevement_id = fields.Many2one("hr.prelevement", string = "Prélèvement", ondelete="cascade")

    @api.model
    def create(self, vals):
        if vals.get("prelevement_id") and vals["prelevement_id"]:
            print("prelevement id")
            return super(paiement_prelevement, self).create(vals)
        elif self.prelevement_id:
            return super(paiement_prelevement, self).create(vals)


    def write(self, vals):
        if vals.get("state"):
            if self.prelevement_id and vals["state"] == "paye":
                self.prelevement_id.montant_paye = self.prelevement_id.montant_paye + self.montant_a_payer
                self.prelevement_id.reste_a_paye = self.prelevement_id.montant_total_prime - self.prime_id.montant_paye
            elif self.prelevement_id and vals["state"] == "non_paye": 
                self.prelevement_id.montant_paye = self.prelevement_id.montant_paye - self.montant_a_payer
                self.prelevement_id.reste_a_paye = self.prelevement_id.montant_total_prime + self.prime_id.montant_paye
        return super(paiement_prelevement, self).write(vals)
    
    def calculer_prelevement_montant_reste(self):
        if self.state == "non_paye":
            # self.state = "paye"
            self.prelevement_id.montant_paye = self.prelevement_id.montant_paye + self.montant_a_payer
            self.prelevement_id.reste_a_paye = self.prelevement_id.montant_total_prime - self.prime_id.montant_paye
        else : 
            # self.state = "non_paye"
            self.prelevement_id.montant_paye = self.prelevement_id.montant_paye - self.montant_a_payer
            self.prelevement_id.reste_a_paye = self.prelevement_id.montant_total_prime + self.prime_id.montant_paye
