# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import date

class allocations(models.Model):
    _name = "hr.allocations"
    _description = "Allocations"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char("Libellé",default="Allocations")
    employee_id = fields.Many2one("hr.employee",string="Employé",required=True)
    categorie = fields.Selection([
        ('bonus',"Bonus jour Congé"),
        ('conge_annuel',"Congé annuel"),
        ('jour_ferie',"Jour férié"),
        ('dimanche_travaille',"Dimanche travaillé"),
        ('stc',"STC"),
        ('indemnite_conge',"Indemnité de congé"),
        ('compensation',"Compensation de salaire"),
        ('regularisation',"Régularisation"),
        ],"Catégorie", required=True
    )
    nbr_jour = fields.Float("Nombre de jours")
    state = fields.Selection([
        ('draft',"Brouillon"),
        ('approuvee',"Approuvée"),
        ('refusee',"Refusée"),
        ],"Statut",
        default='draft',
        readonly=True
    )
    period_id = fields.Many2one("account.month.period", string = "Période")
    stc_id = fields.Many2one("hr.stc", string = "STC", required=False)


    @api.model
    def create(self, vals):
        return super(allocations, self).create(vals)

    def write(self, vals):
        return super(allocations, self).write(vals)
    
    def to_draft(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie'):
            if self.state not in {'draft'} :
                self.state = 'draft'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )
        
    def to_approuvee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie'):
            if self.state not in {'approuvee'} :
                self.state = 'approuvee'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )

    def to_refusee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie'):
            if self.state not in {'refusee'} :
                self.state = 'refusee'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )

    def get_sum_allocation(self,employee_id,period_actuel_id,period_debut_contrat_id,is_dimanche=False):
        query = """
                SELECT SUM(nbr_jour)
                FROM hr_allocations
                WHERE categorie %s 'dimanche_travaille' 
                AND employee_id = %s AND period_id <= %s and period_id >= %s
                AND state = 'approuvee'
            """ % ('=' if is_dimanche else '!=',employee_id.id,period_actuel_id.id,period_debut_contrat_id.id if period_debut_contrat_id else 7)
        self.env.cr.execute(query)
        return self.env.cr.fetchall()[0][0]
