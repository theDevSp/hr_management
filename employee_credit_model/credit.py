# # -*- coding: utf-8 -*-

# from odoo import models, fields, api
# from odoo.exceptions import ValidationError
# from math import *

# class credit(models.Model):
#     _name = "hr.credit"
#     _description = "Credit"
#     _inherit = ["hr.prime",'mail.thread', 'mail.activity.mixin']

#     paiement_credit_ids = fields.One2many("hr.paiement.credit","credit_id", string = "Paiement Crédit" )
#     is_credit = fields.Boolean("Crédit?", default = True)
#     type_credit = fields.Selection([
#         ("en_montant","Crédit En Montant"),
#         ("en_jour","Crédit En Jour"),
#         ],"Type de prélèvement",
#     )

#     @api.model
#     def create(self, vals):
#         return super(credit, self).create(vals)
         
#     def write(self, vals):
#         if vals.get("echeance") or vals.get("montant_total_prime"):
#             for ligne in self.paiement_credit_ids:
#                 if ligne.state == "paye":
#                     raise ValidationError("Erreur, vous ne pouvez pas faire ce traitement.")
#         if vals.get("montant_paye") and vals["montant_paye"] > self.montant_total_prime:
#             raise ValidationError("Le montant payé doit être inférieur du montant et strictement supérieur à 0.")
#         if vals.get("state") and vals["state"] == "draft" and self.state == "annulee":
#             for ligne in self.paiement_credit_ids:
#                 ligne.unlink()
#         if vals.get("state") and vals["state"] == "validee":
#             if vals.get("echeance") or vals.get("montant_total_prime"):
#                 for ligne in self.paiement_credit_ids:
#                     ligne.unlink()
#             self.compute_credit()
#         return super(credit, self).write(vals)
    

#     def compute_credit(self):
#         if self.echeance > 0 and self.echeance <= self.montant_total_prime:
#             res = self.montant_total_prime / self.echeance
#             nbr_periodes = ceil(res)            
#             self.compute_alimenter_paiement_credit(nbr_periodes)


#     def compute_alimenter_paiement_credit(self,nbr_periodes):
#         for rec in self:
#             query = """
#                     SELECT id from account_month_period
#                     WHERE id >= '%s'
#                     LIMIT %s;
#                 """  % (rec.first_period_id.id, nbr_periodes)
#             rec.env.cr.execute(query)
#             res = rec.env.cr.fetchall()
#             paiement_lines=[]
#             reste = 0
#             for id in res:
#                 var = rec.montant_total_prime - reste
#                 paiement_lines.append(
#                     {
#                         "period_id" : id[0],
#                         "credit" : rec.id,
#                         "montant_a_payer" : rec.echeance if (var >= rec.echeance) else var,
#                     }
#                 )
#                 reste += rec.echeance
           
#             self.create_paiement_credit(paiement_lines)


#     def create_paiement_credit(self,paiement_lines):
#         for rec in paiement_lines:
#             self.env["hr.paiement.credit"].create(rec)


#     def to_draft(self):
#         if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
#             if self.state not in {'draft','validee'} :
#                 if self.state == "cloture":
#                     for ligne in self.paiement_credit_ids:
#                         if ligne.state == "annule":
#                             ligne.state = "non_paye"
#                 elif self.state == "cloture_paye":
#                     for ligne in self.paiement_credit_ids:
#                         if ligne.state == "paye":
#                             ligne.state = "non_paye"
#                 self.state = 'draft'
#             else:
#                 raise ValidationError("Erreur, Cette action n'est pas autorisée.")
#         else:
#             raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut.")


#     def to_validee(self):
#         if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
#             if self.state not in {'validee','annulee','cloture_paye','cloture'} :
#                 self.state = 'validee'
#             else:
#                 raise ValidationError("Erreur, Cette action n'est pas autorisée.")
#         else:
#             raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut.")


#     def to_annulee(self):
#         if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
#             if self.state not in {'annulee','cloture_paye','cloture'} :
#                 self.state = 'annulee'
#             else:
#                 raise ValidationError("Erreur, Cette action n'est pas autorisée.")
#         else:
#             raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut.")


#     def to_cloturer_payer(self):
#         if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
#             if self.state not in {'draft','annulee','cloture_paye','cloture'} :
#                 if self.state == "validee":
#                     for ligne in self.paiement_credit_ids:
#                         if ligne.state == "non_paye":
#                             ligne.state = "paye"
#                 self.state = 'cloture_paye'
#             else:
#                 raise ValidationError("Erreur, Cette action n'est pas autorisée.")
#         else:
#             raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut.")
    

#     def to_cloturer(self):
#         if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
#             if self.state not in {'draft','annulee','cloture_paye','cloture'} :
#                 if self.state == "validee":
#                     for ligne in self.paiement_credit_ids:
#                         if ligne.state == "non_paye":
#                             ligne.state = "annule"
#                 self.state = 'cloture'
#             else:
#                 raise ValidationError("Erreur, Cette action n'est pas autorisée.")
#         else:
#             raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut.")