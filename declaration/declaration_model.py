from odoo import fields, models, api, SUPERUSER_ID
from odoo.osv import expression
from odoo.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta
from lxml import etree
from odoo.exceptions import UserError
import re

class declaration_anomalie_employee_sur_chantier(models.Model):
    _name = 'declaration.anomalie.employee.sur.chantier'
    _description = 'Ce Module à pour but de gérer les déclaration ab,stc ... sur chantier'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_chantier_domain(self):
        pointeur = self.env['res.users'].has_group("hr_management.group_pointeur")
        
        res = []
        if pointeur :
            for user_chantier in self.env.user.chantier_responsable_ids:
                res.append(user_chantier.id)
        else:
            for chantier in self.env['fleet.vehicle.chantier'].search([('type_chantier','in',('Chantier','Depot','Poste'))]):
                res.append(chantier.id)
        
        return [('id', 'in',res)] 
    
    name = fields.Char('name')
    chantier_id = fields.Many2one('fleet.vehicle.chantier', string='Chantier',domain=_get_chantier_domain,required=True)
    employee_id = fields.Many2one('hr.employee', string='Employé',required=True)
    type_declaration = fields.Selection([
            ('5',u"Absence Non Autorisée"),
            ('6',u"Abondement de Poste"),
            ('7',u"STC"),
            ('8',u'Accident du Travail')
    ], string='Type Déclaration',required=True)
    date_fait = fields.Date("Date effective",required=True)
    motif = fields.Text('Motif',required=True)
    state = fields.Selection([
        ('draft', 'Brouillion'),
        ('valide', 'Validée'),
        ('cancel','Annulée'),
        ('approuved','Approuvée')
    ], string='Status',default='draft')

    _prefix_dict = {'5':'AB','6':'AP','7':'STC','8':'AT'}

    @api.model
    def create(self, vals):
        if self.env['account.month.period'].is_sunday(vals['date_fait']) and vals['type_declaration'] in ('5','6'):
            raise ValidationError(
                "Mauvais choix de Jour !!! Vous ne pouvez pas déclarer un %s le dimanche."%(dict(self.fields_get(allfields=['type_declaration'])['type_declaration']['selection'])[vals['type_declaration']])
                )
        query = """
            SELECT COUNT(*)
            FROM declaration_anomalie_employee_sur_chantier
            WHERE type_declaration = '%s' ;
        """ % (vals['type_declaration'])
        self.env.cr.execute(query)
        res = "{:05d}".format(self.env.cr.dictfetchall()[0]['count']+ 1 ) 
        
        vals['name'] = self._prefix_dict[vals['type_declaration']]+str(res)


        return super().create(vals)

    def write(self, vals):
        res= super().write(vals)
        if 'state' in vals and res:
            
            if self.create_uid.id == self.env.user.id and self._uid != SUPERUSER_ID and not self.env.user._is_admin() and vals['state'] not in ('draft','cancel','valide'):
                raise UserError("Action Non autorisé")
            if vals['state'] in ('draft','cancel'):
                self.update_corresponding_lines('1',self.type_declaration)
            elif vals['state'] == 'valide':
                self.update_corresponding_lines(self.type_declaration,'1')
        return res
    
    def update_corresponding_lines(self,day_type,type_condition):
        lines = self.env['hr.rapport.pointage.line'].search([
                ('employee_id','=',self.employee_id.id),
                ('day','=',self.date_fait),
                ('day_type','=',type_condition)
                ])
        
        if lines:
            new_state = 'working' if type_condition == '1' else 'draft'
            for line in lines:
                line.write({
                    'day_type': day_type,
                    'details' : self.motif if type_condition == '1' else False,
                    'chantier_id': line.rapport_id.chantier_id.id if type_condition == '1' else False,
                    'state':new_state
                })
        return

    def action_validation(self):
        self.write({'state': 'valide'})
    
    
    def action_draft(self):
        self.write({'state': 'draft'})
    
    
    def action_cancel(self):
        self.write({'state': 'cancel'})
    
    
    def action_done(self):
        self.write({'state': 'approuved'})