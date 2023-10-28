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
    sous_chantier = fields.Many2one("fleet.vehicle.chantier.emplacement",string="Equipes")
    employee_type = fields.Selection([("s","Salarié"),("o","Ouvrier")],string=u"Type d'employé")
    period_id = fields.Many2one("account.month.period",u'Période',domain = _get_ab_default)
    quinzaine = fields.Selection([('quinzaine1',"Première quinzaine"),('quinzaine2','Deuxième quinzaine'),('quinzaine12','Q1 + Q2')],string="Quinzaine")
    jour = fields.Date('Date Jour')
    employee_id = fields.Many2one("hr.employee",string="Employées")
    vehicle_id = fields.Many2one("fleet.vehicle",u"Code engin")
    rapport_id = fields.Many2one("hr.rapport.pointage",u"Rapport Pointage", ondelete='cascade')

    @api.onchange('chantier_id')
    def _onchange_chantier_id(self):
        if self.chantier_id:
            self.quinzaine = 'quinzaine12' if self.employee_type ==  's' else 'quinzaine1'

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.chantier_id = self.employee_id.chantier_id
            self.employee_type = self.employee_id.type_emp
        

    @api.onchange('employee_type')
    def _onchange_employee_type(self):
        if self.employee_type == 's':
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
    
    def create_rapports_pointage_mass(self):

        pointeur = self.env['res.users'].has_group("hr_management.group_pointeur")
        now = datetime.now()

        period_month = self.period_id.date_start.month
        period_year = self.period_id.date_start.year

        last_period_month = period_month - 1 if period_month > 1 else 12
        last_period_year = period_year if period_month > 1 else period_year - 1

        quinzaine1_first_day = datetime.strptime(str(period_year)+'-'+str(period_month)+'-01', "%Y-%m-%d")
        quinzaine1_day_ref = datetime.strptime(str(period_year)+'-'+str(period_month)+'-18', "%Y-%m-%d")
        quinzaine2_day_ref = datetime.strptime(str(period_year)+'-'+str(period_month + 1)+'-03', "%Y-%m-%d")  if period_month != 12 else datetime.strptime(str(period_year +1)+'-01-03', "%Y-%m-%d")

        quinzaine1_delimite = datetime.strptime(str(period_year)+'-'+str(period_month)+'-15', "%Y-%m-%d")
        quinzaine2_delimite = datetime.strptime(str(period_year)+'-'+str(period_month)+'-'+str(calendar.monthrange(period_year, period_month)[1]), "%Y-%m-%d")

        last_period_qu1_first_day = datetime.strptime(str(last_period_year)+'-'+str(last_period_month)+'-01', "%Y-%m-%d")
        last_period_qu1_day_ref = datetime.strptime(str(last_period_year)+'-'+str(last_period_month)+'-18', "%Y-%m-%d")
        last_period_qu2_day_ref = datetime.strptime(str(last_period_year)+'-'+str(last_period_month + 1)+'-03', "%Y-%m-%d")  if last_period_month != 12 else datetime.strptime(str(last_period_year +1)+'-01-03', "%Y-%m-%d")

        last_period_qu1_delimite = datetime.strptime(str(last_period_year)+'-'+str(last_period_month)+'-15', "%Y-%m-%d")
        last_period_qu2_delimite = datetime.strptime(str(last_period_year)+'-'+str(last_period_month)+'-'+str(calendar.monthrange(last_period_year, last_period_month)[1]), "%Y-%m-%d")

        #---------- get liste of excluded employees --------------------
        exclud_list,result,foreign_list = [],[],[]
        #---------- quainzaine 1 ---------------------------------------

        if self.quinzaine == 'quinzaine1' and self.previlege_validation():

            exclud_list = [ln['employee_id'][0] for ln in self.env['declaration.anomalie.employee.sur.chantier'].read_group(
                                domain=[
                                    ('chantier_id', '=', self.chantier_id.id),
                                    ('state', 'in', ('valide','approuved')),
                                    ('date_fait', '>=', last_period_qu1_delimite),
                                    ('date_fait', '<=', now),
                                    ('type_declaration','in',('6','7'))
                                ],
                                fields=['employee_id'],
                                groupby=['employee_id'],
                            )] 

            res = [ln['employee_id'][0] for ln in self.env['hr.rapport.pointage'].read_group(
                                domain=[
                                    ('chantier_id', '=', self.chantier_id.id),
                                    ('period_id', '=', self.period_id.id - 1),
                                    ('type_emp', '=', self.employee_type),
                                ],
                                fields=['employee_id'],
                                groupby=['employee_id'],
                            )] 
            result = filter(lambda ln: ln not in exclud_list, res)

        #---------- quainzaine 2 ---------------------------------------

        elif self.quinzaine == 'quinzaine2' and self.previlege_validation():

            exclud_list = [ln['employee_id'][0] for ln in self.env['declaration.anomalie.employee.sur.chantier'].read_group(
                                domain=[
                                    ('chantier_id', '=', self.chantier_id.id),
                                    ('state', 'in', ('valide','approuved')),
                                    ('date_fait', '>=', quinzaine1_first_day),
                                    ('date_fait', '<=', now),
                                    ('type_declaration','in',('6','7'))
                                ],
                                fields=['employee_id'],
                                groupby=['employee_id'],
                            )] 

            res = [ln['employee_id'][0] for ln in self.env['hr.rapport.pointage'].read_group(
                                domain=[
                                    ('chantier_id', '=', self.chantier_id.id),
                                    ('period_id', '=', self.period_id.id),
                                    ('type_emp', '=', self.employee_type),
                                ],
                                fields=['employee_id'],
                                groupby=['employee_id'],
                            )] 
            result = filter(lambda ln: ln not in exclud_list, res)

        #---------- quainzaine 1 + 2 -----------------------------------
        
        elif self.quinzaine == 'quinzaine12' and self.previlege_validation():

            exclud_list = [ln['employee_id'][0] for ln in self.env['declaration.anomalie.employee.sur.chantier'].read_group(
                                domain=[
                                    ('chantier_id', '=', self.chantier_id.id),
                                    ('state', 'in', ('valide','approuved')),
                                    ('date_fait', '>=', quinzaine1_first_day),
                                    ('date_fait', '<=', now),
                                    ('type_declaration','in',('6','7'))
                                ],
                                fields=['employee_id'],
                                groupby=['employee_id'],
                            )] 

            res = [ln['employee_id'][0] for ln in self.env['hr.rapport.pointage'].read_group(
                                domain=[
                                    ('chantier_id', '=', self.chantier_id.id),
                                    ('period_id', '=', self.period_id.id - 1),
                                    ('type_emp', '=', self.employee_type),
                                ],
                                fields=['employee_id'],
                                groupby=['employee_id'],
                            )] 

            result = filter(lambda ln: ln not in exclud_list, res)
        
        else:
            raise ValidationError ('Action non autoriée')

        if result:
        
            for employee_id in result:
                self.env['hr.rapport.pointage'].sudo().create({
                    'employee_id':employee_id,
                    'period_id':self.period_id.id,
                    'chantier_id':self.chantier_id.id,
                    'quinzaine':self.quinzaine
                    })
                    
        
        return True
    
    def previlege_validation(self):
        pointeur = self.env['res.users'].has_group("hr_management.group_pointeur")
        dates = self.verification_dates()

        quz1_condition = self.quinzaine == 'quinzaine1' and pointeur and (dates['now'] < dates['quz1_03'] or dates['now'] >= dates['quz1_18'])
        quz2_condition = self.quinzaine == 'quinzaine2' and pointeur and (dates['now'] >= dates['quz2_03'] or dates['now'] < dates['quz1_18'])
        quz12_condition = self.quinzaine == 'quinzaine12' and pointeur and (dates['now'] < dates['quz1_03'] or dates['now'] >= dates['quz2_03'])

        if quz12_condition or quz1_condition or quz2_condition:
            return False

        return True
    
    def create_rapports_pointage_individuel(self):
        

        if self.employee_id.type_emp == 'o' and self.quinzaine == 'quinzaine1' and self.previlege_validation():
            self.env['hr.rapport.pointage'].sudo().create({
                'employee_id':self.employee_id.id,
                'period_id':self.period_id.id,
                'chantier_id':self.chantier_id.id,
                'quinzaine':'quinzaine1'
                })
        elif self.employee_id.type_emp == 'o' and self.quinzaine == 'quinzaine2' and self.previlege_validation():
            self.env['hr.rapport.pointage'].sudo().create({
                'employee_id':self.employee_id.id,
                'period_id':self.period_id.id,
                'chantier_id':self.chantier_id.id,
                'quinzaine':'quinzaine2'
                })
        elif self.employee_id.type_emp == 's' and self.quinzaine == 'quinzaine12' and self.previlege_validation():
            self.env['hr.rapport.pointage'].sudo().create({
                'employee_id':self.employee_id.id,
                'period_id':self.period_id.id,
                'chantier_id':self.chantier_id.id,
                'quinzaine':'quinzaine12'
                })
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ("Erreur de saisie"),
                    'message': ("Information saisis erronées veuillez réessayer"),
                    'sticky': False,
                    'type': 'danger',
                }
            }
        
        return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ("Succés"),
                    'message': ("Rapport généré avec succé"),
                    'sticky': False,
                    'type': 'success',
                }
            }
    
    
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

        return self.env['res.users'].has_group("hr_management.group_pointeur")
    
    def user_company_id(self):
        return self.chantier_id.cofabri
    
    def verification_dates(self):
        now = datetime.now()

        period_month = self.period_id.date_start.month
        period_year = self.period_id.date_start.year

        last_period_month = period_month - 1 if period_month > 1 else 12
        last_period_year = period_year if period_month > 1 else period_year - 1

        quinzaine1_first_day = datetime.strptime(str(period_year)+'-'+str(period_month)+'-01', "%Y-%m-%d") # ---  01/xx/xxxx
        quinzaine1_third_day = datetime.strptime(str(period_year)+'-'+str(period_month)+'-03', "%Y-%m-%d") # ---  03/xx/xxxx
        quinzaine1_day_ref = datetime.strptime(str(period_year)+'-'+str(period_month)+'-18', "%Y-%m-%d") # --- 18/xx/xxxx
        # --- 03/01/xxxx + 1 if xx == 12 else 03/xx + 01/xxxx
        quinzaine2_day_ref = datetime.strptime(str(period_year)+'-'+str(period_month + 1)+'-03', "%Y-%m-%d")  if period_month != 12 else datetime.strptime(str(period_year +1)+'-01-03', "%Y-%m-%d")

        quinzaine1_delimite = datetime.strptime(str(period_year)+'-'+str(period_month)+'-15', "%Y-%m-%d") # --- 15/xx/xxxx
        quinzaine2_delimite = datetime.strptime(str(period_year)+'-'+str(period_month)+'-'+str(calendar.monthrange(period_year, period_month)[1]), "%Y-%m-%d") # --- 30/xx/xxxx
        
        # --- same as above for period before current period
        last_period_qu1_first_day = datetime.strptime(str(last_period_year)+'-'+str(last_period_month)+'-01', "%Y-%m-%d")
        last_period_qu1_day_ref = datetime.strptime(str(last_period_year)+'-'+str(last_period_month)+'-18', "%Y-%m-%d")
        last_period_qu2_day_ref = datetime.strptime(str(last_period_year)+'-'+str(last_period_month + 1)+'-03', "%Y-%m-%d")  if last_period_month != 12 else datetime.strptime(str(last_period_year +1)+'-01-03', "%Y-%m-%d")

        last_period_qu1_delimite = datetime.strptime(str(last_period_year)+'-'+str(last_period_month)+'-15', "%Y-%m-%d")
        last_period_qu2_delimite = datetime.strptime(str(last_period_year)+'-'+str(last_period_month)+'-'+str(calendar.monthrange(last_period_year, last_period_month)[1]), "%Y-%m-%d")

        return {
                'now':now,
                'quz1_01':quinzaine1_first_day,
                'quz1_03':quinzaine1_third_day,
                'quz1_18':quinzaine1_day_ref,
                'quz2_03':quinzaine2_day_ref,
                'quz1_15':quinzaine1_delimite,
                'quz2_30':quinzaine2_delimite,
                'last_period_qu1_01':last_period_qu1_first_day,
                'last_period_qu1_18':last_period_qu1_day_ref,
                'last_period_qu2_03':last_period_qu2_day_ref,
                'last_period_qu1_15':last_period_qu1_delimite,
                'last_period_qu2_30':last_period_qu2_delimite,
            }
