# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

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
    payslip_id = fields.Many2one("hr.payslip", string = "Fiche de Paie", required=False)


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

    def get_sum_allocation(self,employee_id,period_actuel_id,period_debut_contrat_id,is_dimanche=False,is_jf=False):

        allocations_list = self.env['hr.allocations'].search([('employee_id','=',employee_id.id)])

        date_start = period_debut_contrat_id.date_start if period_debut_contrat_id else datetime.strptime('1900-01-01', '%Y-%m-%d').date()
        date_end = period_actuel_id.date_start if period_actuel_id else (datetime.now() + relativedelta(months=+1)).date()

        plus_alloc = sum(line.nbr_jour for line in allocations_list.filtered(
                                        lambda ln: ln.categorie in ('bonus','regularisation') 
                                                and ln.period_id.date_start < date_end
                                                and ln.period_id.date_start >= date_start
                                        ))
        minec_alloc = sum(line.nbr_jour for line in allocations_list.filtered(
                                        lambda ln: ln.categorie not in ('bonus','regularisation','dimanche_travaille','jour_ferie') 
                                                and ln.period_id.date_start < date_end
                                                and ln.period_id.date_start >= date_start
                                        ))
        dimanche_alloc = sum(line.nbr_jour for line in allocations_list.filtered(
                                        lambda ln: ln.categorie in ('dimanche_travaille') 
                                                and ln.period_id.date_start < date_end
                                                and ln.period_id.date_start >= date_start
                                        ))
        jf_alloc = sum(line.nbr_jour for line in allocations_list.filtered(
                                        lambda ln: ln.categorie in ('jour_ferie') 
                                                and ln.period_id.date_start < date_end
                                                and ln.period_id.date_start >= date_start
                                        ))

        
        if is_dimanche and not is_jf:
            return dimanche_alloc
        elif is_jf and not is_dimanche:
            return jf_alloc
        elif not is_dimanche and not is_jf:
            return plus_alloc - minec_alloc
        else:
            return 0
