from math import ceil
from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError,UserError
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
import calendar


class hr_filtre_pointage_wizard(models.TransientModel):       

    _name = "hr.filtre.pointage.wizard"

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
    
    def _get_ab_default(self):
        domain = [('id','=','-1')]
        year = date.today().year
        period_ids = []
        for mois_id in self.env["account.month.period"].search([('date_stop','<=',str(year)+'-12-31'),('date_start','>=',str(year-1)+'-01-01')]):  
            period_ids.append(mois_id.id) 
        if period_ids :
            domain = [('id', 'in',period_ids)]  

        return domain

        
    chantier_id = fields.Many2one("fleet.vehicle.chantier",u"Chantier",domain=_get_chantier_domain)
    periodicite = fields.Selection(related="chantier_id.periodicite")
    sous_chantier = fields.Many2one("fleet.vehicle.chantier.emplacement2",string="Equipes")
    employee_type = fields.Selection([("s","Salarié"),("o","Ouvrier")],string=u"Type d'employé")
    period_id = fields.Many2one("account.month.period",u'Période',domain = _get_ab_default)
    quinzaine = fields.Selection([('quinzaine1',"Première quinzaine"),('quinzaine2','Deuxième quinzaine'),('quinzaine12','Q1 + Q2')],string="Quinzaine",default='quinzaine1')
    jour = fields.Date('Date Jour')
    employee_id = fields.Many2one("hr.employee",string="Employées")
    vehicle_id = fields.Many2one("fleet.vehicle",u"Code engin")
    rapport_id = fields.Many2one("hr.rapport.pointage",u"Rapport Pointage", ondelete='cascade')

    @api.onchange('chantier_id')
    def _onchange_chantier_id(self):
        if self.chantier_id:
            self.quinzaine = 'quinzaine12' if self.chantier_id.periodicite == 2 or self.employee_type ==  's' else 'quinzaine1'

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.chantier_id = self.employee_id.chantier_id

    @api.onchange('employee_type')
    def _onchange_employee_type(self):
        if self.employee_type == 's' or self.chantier_id.periodicite == 2:
            self.quinzaine = 'quinzaine12'
        else:
            self.quinzaine = 'quinzaine1'

    def prepare_lines(self):
        
        result_to_return =  self.env['hr.rapport.pointage']
        active_ids = self.env.context.get('active_ids')
        res = {}

        where = [('period_id','=',self.period_id.id)]
       
       
        if self.chantier_id:
            where.append(('chantier_id','=',self.chantier_id.id))
        if self.sous_chantier:
            where.append(('emplacement_chantier_id','=',self.sous_chantier.id))
        if self.quinzaine:
            where.append(('quinzaine','=',self.quinzaine))
        if active_ids:
            result_to_return = self.env['hr.rapport.pointage'].search([('id', 'in',active_ids)])
            
        else:
            
            for line in list(self.env['hr.rapport.pointage'].search(where)):
                if line.employee_id.employee_type == self.employee_type:
                    result_to_return += self.env['hr.rapport.pointage'].browse(line.id)   
        
        return result_to_return
    
    def get_line_of_quinzaine(self,rapport_lines):

        number_of_page = ceil(float(len(rapport_lines))/16.0)
        result_to_return = []
        for i in range(0,int(number_of_page)):
            result_temp = []
            for line in rapport_lines[16*i:16*(i+1)]:
                res = self.env['hr.rapport.pointage.line']
                total = 0
                for line_day in line.rapport_lines:
                   
                    res += self.env['hr.rapport.pointage.line'].browse(line_day.id)
                    total += float(line_day.h_travailler)
                    
                result_temp.append({
                    'employee_id':line.employee_id,
                    'total':total,
                    'lines_quinzaine':res
                })
            result_to_return.append(result_temp)
        
        return result_to_return
    
    def get_line_of_quinzaine1(self,rapport_lines):

        number_of_page = ceil(float(len(rapport_lines))/16.0)
        result_to_return = []
        for i in range(0,int(number_of_page)):
            result_temp = []
            for line in rapport_lines[16*i:16*(i+1)]:
                res = self.env['hr.rapport.pointage.line']
                total = 0
                for line_day in line.rapport_lines:
                    if int(line_day.name[:2]) <= 15:
                        res += self.env['hr.rapport.pointage.line'].browse(line_day.id)
                        total += float(line_day.h_travailler)
                    
                result_temp.append({
                    'employee_id':line.employee_id,
                    'total':total,
                    'lines_quinzaine':res
                })
            result_to_return.append(result_temp)

        return result_to_return
    
    def get_line_of_quinzaine2(self,rapport_lines):

        number_of_page = ceil(float(len(rapport_lines))/16.0)
        result_to_return = []
        for i in range(0,int(number_of_page)):
            result_temp = []
            for line in rapport_lines[16*i:16*(i+1)]:
                res = self.env['hr.rapport.pointage.line']
                total = 0
                for line_day in line.rapport_lines:
                    if int(line_day.name[:2]) > 15:
                        res += self.env['hr.rapport.pointage.line'].browse(line_day.id)
                        total += float(line_day.h_travailler)
                    
                result_temp.append({
                    'employee_id':line.employee_id,
                    'total':total,
                    'lines_quinzaine':res
                })
            result_to_return.append(result_temp)

        return result_to_return
    
    def get_days(self,quinzaine,period_id):
        quinzaine1 ,quinzaine2 = [] ,[]
        
        if quinzaine == 'quinzaine1' or quinzaine == 'quinzaine12':
            i = 1
            while i <16:
                quinzaine1.append('%02d' % i)
                i+=1
        if quinzaine == 'quinzaine2' or quinzaine == 'quinzaine12':
            i = 16
            while i < self.env['hr.rapport.pointage'].get_range_month(period_id) + 1:
                quinzaine2.append('%02d' % i)
                i+=1
        return [quinzaine1,quinzaine2]

    
    def access_list_rapport_line_by_day(self):
        res = ''
        if not self.sous_chantier:
            raise UserError("Veuillez choisir une équipe")
        active_ids = self.env.context.get('active_ids')
        report_ids = self.prepare_lines()
        
        if not active_ids :
            if self.employee_type == 'employee1' :
                res = self.env['report'].get_action(report_ids, 'nxtm_employee_mngt.report_pointage_salarier_pdf')
            if self.employee_type == 'employee2':
                res = self.env['report'].get_action(self, 'nxtm_employee_mngt.report_pointage_ouvrier_pdf')
        else:
            record = self.env['hr.rapport.pointage'].browse(active_ids[0])
            self.period_id = record.period_id
            self.chantier_id = record.chantier_id
            self.sous_chantier = record.emplacement_chantier_id
            self.employee_type = record.employee_id.employee_type
            if record.employee_id.employee_type == 'employee1':
                res = self.env['report'].get_action(report_ids, 'nxtm_employee_mngt.report_pointage_salarier_pdf')
            if record.employee_id.employee_type == 'employee2':
                res = self.env['report'].get_action(self, 'nxtm_employee_mngt.report_pointage_ouvrier_pdf')
        
        return res
    
    
    def create_rapports_pointage_mass(self):

        periode = ''

        if int(self.period_id.name.split('/')[0]) > 1:
            periode = str("%02d" %(int(self.period_id.name.split('/')[0]) -1)) +'/'+self.period_id.name.split('/')[1] 
        else:
            periode = '12/'+str(int(self.period_id.name.split('/')[1]) -1) 

        query = """
                    select distinct(hrp.employee_id),hre.name_related,hre.employee_type from hr_rapport_pointage hrp 
                    left join hr_employee hre on hrp.employee_id = hre.id
                    where hrp.chantier_id = %s and hrp.period_id = (select id from account_period where name like '%s') and (hrp.etat not in (6,7) or hrp.emplacement_chantier_id not in (16))
                    order by hre.name_related asc
                """ % (self.chantier_id.id,periode)
        
        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()
        
        if res:
        
            for employee_id in res:
                if self.chantier_id.periodicite == 1 and employee_id['employee_type'] == 'employee2':
                    self.env['hr.rapport.pointage'].create({
                        'employee_id':employee_id['employee_id'],
                        'period_id':self.period_id.id,
                        'chantier_id':self.chantier_id.id,
                        'quinzaine':'quinzaine1'
                        })
                    self.env['hr.rapport.pointage'].create({
                        'employee_id':employee_id['employee_id'],
                        'period_id':self.period_id.id,
                        'chantier_id':self.chantier_id.id,
                        'quinzaine':'quinzaine2'
                        })
                else:
                    self.env['hr.rapport.pointage'].create({
                        'employee_id':employee_id['employee_id'],
                        'period_id':self.period_id.id,
                        'chantier_id':self.chantier_id.id,
                        'quinzaine':'quinzaine12'
                        })
        return True
    
    
    def create_rapports_pointage_individuel(self):

        if self.chantier_id.periodicite == 1 and self.employee_id.employee_type == 'o':
            self.env['hr.rapport.pointage'].create({
                'employee_id':self.employee_id.id,
                'period_id':self.period_id.id,
                'chantier_id':self.chantier_id.id,
                'quinzaine':'quinzaine1'
                })
            self.env['hr.rapport.pointage'].create({
                'employee_id':self.employee_id.id,
                'period_id':self.period_id.id,
                'chantier_id':self.chantier_id.id,
                'quinzaine':'quinzaine2'
                })
        else:
            self.env['hr.rapport.pointage'].create({
                'employee_id':self.employee_id.id,
                'period_id':self.period_id.id,
                'chantier_id':self.chantier_id.id,
                'quinzaine':'quinzaine12'
                })
        
        return True
    
    
    def cancel_rapport_creation(self):
        return True
    
    
    def create_payslip(self):
        periode = self.env['hr.payroll.ma.mois'].search([('mois','=',self.period_id.id)])
        if not periode:
            periode = self.env['hr.payroll.ma.mois'].create({
                'name':fields.Date.from_string(self.period_id.date_start).strftime("%B").capitalize()+' '+fields.Date.from_string(self.period_id.date_start).strftime("%Y"),
                'mois':self.period_id.id
            })
        note = self.env['hr.payslip'].get_prev_note(self.employee_id,periode)
        data = {
            'employee_id':self.employee_id.id,
            'chantier_id':self.chantier_id.id,
            'periode':periode.id,
            'job':self.employee_id.job,
            'employee_type':self.employee_id.employee_type,
            'vehicle_id':self.vehicle_id.id,
            'emplacement_chantier_id':self.sous_chantier.id,
            'rapport_id':self.rapport_id.id,
            'quinzaine':self.quinzaine,
            'note':note and note.get("note") or False
        }
        total_h,total_j = 0,0.0

        payslip_id = self.env['hr.payslip'].create(data)
        
        if self.quinzaine == 'quinzaine12':
            total_h = self.rapport_id.total_h_v
            total_j = self.rapport_id.total_j_v
        elif self.quinzaine == 'quinzaine1':
            for line_day in self.rapport_id.rapport_lines:
                if int(line_day.name[:2]) < 16 :
                    total_h += int(line_day.h_travailler_v) + int(line_day.h_sup)
                    total_j += float(line_day.j_travaille_v)
        else:
            for line_day in self.rapport_id.rapport_lines:
                if int(line_day.name[:2]) >= 16 :
                    total_h += int(line_day.h_travailler_v) + int(line_day.h_sup)
                    total_j += float(line_day.j_travaille_v)
        if payslip_id:
            payslip_id.recuperer_rubriques_payslip()
            for line in payslip_id.view_line_ids:
                if line.code == 'h1':
                    line.valeur = total_h
                if line.code == 'njt':
                    line.valeur = total_j
            payslip_id.compute_sheet_ma()
            
    
    def is_pointeur(self):

        return self.env['res.users'].has_group("nxtm_employee_mngt.group_pointage_user")
    
    
    def user_company_id(self):
        return self.chantier_id.cofabri
  