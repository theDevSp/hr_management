from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError,UserError
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
import calendar
import locale

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

        for rapport in self:
            query = """
                    select sum(h_travailler::real) as tht,
                            sum(h_bonus::real) as thb,
                            sum(h_sup::real) as ths,
                            sum(h_travailler_v::real) as thtv  
                            from hr_rapport_pointage_line where rapport_id = %s;
                """   % (rapport.id)
            self.env.cr.execute(query)
            res = self.env.cr.dictfetchall()[0]

            rapport.total_h = res['tht'] if res else 0
            rapport.total_h_bonus = res['thb'] if res else 0
            rapport.total_h_sup = res['ths'] if res else 0
            rapport.total_h_v = res['thtv'] if res else 0
        
    def _compute_days(self):
        for rapport in self:
            query = """
                        select sum(j_travaille::real) as tj,sum(j_travaille_v::real) as tjv 
                        from hr_rapport_pointage_line where rapport_id = %s and day_type = '1';
                    """   % (rapport.id)
        
            self.env.cr.execute(query)
            res = self.env.cr.dictfetchall()[0]

            rapport.total_j = res['tj'] if res else 0
            rapport.total_j_v = res['tjv'] if res else 0
    

    def _compute_days_conge_absence_abondon(self):
        for rapport in self:
            query = """
                    select 
                    count(1) filter (where day_type='2' and h_travailler::real > 0) as tdim,
                    count(1) filter (where day_type='3' and h_travailler::real > 0) as tferie,
                    count(1) filter (where day_type='5') as tabsense
                    from hr_rapport_pointage_line where rapport_id = %s;
                """ % (rapport.id)
        
            self.env.cr.execute(query)
            res = self.env.cr.dictfetchall()[0]
            self.count_nbr_dim_days = res['tdim'] if res else 0
            self.count_nbr_ferier_days = res['tferie'] if res else 0
            self.count_nbr_absense_days = res['tabsense'] if res else 0
    
    def _compute_total_holidays(self):
        res = 0
        for holiday in self.holiday_ids:
            res += holiday.duree_jours
        self.count_nbr_holiday_days = res

    def _compute_holidays_liste(self):

        date_start = self.rapport_lines[0].day
        date_stop = self.rapport_lines[len(self.rapport_lines)-1].day

        self.holiday_ids = self.env['hr.holidays'].search([
                                    ('employee_id','=',self.employee_id.id),
                                    ('state','!=','draft'),
                                    '|',
                                        '|',
                                            '&',
                                            ('date_start','>=',date_start),
                                            ('date_start','<=',date_stop),
                                            '&',
                                            ('date_end','>=',date_start),
                                            ('date_end','<=',date_stop),
                                        '&',
                                        ('date_select_half_perso','>=',date_start),
                                        ('date_select_half_perso','<=',date_stop),
                                    ])         

        
        
    def _compute_transferts_liste(self):
        date_start = self.rapport_lines[0].day
        date_stop = self.rapport_lines[len(self.rapport_lines)-1].day

        self.transfert_ids = self.env['hr.employee.transfert'].search([
                                                ('employee_id','=',self.employee_id.id),
                                                '|',
                                                    '&',
                                                    ('date_transfert','>=',date_start),
                                                    ('date_transfert','<=',date_stop),
                                                    '&',
                                                    ('date_arriver','>=',date_start),
                                                    ('date_arriver','<=',date_stop)])


    name = fields.Char("Référence",readonly=True)
    employee_id = fields.Many2one("hr.employee",u"Employée",readonly=True, ondelete='cascade')
    cin = fields.Char(related='employee_id.cin',string="N° CIN",readonly=True)
    fonction = fields.Char(related='employee_id.job',string="Fonction",readonly=True)
    job_id = fields.Many2one(related='employee_id.job_id',string="Poste occupé",readonly=True)

    chantier_id = fields.Many2one("fleet.vehicle.chantier",u"Dernier Chantier",readonly=True)
    periodicite = fields.Selection(related='chantier_id.periodicite',readonly=True)
    grant_modification = fields.Boolean(related='chantier_id.grant_modification',readonly=True)

    vehicle_id = fields.Many2one("fleet.vehicle",u"Dérnier Code engin",readonly=True)
    emplacement_chantier_id = fields.Many2one("fleet.vehicle.chantier.emplacement","Dernière Équipe",readonly=True)

    period_id = fields.Many2one("account.month.period",u'Période',required=True,readonly=True,domain = _get_ab_default)

    total_h = fields.Float("Heures Travaillées",compute="_compute_hours",readonly=True)
    total_h_bonus = fields.Float("Heures Bonus",compute="_compute_hours",readonly=True)
    total_h_sup = fields.Float("Heures Supp",compute="_compute_hours",readonly=True)
    total_j = fields.Float("Jours Travaillés",readonly=True,compute="_compute_days")
    total_h_v = fields.Float("Heures Validées",compute="_compute_hours",readonly=True)
    total_j_v = fields.Float("Jours Validés",readonly=True,compute="_compute_days")

    note = fields.Text("Observation", states=READONLY_STATES)

    payslip_ids = fields.One2many("hr.payslip",'rapport_id',u'Fiche Paie',readonly=True)
    holiday_ids = fields.One2many("hr.holidays",'rapport_id',u'Congés',compute="_compute_holidays_liste")
    rapport_lines = fields.One2many("hr.rapport.pointage.line", 'rapport_id',string="Lignes Rapport Pointage")
    transfert_ids = fields.One2many("hr.employee.transfert",'rapport_id',u'Transfert',readonly=True,compute="_compute_transferts_liste")
    
    quinzaine = fields.Selection([('quinzaine1',"Première quinzaine"),('quinzaine2','Deuxième quinzaine'),('quinzaine12','Q1 + Q2')],string="Quinzaine")

    state = fields.Selection([('draft',u'Brouillon'),('working',u'Traitement En Cours'),('compute',u"Mois Calculé"),('valide',u"Validé"),('done',u"Clôturé"),('cancel','Annulé')],u"Etat Pointage",default='draft',tracking=True)

    count_nbr_holiday_days = fields.Float("Jours Congés",readonly=True,compute="_compute_total_holidays")
    count_nbr_ferier_days = fields.Float("Jours Fériés",readonly=True,compute="_compute_days_conge_absence_abondon")
    count_nbr_dim_days = fields.Float("Dimanches",readonly=True,compute="_compute_days_conge_absence_abondon")
    count_nbr_absense_days = fields.Float("Absences",readonly=True,compute="_compute_days_conge_absence_abondon")

    q1_state = fields.Selection([('q1_draft',u'En Attente'),('q1_working',u'Q1 Traitement En Cours'),('q1_compute',u"Q1 Calculé"),('q1_valide',u"Q1 Validé"),('q1_done',u"Q1 Clôturé")],u"Première Quinzaine",default="q1_draft")
    q2_state = fields.Selection([('q2_draft',u'En Attente'),('q2_working',u'Q2 Traitement En Cours'),('q2_compute',u"Q2 Calculé"),('q2_valide',u"Q2 Validé"),('q2_done',u"Q2 Clôturé")],u"Deuxième Quinzaine",default="q2_draft")

    type_emp = fields.Selection(related="employee_id.contract_id.type_emp",string=u"Type d'employé", required=False)

    def _compute_message_change_chantier(self):
        self.message_change_chantier = False
        if self.employee_id.contract_id.contract_type.depends_emplacement == True:
            for rapport_line in self.rapport_lines:
                if rapport_line.chantier_id.id != self.employee_id.contract_id.chantier_id.id and rapport_line.chantier_id:
                    self.message_change_chantier = "Attention !!! Cet employée posséde une contrat de chantier et il y a un changement de chantier détécté durant cette période."
                

    def _compute_message_end_existence_contract(self):
        self.message_end_existence_contract = False
        if self.employee_id.contract_id:
            if self.employee_id.contract_id.contract_type.depends_duration == True:
                end_date = datetime.now()
                start_date = self.employee_id.contract_id.date_end
                num_months = 0
                num_jours = 0
                if start_date:
                    num_months = (start_date.year - end_date.year) * 12 + (start_date.month - end_date.month) 
                    num_jours = (start_date.day - end_date.day)

                if num_months > 0.0 and num_months <= 3.0 or num_jours > 0:
                    self.message_end_existence_contract = "Attention !!! Contrat de %s sera terminé dans %s mois et %s jours. Date de fin de contrat est %s"%(self.employee_id.name,str(num_months),str(num_jours),start_date) 
                else:
                    self.message_end_existence_contract = False
        else:
            self.message_end_existence_contract = "Attention !!! Cet employé n'a pas encore de contrat"   

    def _compute_message_last_periode(self):
        obj = self.env['hr.payslip']
        self.message_last_periode = False
        self.message_gap_payement = False
        
        if self.period_id:
            date_stop = self.period_id.date_stop - relativedelta(months=+1)
            date_start = self.period_id.date_start - relativedelta(months=+1)
            period_id = self.env["account.month.period"].search([('date_stop','>=',date_stop),('date_start','<=',date_start)],limit=1) 
            
            prev_paied_period = obj.search([('employee_id',"=",self.employee_id.id),('period_id',"=",period_id.id),('quinzaine','=',self.quinzaine)])
            last_period = obj.search([('employee_id',"=",self.employee_id.id),('period_id','!=',self.period_id.id)],limit = 1,order="id desc") if not prev_paied_period else prev_paied_period
            if not prev_paied_period:
                self.message_gap_payement = "Un décalage de paiement est détecté"
            if last_period:
                self.message_last_periode = "Dernière période payée %s"%(last_period.period_id.name)
            else:
                self.message_last_periode = "C'est la première période travaillée"


    message_change_chantier = fields.Char('message_change_chantier',compute="_compute_message_change_chantier")
    message_end_existence_contract = fields.Char('message_end_existence_contract',compute="_compute_message_end_existence_contract")
    message_last_periode = fields.Char('message_last_periode',compute="_compute_message_last_periode")
    message_gap_payement = fields.Char('message_gap_payement',compute="_compute_message_last_periode")

    @api.model
    def create(self,vals):

        employee_id = self.env['hr.employee'].browse(vals['employee_id'])
        vals['name'] = self.env['ir.sequence'].next_by_code('hr.rapport.pointage.sequence')
        if not vals.get('chantier_id'):
            vals['chantier_id'] = employee_id.chantier_id.id  if employee_id.chantier_id else False
        vals['emplacement_chantier_id'] = employee_id.emplacement_chantier_id.id if employee_id.emplacement_chantier_id else False
        vals['vehicle_id'] = employee_id.vehicle_id.id if employee_id.vehicle_id else False
        
        if_exist = self.env['hr.rapport.pointage'].search_count([('period_id', '=', vals['period_id']),('employee_id', '=', vals['employee_id']),('quinzaine','=',vals['quinzaine'])])
        
        
        res = super(hr_rapport_pointage,self).create(vals)
        if not if_exist:
            
            if res.chantier_id.periodicite == '1' and res.employee_id.type_emp == 'o':
                if res.quinzaine == 'quinzaine1':
                    for line in self._prepare_rapport_pointage_lines(res.period_id,res.id,employee_id=vals['employee_id']):
                        if line['day'].date() <= self.get_half_month_day(res.period_id):
                            self.env['hr.rapport.pointage.line'].create(line)
                elif res.quinzaine == 'quinzaine2':
                    for line in self._prepare_rapport_pointage_lines(res.period_id,res.id,employee_id=vals['employee_id']):
                        if line['day'].date() > self.get_half_month_day(res.period_id):
                            self.env['hr.rapport.pointage.line'].create(line)
            else:
                for line in self._prepare_rapport_pointage_lines(res.period_id,res.id,employee_id=vals['employee_id']):
                    self.env['hr.rapport.pointage.line'].create(line)
        else:
            raise UserError('Rapport déja existe')

        return res

    def _prepare_rapport_pointage_lines(self,period_id,rapport_id,employee_id):   
                    
        nbr_days_months = self.get_range_month(period_id)
        repport_lines = []
        for number in range(nbr_days_months):
            day = number+1
            day_type = "1"
            name = self._get_day(period_id,day)
            if 'Dim' in name:
                day_type = "2"
            
            repport_lines.append({
                'name':name,
                'day':datetime(period_id.date_start.year,period_id.date_start.month, day),
                'day_type':str(day_type),
                'rapport_id':rapport_id,
                'employee_id':employee_id
            })
        return repport_lines
    
    
    def get_range_month(self,period_id):
        return calendar.monthrange(period_id.date_start.year, period_id.date_start.month)[1] 

    def _get_day(self,period_id,day):
        locale.setlocale(locale.LC_TIME, self.env.context['lang'] + '.utf8')
        return str('%02d' % day)+' '+datetime(period_id.date_start.year, period_id.date_start.month, day).strftime("%a").lower().capitalize().replace('.','')

    def get_first_n_characters(self,word,n):
        if word:
            if len(word) >= n:
                return word[:n]
        return word

    def is_pointeur(self):
        return self.env['res.users'].has_group("hr_management.group_pointeur")

    def create_payslip(self):
        view = self.env.ref('hr_management.fiche_paie_formulaire')

        data = {
            'employee_id':self.employee_id.id,
            'contract_id':self.employee_id.contract_id.id,
            'chantier_id':self.chantier_id.id,
            'period_id':self.period_id.id,
            'job_id':self.employee_id.job_id.id,
            'type_emp':self.employee_id.type_emp,
            'vehicle_id':self.vehicle_id.id,
            'emplacement_chantier_id':self.emplacement_chantier_id.id,
            'rapport_id':self.id,
            'quinzaine':self.quinzaine,
            'nbr_jour_travaille':self.total_j_v,
            'nbr_heure_travaille':self.total_h_v
        }
        created_payroll = self.env['hr.payslip'].create(data)

        return {
            'name': ("Fiche de paie %s crée" % created_payroll.name),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.payslip',
            'res_id': created_payroll.id,
            'views': [(view.id, 'form')],
            'view_id': view.id,
        }

    def action_validation(self):
        self.write({'state': 'valide'})
    
    def action_draft(self):
        self.write({'state': 'draft'})
    
    def action_cancel(self):
        self.write({'state': 'cancel'})
    
    def action_done(self):
        self.write({'state': 'done'})

    def action_working(self):
        if not self.employee_id.contract_id.profile_paie_id:
            raise ValidationError(
                        "Manque d'information, Cet employé n'a pas encors de profile de paie pour commancer le traitement. Veuillez régler la situation avant de procéder."
                    )
        self.write({'state': 'working'})
        for line in self.rapport_lines:
            line.j_travaille_v = self.employee_id.contract_id.get_hours_per_day(line.h_travailler_v)
    
    def get_half_month_day(self,period_id):
        period_month = period_id.date_start.month
        period_year = period_id.date_start.year
        return datetime.strptime(str(period_year)+'-'+str(period_month)+'-15', '%Y-%m-%d').date()
    
    def get_last_month_day(self):
        period_month = self.period_id.date_start.month
        period_year = self.period_id.date_start.year
        return datetime.strptime(str(period_year)+'-'+str(period_month)+'-'+str(calendar.monthrange(period_year, period_month)[1]), '%Y-%m-%d').date() 

    def user_company_id(self):
        return self.chantier_id.cofabri
    
    @api.depends('employee_id')
    def _compute_type_employee(self):
        self.employee_type = self.employee_id.type_emp

    def group_worked_time(self):
        data = {}
        for line in self.rapport_lines:
            key = line.chantier_id.id or 0 + line.emplacement_chantier_id.id or 0 + line.vehicle_id.id or 0
            if key > 0:
                data[key] = key 
        print(data)