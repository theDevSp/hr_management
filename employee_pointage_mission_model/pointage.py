from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
import calendar

class hr_rapport_pointage(models.Model):
    
    _name="hr.rapport.pointage"
    _description = "Rapport de Pointage"
    _inherit = ['mail.thread', 'mail.activity.mixin']
   

    READONLY_STATES = {
        'working': [('readonly', True)],
        'valide': [('readonly', True)],
        'compute': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)]
    }
    
    def _get_ab_default(self):
        domain = [('id','=','-1')]
        year = date.today().year
        period_ids = []
        for mois_id in self.env["account.month.period"].search([('date_stop','<=',str(year)+'-12-31'),('date_start','>=',str(year)+'-01-01')]):  
            period_ids.append(mois_id.id) 
        if period_ids :
            domain = [('id', 'in',period_ids)]  
        return domain


    def _compute_hours(self):
        query = """
                    select sum(h_travailler::real) as tht,sum(h_bonus::real) as thb,sum(h_sup::real) as ths,sum(h_travailler_v::real) as thtv  from hr_rapport_pointage_line where rapport_id = %s;
                """   % (self.id)
        if len(self.rapport_lines) > 0:
            self.env.cr.execute(query)
            res = self.env.cr.dictfetchall()[0]
            self.total_h = res['tht']
            self.total_h_bonus = res['thb']
            self.total_h_sup = res['ths']
            self.total_h_v = res['thtv']


    def _compute_days(self):
        query = """
                    select sum(j_travaille::real) as tj,sum(j_travaille_v::real) as tjv from hr_rapport_pointage_line where rapport_id = %s and day_type != '2';
                """   % (self.id)
        if len(self.rapport_lines) > 0:
            self.env.cr.execute(query)
            res = self.env.cr.dictfetchall()[0]
            self.total_j = res['tj']
            self.total_j_v = res['tjv']
    

    def _compute_days_conge_absence_abondon(self):
        query = """
                    select 
                    count(1) filter (where day_type='2' and h_travailler::real > 0) as tdim,
                    count(1) filter (where day_type='3' and h_travailler::real > 0) as tferie,
                    count(1) filter (where day_type='4') as tconge,
                    count(1) filter (where day_type='5') as tabsense
                    from hr_rapport_pointage_line where rapport_id = %s;
                """ % (self.id)
        if len(self.rapport_lines) > 0:
            self.env.cr.execute(query)
            res = self.env.cr.dictfetchall()[0]
            self.count_nbr_dim_days = res['tdim']
            self.count_nbr_ferier_days = res['tferie']
            self.count_nbr_holiday_days = res['tconge']
            self.count_nbr_absense_days = res['tabsense']


    def _compute_holidays_liste(self):
        query_result = self.env['hr.holidays']
        if self.employee_id:
            query = """
                    select id from hr_holidays where
                    employee_id = %s and
                    ((date_start >= '%s' and date_start <= '%s') or (date_end >= '%s' and date_end <= '%s'))
                    """   % (self.employee_id.id,self.rapport_lines[0].day,self.rapport_lines[len(self.rapport_lines) - 1].day,self.rapport_lines[0].day,self.rapport_lines[len(self.rapport_lines) - 1].day)
            self.env.cr.execute(query)            
            for id in self.env.cr.fetchall():
                query_result += self.env['hr.holidays'].browse(id[0])
        self.holiday_ids = query_result
        
        
    def _compute_transferts_liste(self):
        self.transfert_ids = self.env['hr.employee.transfert'].search([('employee_id','=',self.employee_id.id),('date_transfert','<=',self.period_id.date_stop),('date_transfert','>=',self.period_id.date_start)])


    def display_msg(self,msg,state):
        if state == 'danger':
            return  """
                        <div class="alert alert-danger">
                            <strong>Attention !!!</strong> %s.
                        </div>
                    """ %(msg)
        elif state == 'warning':
            return """
                        <div class="alert alert-warning">
                            <strong>Information !!!</strong> %s.
                        </div>
                    """ %(msg)
        elif state == 'infos':
            return """
                        <div class="alert alert-info">
                            <strong>Message !!!</strong> %s.
                        </div>
                    """ %(msg)


    def _render_html(self):
        self.data_html = ""
        last_period = self.env['hr.payslip'].search([('employee_id',"=",self.employee_id.id),('period_id','!=',self.period_id.id)],limit = 1,order="id desc")

        alerts = ''
        warnings = ''
        infos = ''

        errors = {}

        if self.employee_id.contract_id.contract_type.depends_duration == True:
            end_date = datetime.now()
            start_date = self.employee_id.contract_id.date_end
            num_months = 0
            num_jours = 0
            if start_date:
                num_months = (fields.Date.from_string(start_date).year - end_date.year) * 12 + (fields.Date.from_string(start_date).month - end_date.month) 
                num_jours = (fields.Date.from_string(start_date).day - end_date.day)
            if num_months > 0.0 and num_months <= 3.0 or num_jours > 0:
                errors['contrat_error'] = 1
                
        elif self.employee_id.contract_id.contract_type.depends_emplacement == True:
            for rapport_line in self.rapport_lines:
                if rapport_line.chantier_id.id != self.employee_id.contract_id.chantier_id.id and rapport_line.chantier_id:
                    errors['chantier_error'] = 1
        
        elif self.period_id and self.quinzaine == 'quinzaine12':
            date_stop = fields.Date.from_string(self.period_id.date_stop) - relativedelta(months=+1)
            date_start = fields.Date.from_string(self.period_id.date_start) - relativedelta(months=+1)
            period_id = self.env["account.month.period"].search([('date_stop','>=',date_stop),('date_start','<=',date_start)],limit=1)   
            prev_paied = self.env['hr.payslip'].search([('employee_id',"=",self.employee_id.id),('period_id',"=",period_id.id)])
            if not prev_paied:
                errors['period_error'] = 1
        
        elif self.period_id and self.quinzaine == 'quinzaine1':
            date_stop = fields.Date.from_string(self.period_id.date_stop) - relativedelta(months=+1)
            date_start = fields.Date.from_string(self.period_id.date_start) - relativedelta(months=+1)
            period_id = self.env["account.month.period"].search([('date_stop','>=',date_stop),('date_start','<=',date_start)],limit=1)   
            prev_paied = self.env['hr.payslip'].search([('employee_id',"=",self.employee_id.id),('period_id',"=",period_id.id),('quinzaine','=','quinzaine2')])  
            if not prev_paied:
                errors['period_error'] = 1

        elif self.period_id and self.quinzaine == 'quinzaine2':
            prev_paied = self.env['hr.payslip'].search([('employee_id',"=",self.employee_id.id),('period_id',"=",self.period_id.id),('quinzaine','=','quinzaine1')])  
            if not prev_paied:
                errors['period_error'] = 1      
            else:
                last_period = prev_paied
        
        if last_period:
            infos += self.display_msg("Dernière période payée %s"%(last_period.period_id.name),'infos')
        else:
            warnings += self.display_msg("C'est la première période travaillée",'warning')

        if errors.get('contrat_error'):
            alerts += self.display_msg("Contrat de %s sera terminé dans %s mois et %s jours. Date de fin de contrat est %s" %(self.employee_id.name,str(num_months),str(num_jours),start_date),'danger') 
        if errors.get('chantier_error'):
            alerts += self.display_msg("Cet employé possède un contrat de chantier et il y a un changement de chantier détécté durant cette période.",'danger')
        if errors.get('period_error'):
            alerts += self.display_msg("Un décalage de paiement est détecté",'danger')

        if alerts:
            self.data_html +=    """
                                <div class="col-md-4 panel-group">%s</div>
                            """%(alerts)
        if warnings:
            self.data_html +=    """
                                <div class="col-md-4 panel-group">%s</div>
                            """%(warnings)
        if infos:
            self.data_html +=    """
                                <div class="col-md-4 panel-group">%s</div>
                            """%(infos)

    name = fields.Char("Référence")
    employee_id = fields.Many2one("hr.employee",u"Employée",readonly=False, ondelete='cascade')
    cin = fields.Char(related='employee_id.cin',string="N° CIN",readonly=False)
    fonction = fields.Char(related='employee_id.job',string="Fonction",readonly=False)
    job_id = fields.Many2one(related='employee_id.job_id',string="Poste occupé",readonly=True)
    chantier_id = fields.Many2one("fleet.vehicle.chantier",u"Dernier Chantier",readonly=False)
    grant_modification = fields.Boolean(related='chantier_id.grant_modification')
    vehicle_id = fields.Many2one("fleet.vehicle",u"Dérnier Code engin",readonly=True)
    emplacement_chantier_id = fields.Many2one("fleet.vehicle.chantier.emplacement","Dernière Équipe",readonly=True)
    period_id = fields.Many2one("account.month.period",u'Période',required=True,readonly=False,domain = _get_ab_default)
    total_h = fields.Float("Heures Travaillées",compute="_compute_hours",readonly=True)
    total_h_bonus = fields.Float("Heures Bonus",compute="_compute_hours",readonly=True)
    total_h_sup = fields.Float("Heures Supp",compute="_compute_hours",readonly=True)
    total_j = fields.Float("Jours Travaillés",readonly=True,compute="_compute_days")
    total_h_v = fields.Float("Heures Validées",compute="_compute_hours",readonly=True)
    total_j_v = fields.Float("Jours Validés",readonly=True,compute="_compute_days")
    note = fields.Text("Observation", states=READONLY_STATES)
    payslip_ids = fields.One2many("hr.payslip",'rapport_id',u'Fiche Paie',readonly=True)
    holiday_ids = fields.One2many("hr.holidays",'rapport_id',u'Congés',readonly=True,compute="_compute_holidays_liste")
    # ####holiday_ids = fields.Many2many('hr.holydays', 'rapport_holidays_relation', 'holiday_ids', 'rapport_id', string="Congés")
    # transfert_ids = fields.One2many("hr.employee.transfert",'rapport_id',u'Transfert',readonly=True,compute="_compute_transferts_liste")
    etat = fields.Selection([('5',u"Absence Non Autorisé"),('6',u"Abondement de Poste"),('7',u"STC"),('8',u'Accident du Travail'),('9',u'Transfert')],u"État Salarié")
    quinzaine = fields.Selection([('quinzaine1',"Première quinzaine"),('quinzaine2','Deuxième quinzaine'),('quinzaine12','Q1 + Q2')],string="Quinzaine")

    state = fields.Selection([('draft',u'Brouillon'),('working',u'Traitement En Cours'),('compute',u"Mois Calculé"),('valide',u"Validé"),('done',u"Clôturé"),('cancel','Annulé')],u"Etat Pointage",default='draft',tracking=True)
    rapport_lines = fields.One2many("hr.rapport.pointage.line", 'rapport_id',string="Lignes Rapport Pointage")

    count_nbr_holiday_days = fields.Integer("Jours Congés",readonly=True,compute="_compute_days_conge_absence_abondon")
    count_nbr_ferier_days = fields.Integer("Jours Fériés",readonly=True,compute="_compute_days_conge_absence_abondon")
    count_nbr_dim_days = fields.Integer("Dimanches",readonly=True,compute="_compute_days_conge_absence_abondon")
    count_nbr_absense_days = fields.Integer("Absences",readonly=True,compute="_compute_days_conge_absence_abondon")

    q1_state = fields.Selection([('q1_draft',u'En Attente'),('q1_working',u'Q1 Traitement En Cours'),('q1_compute',u"Q1 Calculé"),('q1_valide',u"Q1 Validé"),('q1_done',u"Q1 Clôturé")],u"Première Quinzaine",default="q1_draft")
    q2_state = fields.Selection([('q2_draft',u'En Attente'),('q2_working',u'Q2 Traitement En Cours'),('q2_compute',u"Q2 Calculé"),('q2_valide',u"Q2 Validé"),('q2_done',u"Q2 Clôturé")],u"Deuxième Quinzaine",default="q2_draft")

    data_html = fields.Html('HTML Data', readonly=True, compute='_render_html')
  
    employee_type = fields.Selection([("s","Salarié"),("o","Ouvrier")],string=u"Type d'employé",default="s", compute="_compute_type_employee", store=True)
    # type_emp = fields.Selection(related="contract_id.type_emp",string=u"Type d'employé", required=False, store=True)
    # employee_type = fields.Selection(related='employee_id.type_emp',string="Type Employee",readonly=False)
    # periodicite = fields.Selection(related='chantier_id.periodicite')
    periodicite = fields.Selection([("1","Quinzaine"),("2","Mensuelle")],default="1",string="Périodicité",compute="_compute_periodicite", store=True)

    # @api.model
    # def create(self,vals):
    #     employee_id = self.env['hr.employee'].browse(vals['employee_id'])
    #     vals['name'] = self.env['ir.sequence'].next_by_code('hr.rapport.pointage')
    #     if not vals.get('chantier_id'):
    #         vals['chantier_id'] = employee_id.chantier_id.id 
    #     vals['emplacement_chantier_id'] = employee_id.emplacement_chantier_id.id
    #     # vals['vehicle_id'] = employee_id.vehicle_id.id
        
    #     if_exist = self.env['hr.rapport.pointage'].search_count([('period_id', '=', vals['period_id']),('employee_id', '=', vals['employee_id']),('quinzaine','=',vals['quinzaine'])])

    #     if not if_exist:
    #         res = super(hr_rapport_pointage,self).create(vals)
    #         if res.chantier_id.periodicite == '1' and res.employee_id.type_emp == 'o':
    #             if res.quinzaine == 'quinzaine1':
    #                 for line in self._prepare_rapport_pointage_lines(res.period_id,res.id,employee_id=vals['employee_id']):
    #                     if line['day'].date() <= self.get_half_month_day(res.period_id):
    #                         self.env['hr.rapport.pointage.line'].create(line)
    #             elif res.quinzaine == 'quinzaine2':
    #                 for line in self._prepare_rapport_pointage_lines(res.period_id,res.id,employee_id=vals['employee_id']):
    #                     if line['day'].date() > self.get_half_month_day(res.period_id):
    #                         self.env['hr.rapport.pointage.line'].create(line)
    #         else:
    #             for line in self._prepare_rapport_pointage_lines(res.period_id,res.id,employee_id=vals['employee_id']):
    #                 self.env['hr.rapport.pointage.line'].create(line)

    #     return True
    

    def write(self,vals):
        pointeur = self.env['res.users'].has_group("hr_management.group_pointeur")
        res = super(hr_rapport_pointage,self).write(vals)
        if pointeur or self._uid == SUPERUSER_ID:
            self.employee_id.write({'chantier_id':self.chantier_id.id})
            self.employee_id.write({'vehicle_id':self.vehicle_id.id})
            self.employee_id.write({'emplacement_chantier_id':self.emplacement_chantier_id.id})
        if 'state' in vals:
            for line in self.rapport_lines:
                line.write({'state':vals['state']})
        if 'q1_state' in vals:
            for line in self.rapport_lines:
                if fields.Date.from_string(line.day) <= self.get_half_month_day(self.period_id):
                    line.write({'state':vals['q1_state'][3:]})
        if 'q2_state' in vals:
            for line in self.rapport_lines:
                if fields.Date.from_string(line.day) > self.get_half_month_day(self.period_id) and fields.Date.from_string(line.day) <= self.get_last_month_day():
                    line.write({'state':vals['q2_state'][3:]})
        return res
    

    def _prepare_rapport_pointage_lines(self,period_id,rapport_id,employee_id):                 
        nbr_days_months = self.get_range_month(period_id)
        repport_lines = []
        for number in range(nbr_days_months):
            day = number+1
            day_type = 1
            name = self._get_day(period_id,day)
            if 'Dim' in name:
                day_type = 2
            
            repport_lines.append({
                'name':name,
                'day':datetime(fields.Date.from_string(period_id.date_start).year, fields.Date.from_string(period_id.date_start).month, day),
                'day_type':str(day_type),
                'rapport_id':rapport_id,
                'employee_id':employee_id
            })
        return repport_lines
    
    
    def get_range_month(self,period_id):
        return calendar.monthrange(fields.Date.from_string(period_id.date_start).year, fields.Date.from_string(period_id.date_start).month)[1] 

    def _get_day(self,period_id,day):
        return str('%02d' % day)+' '+datetime(fields.Date.from_string(period_id.date_start).year, fields.Date.from_string(period_id.date_start).month, day).strftime("%a").lower().capitalize().replace('.','')


    def action_pointage_user(self,employee_type,etat):
        pointeur = self.env['res.users'].has_group("hr_management.group_pointeur")
        view = self.env.ref('hr_management.rapport_pointage_tree_user') if pointeur else self.env.ref('hr_management.rapport_pointage_tree')
        form = self.env.ref('hr_management.rapport_pointage_form_user') if pointeur else self.env.ref('hr_management.rapport_pointage_form')
        res=[]
        where = ''
        if etat:
            where += 'etat = '+str(etat)
        else:
            where +='(etat = 5 or etat is null or etat = 9)'
        dest = 'Salariés' if employee_type == 's' else 'Ouvriers'

        query = ""

        if pointeur:
            query = """
                    select id from hr_rapport_pointage where chantier_id in (select chantier_id from chantier_responsable_relation where user_id = %s) and %s;
                """   % (self.env.user.id,where)
        else:
            query = """
                    select id from hr_rapport_pointage where %s;
                """   % (where)
        self.env.cr.execute(query)
        for result in self.env.cr.fetchall():
            res.append(result[0])
        
        context = {
                "search_default_group_by_public_market_id":1,
                "search_default_group_by_period_id":1,
                "search_default_group_by_emplacement_chantier_id":1
            }
        if employee_type == 'o':
            context['search_default_group_by_quinzaine'] = 1
        
        return {
            'name':'Pointage Mensuel ' + dest,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': self._name,
            'views': [(view.id, 'tree'),(form.id, 'form')],
            #'view_id': view.id,
            'target': 'current',
            'domain':[('id','in',res),('employee_id.type_emp','=',employee_type)],
            'context':context
        }
    

    def remove_first_word(self,word):
        if word:
            res = []
            for item in word.partition(' '):
                if item.lower() not in (' ','equipe') :
                    if '-' in item:
                        for subItem in item.partition('-'):
                            if '-' not in subItem:
                                res.append(subItem.lower().strip())
                    else:
                        res.append(item.lower())
            
            if len(res) <= 1 :
                return res[0].capitalize() 
            else:
                concat = ''
                for item in res:
                    concat += item[:4].capitalize()+'. '
                return concat


    def get_first_n_characters(self,word,n):
        if word:
            if len(word) >= n:
                return word[:n]
        return word
    

    def is_pointeur(self):
        return self.env['res.users'].has_group("hr_management.group_pointeur")
   
   
    """
    @api.multi
    def generate_payslip(self):
        view = self.env.ref(
            'hr_management.creation_payslip_wizard')
        
        
        if self.employee_id.type_emp == 'o':
            return {
                'name': _('Création Fiche de paie'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'hr.filtre.pointage.wizard',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context':{
                    'default_employee_id':self.employee_id.id,
                    'default_sous_chantier':self.emplacement_chantier_id.id,
                    'default_chantier_id':self.chantier_id.id,
                    'default_rapport_id':self.id,
                    'default_period_id':self.period_id.id
                }
            }
        else:
            self.create_payslip()

    """

    def create_payslip(self,quinzaine):
        # periode = self.env['account.month.period'].search([('id','=',self.period_id.id)])
        # note = self.env['hr.payslip'].get_prev_note(self.employee_id,periode)
        equipe = False
        
        res1 = self.env['hr.rapport.pointage.line'].search([('chantier_id','!=',False),('emplacement_chantier_id','!=',False),('rapport_id','=',self.id),('day','<=',str(self.get_half_month_day(self.period_id)))],order="id desc",limit=1)
        res2 = self.env['hr.rapport.pointage.line'].search([('chantier_id','!=',False),('emplacement_chantier_id','!=',False),('rapport_id','=',self.id)],order="id desc",limit=1)

        if quinzaine == 'quinzaine1' and res1:             
            equipe = res1[0].emplacement_chantier_id.id
        if quinzaine != 'quinzaine1' and res2:
            equipe = res2[0].emplacement_chantier_id.id
        data = {
            'employee_id':self.employee_id.id,
            'chantier_id':self.chantier_id.id,
            'period_id':self.period_id.id,
            'job_id':self.employee_id.job_id.id,
            'type_emp':self.employee_id.type_emp,
            'vehicle_id':self.vehicle_id.id,
            'emplacement_chantier_id':equipe,
            'rapport_id':self.id,
            'quinzaine':quinzaine,
            # 'note':note and note.get("note") or False
        }
        return self.env['hr.payslip'].create(data)
 

    def create_q1_payslip(self):
        total_h,total_j = 0,0.0
        payslip_id = self.create_payslip('quinzaine1')
        for line_day in self.rapport_lines:
            if float(line_day.name[:2]) < 16 :
                total_h += float(line_day.h_travailler_v)
                total_j += float(line_day.j_travaille_v)
        if payslip_id:
            payslip_id.recuperer_rubriques_payslip()
            for line in payslip_id.view_line_ids:
                if line.code == 'h1':
                    line.valeur = total_h
                if line.code == 'njt':
                    line.valeur = total_j 
            payslip_id.compute_sheet_ma()
            self.write({
                    'q1_state':'q1_compute'
                })
        

    def create_q2_payslip(self):
        total_h,total_j = 0,0.0
        payslip_id = self.create_payslip('quinzaine2')
        for line_day in self.rapport_lines:
            if float(line_day.name[:2]) >= 16 :
                total_h += float(line_day.h_travailler_v)
                total_j += float(line_day.j_travaille_v)
        if payslip_id:
            payslip_id.recuperer_rubriques_payslip()
            for line in payslip_id.view_line_ids:
                if line.code == 'h1':
                    line.valeur = total_h
                if line.code == 'njt':
                    line.valeur = total_j 
            payslip_id.compute_sheet_ma()
            self.write({
                    'q2_state':'q2_compute'
                })


    def create_q12_payslip(self):
        total_h,total_j = 0,0.0
        payslip_id = self.create_payslip('quinzaine12')
        total_h = self.total_h_v
        total_j = self.total_j_v
        if payslip_id:
            payslip_id.recuperer_rubriques_payslip()
            for line in payslip_id.view_line_ids:
                if line.code == 'h1':
                    line.valeur = total_h
                if line.code == 'njt':
                    line.valeur = total_j 
            payslip_id.compute_sheet_ma()
            self.write({
                    'state':'compute'
                })


    def action_validation(self):
        self.write({'state': 'valide'})
    
    def action_draft(self):
        self.write({'state': 'draft'})
    
    def action_cancel(self):
        self.write({'state': 'cancel'})
    
    def action_done(self):
        self.write({'state': 'done'})

    def action_working(self):
        self.write({'state': 'working'})
    
    #------------------------------- Q1 ---------------------------------

    def action_q1_working(self):
        self.write({'q1_state': 'q1_working'})
        for line in self.rapport_lines:
            if fields.Date.from_string(line.day) <= self.get_half_month_day(self.period_id):
                line.write({'state':'working'})
    
    def action_q1_draft(self):
        self.write({'q1_state': 'q1_draft'})
        for line in self.rapport_lines:
            if fields.Date.from_string(line.day) <= self.get_half_month_day(self.period_id):
                line.write({'state':'draft'})
    
    def action_q1_valide(self):
        self.write({'q1_state': 'q1_valide'})
        for line in self.rapport_lines:
            if fields.Date.from_string(line.day) <= self.get_half_month_day(self.period_id):
                line.write({'state':'valide'})

    def action_q1_done(self):
        self.write({'q1_state': 'q1_done'})
        for line in self.rapport_lines:
            if fields.Date.from_string(line.day) <= self.get_half_month_day(self.period_id):
                line.write({'state':'done'})
    
    #------------------------------- Q2 ---------------------------------

    def action_q2_working(self):
        self.write({'q2_state': 'q2_working'})
        for line in self.rapport_lines:
            if fields.Date.from_string(line.day) > self.get_half_month_day(self.period_id) and fields.Date.from_string(line.day) <= self.get_last_month_day():
                line.write({'state':'working'})
    
    def action_q2_draft(self):
        self.write({'q2_state': 'q2_draft'})
        for line in self.rapport_lines:
            if fields.Date.from_string(line.day) > self.get_half_month_day(self.period_id) and fields.Date.from_string(line.day) <= self.get_last_month_day():
                line.write({'state':'draft'})
    
    def action_q2_valide(self):
        self.write({'q2_state': 'q2_valide'})
        for line in self.rapport_lines:
            if fields.Date.from_string(line.day) > self.get_half_month_day(self.period_id) and fields.Date.from_string(line.day) <= self.get_last_month_day():
                line.write({'state':'valide'})
    
    def action_q2_done(self):
        self.write({'q2_state': 'q2_done'})
        for line in self.rapport_lines:
            if fields.Date.from_string(line.day) > self.get_half_month_day(self.period_id) and fields.Date.from_string(line.day) <= self.get_last_month_day():
                line.write({'state':'done'})
    
    def get_half_month_day(self,period_id):
        period_month = fields.Date.from_string(period_id.date_start).month
        period_year = fields.Date.from_string(period_id.date_start).year
        return fields.Date.from_string(str(period_year)+'-'+str(period_month)+'-15')
    
    def get_last_month_day(self):
        period_month = fields.Date.from_string(self.period_id.date_start).month
        period_year = fields.Date.from_string(self.period_id.date_start).year
        return fields.Date.from_string(str(period_year)+'-'+str(period_month)+'-'+str(calendar.monthrange(period_year, period_month)[1]))

    def user_company_id(self):
        return self.chantier_id.cofabri
    
    @api.depends('employee_id')
    def _compute_type_employee(self):
        self.employee_type = self.employee_id.type_emp

    @api.depends('chantier_id')
    def _compute_periodicite(self):
        self.periodicite = self.chantier_id.periodicite