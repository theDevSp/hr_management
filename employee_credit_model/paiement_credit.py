# # -*- coding: utf-8 -*-

# from odoo import fields, models, api

# class paiement_credit(models.Model):
#     _name = "hr.paiement.credit"
#     _description = "Paiement Credit"
#     _inherit = ['mail.thread', 'mail.activity.mixin']

#     period_id = fields.Many2one("account.month.period", string = "Période")
#     credit_id = fields.Many2one("hr.credit", string = "Crédit", ondelete="cascade")
#     currency_id = fields.Many2one("res.currency", string = "Symbole Monétaire")
#     montant_a_payer = fields.Monetary("Échéance", currency_field = "currency_id")
#     state  = fields.Selection([
#         ("paye","Payé"),
#         ("non_paye","Non Payé"),
#         ("annule","Annulé"),
#         ],"Status", 
#         default="non_paye",
#     )       

#     def calculer_credit_montant_reste(self):
#         if self.state == "non_paye":
#             # self.state = "paye"
#             self.credit_id.montant_paye = self.credit_id.montant_paye + self.montant_a_payer
#             self.credit_id.reste_a_paye = self.credit_id.montant_total_prime - self.credit_id.montant_paye
#         else : 
#             # self.state = "non_paye"
#             self.credit_id.montant_paye = self.credit_id.montant_paye - self.montant_a_payer
#             self.credit_id.reste_a_paye = self.credit_id.montant_total_prime + self.credit_id.montant_paye

#     def to_annuler(self):
#         self.state = "annule"

#     @api.model
#     def create(self, vals):
#         return super(paiement_credit, self).create(vals)

#     def write(self, vals):
#         if vals.get("state"):
#             if self.credit_id and vals["state"] == "paye":
#                 self.credit_id.montant_paye = self.credit_id.montant_paye + self.montant_a_payer
#                 self.credit_id.reste_a_paye = self.credit_id.montant_total_prime - self.credit_id.montant_paye
#             elif self.credit_id and vals["state"] == "non_paye": 
#                 self.credit_id.montant_paye = self.credit_id.montant_paye - self.montant_a_payer
#                 self.credit_id.reste_a_paye = self.credit_id.montant_total_prime + self.credit_id.montant_paye
#         return super(paiement_credit, self).write(vals)
    
    