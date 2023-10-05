from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError,UserError
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
import calendar

class hr_employee_add_transit(models.TransientModel):

    _name="hr.employee.add.transit"

    def _get_chantier_domain(self):
        pointeur = self.env['res.users'].has_group("hr_management.group_pointeur")
        
        res = []
        if pointeur :
            for user_chantier in self.env.user.chantier_responsable_ids:
                res.append(user_chantier.id)
        else:
            for chantier in self.env['fleet.vehicle.chantier'].search([('type_chantier','in',('Chantier','Depot','Poste'))]):
                res.append(chantier.id)
        print(res)
        return [('id', 'in',res)] 
    
    def _get_engin_domain(self):
        pointeur = self.env['res.users'].has_group("hr_management.group_pointeur")
        
        res,chantiers = [],[]
        if pointeur :
            for user_chantier in self.env.user.chantier_responsable_ids:
                chantiers.append(user_chantier.id)
        else:
            for chantier in self.env['fleet.vehicle.chantier'].search([('type_chantier','in',('Chantier','Depot','Poste'))]):
                chantiers.append(chantier.id)
        

        query = """
                    select distinct(id) from fleet_vehicle where chantier_id in (""" + ','.join(map(str, chantiers)) + """);
                """ 
        self.env.cr.execute(query)
        for engin_id in self.env.cr.fetchall():
            res.append(engin_id[0])
                
        return [('id', 'in',res)]
    
    def _get_ab_default(self):
        domain = [('id','=','-1')]
        year = date.today().year
        period_ids = []
        for mois_id in self.env["account.month.period"].search([('date_stop','<=',str(year)+'-12-31'),('date_start','>=',str(year-1)+'-01-01')]):  
            period_ids.append(mois_id.id)
        if period_ids :
            domain = [('id', 'in',period_ids)]  

        return domain

    employee_id = fields.Char(string="Nom Employées",required=True)
    cin = fields.Char(string='N° CIN' ,required=True)
    job = fields.Char(string='FONCTION (Description)')
    job_id = fields.Many2one("hr.job",string="Titre du Poste",required=True)
    chantier = fields.Many2one("fleet.vehicle.chantier",string="Chantier",domain=_get_chantier_domain,required=True)
    vehicle = fields.Many2one("fleet.vehicle",string="Code Engin")
    emplacement = fields.Many2one("fleet.vehicle.chantier.emplacement",string="Equipe")
    employee_type = fields.Selection([("s","Salarié"),("o","Ouvrier")],string=u"Type d'employé",required=True)
    period_id = fields.Many2one("account.month.period",u'Période',required=True,domain = _get_ab_default)
    date_start = fields.Date('Date Début',required=True)
    quinzaine = fields.Selection([('quinzaine1',"Première quinzaine"),('quinzaine2','Deuxième quinzaine'),('quinzaine12','Q1 + Q2')],string="Quinzaine",default='quinzaine1')
    contract_type = fields.Many2one('hr.contract.type', string='Type Contrat')
    
    @api.onchange('date_start')
    def _onchange_date_start(self):
        if self.date_start:
            self.period_id = self.env['account.month.period'].get_period_from_date(str(self.date_start))
    
    @api.onchange('employee_type')
    def _onchange_employee_type(self):
        if self.employee_type == 's':
            self.quinzaine = 'quinzaine12'
        else:
            self.quinzaine = 'quinzaine1'
    
    def create_new_employee(self):

        data = {
            'emplacement_chantier_id':self.emplacement.id,
            'state_employee_wtf':'new',
            'vehicle_id':self.vehicle.id,
            'chantier_id':self.chantier.id,
            'name':self.employee_id.upper(),
            'cin':self.cin
        }
        if self.job:
            data['job'] = self.job.upper()

        res = self.env['hr.employee'].sudo().create(data)

        contract_data={
            'employee_id': res.id,
            'job_id':self.job_id.id,
            'date_start':self.date_start,
            'contract_type':self.contract_type.id,
            'wage':1,
            'type_emp':self.employee_type
        }

        contract_res = self.env['hr.contract'].sudo().create(contract_data)
        contract_res.write({
            'state':'open'
        })

        if self.chantier.periodicite == "1" and self.employee_type == 'o':
            self.env['hr.rapport.pointage'].sudo().create({
                'employee_id':res.id,
                'period_id':self.period_id.id,
                'chantier_id':self.chantier.id,
                'quinzaine':'quinzaine1'
                })
            self.env['hr.rapport.pointage'].sudo().create({
                'employee_id':res.id,
                'period_id':self.period_id.id,
                'chantier_id':self.chantier.id,
                'quinzaine':'quinzaine2'
                })
        else:
            self.env['hr.rapport.pointage'].sudo().create({
                'employee_id':res.id,
                'period_id':self.period_id.id,
                'chantier_id':self.chantier.id,
                'quinzaine':'quinzaine12'
                })
        
        if res :
            view = self.env.ref('hr_management.employee_tree')
            form = self.env.ref('hr_management.employee_view_form')
            
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'hr.employee',
                'views': [(view.id, 'tree'),(form.id,'form')],
                'target': 'current'
            }
        
    