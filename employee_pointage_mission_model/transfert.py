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
            

    @api.model
    def create(self,vals):

        vals['name'] = self.env['ir.sequence'].next_by_code('hr.employee.transfert')
        """
        period_id = self.env["account.period"].search([('date_stop','>=',fields.Date.from_string(vals['date_transfert']).strftime('%Y-%m-%d')),('date_start','<=',fields.Date.from_string(vals['date_transfert']).strftime('%Y-%m-%d'))])
        rapport = self.env['hr.rapport.pointage'].search([('employee_id','=',vals['employee_id']),('period_id','=',period_id.id)])
        if not rapport:
            rapport = self.env['hr.rapport.pointage'].sudo().create({
                'employee_id':vals['employee_id'],
                'period_id':period_id.id,
                'chantier_id':vals['chantier_id_source']
                })
        vals['rapport_id'] = rapport.id
        """
        res = super(hr_employee_transfert,self).create(vals)


        return res
    
    
    def write(self,vals):

        period_month = fields.Date.from_string(self.date_transfert).month
        period_year = fields.Date.from_string(self.date_transfert).year

        quinzaine1_first_day = str(period_year)+'-'+str(period_month)+'-01'

        query = """
                    select create_uid from hr_employee_transfert where id = %s;
                """   % (self.id)
        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()

        if not self.date_arriver and not vals.get('date_arriver') and self.state == 'valide':
            raise UserError("Veuillez Spécifier la date d'arrivée")
        
        if 'state' in vals and vals.get('state') == 'done':
            
            if res[0]['create_uid'] == self.env.user.id and self._uid != SUPERUSER_ID and not self.env.user._is_admin():
                raise UserError("Action Non autorisé")

            lines = self.env['hr.rapport.pointage.line'].search([('employee_id','=',self.employee_id.id),('day','>=',fields.Date.from_string(quinzaine1_first_day).strftime('%Y-%m-%d')),('day','<=',fields.Date.from_string(self.date_transfert).strftime('%Y-%m-%d'))])
            if lines:
                if self.chantier_id_destiation.digital:
                    for line in lines[0:len(lines) -1]:
                        line.write({
                            'state':'working'
                        })
            # TODO work on
                lines[len(lines) - 1].write({
                    'day_type':'9',
                    'details':'Transfert vers '+self.chantier_id_destiation.simplified_name,
                    'chantier_id':self.chantier_id_destiation.id
                })
                for reports in  self.env['hr.rapport.pointage'].search([('employee_id','=',self.employee_id.id),('period_id','=',lines[len(lines) - 1].rapport_id.period_id.id)]):
                    reports.write({
                        'chantier_id':self.chantier_id_destiation.id
                    })
                self.employee_id.write({
                    'chantier_id':self.chantier_id_destiation.id
                })


        if 'state' in vals and vals.get('state') == 'cancel':

            if self.state not in ('draft','valide') and not self.env['res.users'].has_group("nxtm_employee_mngt.group_pointage_manager"):
                raise UserError(u"Cette action n'est pas autoriser") 

            lines = self.env['hr.rapport.pointage.line'].search([('employee_id','=',self.employee_id.id),('day','>=',fields.Date.from_string(quinzaine1_first_day).strftime('%Y-%m-%d')),('day','<=',fields.Date.from_string(self.date_transfert).strftime('%Y-%m-%d'))])
            if lines:
                if self.chantier_id_destiation.digital:
                    for line in lines[0:len(lines) -1]:
                        line.write({
                            'state':'draft'
                        })
                
                lines[len(lines) - 1].write({
                        'day_type':'1',
                        'details':'',
                        'chantier_id':False
                    })
                for reports in  self.env['hr.rapport.pointage'].search([('employee_id','=',self.employee_id.id),('period_id','=',lines[len(lines) - 1].rapport_id.period_id.id)]):
                    reports.write({
                        'chantier_id':self.chantier_id_source.id
                    })
                self.employee_id.write({
                    'chantier_id':self.chantier_id_source.id
                }) 


        return super(hr_employee_transfert,self).write(vals)

    
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
    

