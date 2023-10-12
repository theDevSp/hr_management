from odoo import fields, models, api, SUPERUSER_ID
from odoo.osv import expression
from datetime import date
from dateutil.relativedelta import relativedelta
from lxml import etree
from odoo.exceptions import UserError
import re

class hr_employee_transfert(models.Model):

    _name="hr.employee.transfert"
    _description = "Transfert Personnel Entre Chantiers"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    READONLY_STATES_RL = {
        'valide': [('readonly', True)],
        'cancel': [('readonly', True)],
        'done': [('readonly', True)]
    }
    READONLY_STATES_ARR = {
        'cancel': [('readonly', True)],
        'done': [('readonly', True)]
    }

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

    def _get_engin_domain(self):
        
        res = []

        query = """
                select distinct(vehicle_id) from fleet_vehicle_chantier_affectation fvca inner join fleet_vehicle fv on fv.id = fvca.vehicle_id where fv.active = true;
            """  
        self.env.cr.execute(query)
        for result in self.env.cr.fetchall():
            res.append(result[0])
                
        return [('id', 'in',res)]

    def get_employee_domain(self):
        pointeur = self.env['res.users'].has_group("hr_management.group_pointeur")

        res =  []
        query = ""

        if pointeur:
            query = """
                    select distinct(id) from hr_employee where chantier_id in (select chantier_id from chantier_responsable_relation where user_id = %s);
                """   % (self.env.user.id)
        else:
            query = """
                    select distinct(id) from hr_employee where chantier_id in (select id from fleet_vehicle_chantier where type_chantier not in ('Chantier','Depot','Poste'));
                """ 

        self.env.cr.execute(query)
        for employee_id in self.env.cr.fetchall():
            res.append(employee_id[0])
                
        return [('id', 'in',res)]  


    name = fields.Char('Réference',readonly=True)
    employee_id = fields.Many2one("hr.employee",u"Employée",required=True, states=READONLY_STATES_RL)
    type_emp = fields.Selection(related="employee_id.contract_id.type_emp",string=u"Type d'employé", required=False, store=True)

    chantier_id_source = fields.Many2one("fleet.vehicle.chantier",u"Chantier Source", states=READONLY_STATES_RL,domain=_get_chantier_domain,required=True)
    vehicle_id_source = fields.Many2one("fleet.vehicle",u"Code engin Source", states=READONLY_STATES_RL)
    emplacement_chantier_id_source = fields.Many2one("fleet.vehicle.chantier.emplacement","Emplacement Source", states=READONLY_STATES_RL)

    chantier_id_destiation = fields.Many2one("fleet.vehicle.chantier",u"Chantier Destination", states=READONLY_STATES_RL,required=True)
    vehicle_id_destiation = fields.Many2one("fleet.vehicle",u"Code engin Destination", states=READONLY_STATES_RL)
    emplacement_chantier_id_destiation = fields.Many2one("fleet.vehicle.chantier.emplacement","Emplacement Destination", states=READONLY_STATES_RL)

    state = fields.Selection([('draft',u'Nouveau Tranfert'),('valide',u"Validé"),('done',u"Arrivée"),('cancel',u"Annulé")],u"Etat Transfert",default='draft',readonly=True)

    date_transfert = fields.Date('Date Transfert', states=READONLY_STATES_RL,required=True) 
    date_arriver = fields.Date('Date Arrivée', states=READONLY_STATES_ARR) 
    rapport_id = fields.Many2one("hr.rapport.pointage", string = "Rapport de pointage")
            

    @api.model
    def create(self,vals):

        vals['name'] = self.env['ir.sequence'].next_by_code('hr.employee.transfert')

        res = super(hr_employee_transfert,self).create(vals)


        return res
    
    
    def write(self,vals):
        
        res = super().write(vals)
        if not self.date_arriver and not vals.get('date_arriver') and self.state == 'done':
            raise UserError("Veuillez Spécifier la date d'arrivée")
        
        if 'state' in vals and res:
            
            if self.create_uid.id == self.env.user.id and self._uid != SUPERUSER_ID and not self.env.user._is_admin() and vals['state'] == 'done':
                raise UserError("Action Non autorisé")
            if vals['state'] in ('draft','cancel'):
                self.update_corresponding_lines('1','9')
            elif vals['state'] == 'done':
                self.update_corresponding_lines('9','1')

        return res

    def update_corresponding_lines(self,day_type,type_condition):
        date_start = self.env['account.month.period'].get_period_from_date(self.date_transfert).date_start
        lines = self.env['hr.rapport.pointage.line'].sudo().search([
                ('employee_id','=',self.employee_id.id),
                ('day','>=',date_start),
                ('day','<=',self.date_transfert),
                ('day_type','=',type_condition)
                ])

        self.employee_id.sudo().write({
            'vehicle_id':self.vehicle_id_destiation.id if type_condition == '1' else self.vehicle_id_source.id
            })
        self.employee_id.sudo().write({
            'emplacement_chantier_id':self.emplacement_chantier_id_destiation.id if type_condition == '1' else self.emplacement_chantier_id_source.id
            }) 
        self.employee_id.sudo().write({
            'chantier_id':self.chantier_id_destiation.id if type_condition == '1' else self.chantier_id_source.id
            })
        
        if lines:
            lines[len(lines) - 1].write({
                'day_type': day_type,
                'details' : 'Transfert vers %s'%self.chantier_id_destiation.simplified_name if type_condition == '1' else False,
                'chantier_id': self.chantier_id_destiation.id if type_condition == '1' else False
            })
            lines[len(lines) - 1].rapport_id.sudo().write({
                'chantier_id': self.chantier_id_destiation.id if type_condition == '1' else self.chantier_id_source
            })
            new_state = 'working' if type_condition == '1' else 'draft'
            for line in lines[0:len(lines) -1]:
                line.write({
                    'state':new_state
                })
        return

    def is_pointeur(self):
        return self.env['res.users'].has_group("hr_management.group_pointeur")

    def user_company_id(self):
        return self.rapport_id.chantier_id.cofabri

    def open_transfert(self):
        
        form = self.env.ref(
            'nxtm_employee_mngt.hr_employee_transfert_form')

        return {
            'name':'Transferts',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': self._name,
            'views': [(form.id, 'form')],
            'target': 'current',
            'res_id':self.id
            
        }

    
    def action_validation(self):
        self.write({'state': 'valide'})
    
    
    def action_draft(self):
        self.write({'state': 'draft'})
    
    
    def action_cancel(self):
        self.write({'state': 'cancel'})
    
    
    def action_done(self):
        self.write({'state': 'done'})
    
    def open_transfert(self):
        view = self.env.ref('hr_management.hr_employee_transfert_form')
        
        return {
            'name': ("Transferts %s " % self.name),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': self.id,
            'views': [(view.id, 'form')]
        }

