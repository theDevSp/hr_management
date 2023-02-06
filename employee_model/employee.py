from odoo import fields, models, api
from odoo.osv import expression
from datetime import date
from dateutil.relativedelta import relativedelta

class hr_employee(models.Model):
    _description = "Employee"
    _order = 'name'
    _inherit = ['hr.employee']
    _mail_post_access = 'read'

    cin = fields.Char('CIN', required=True)
    cnss = fields.Char('CNSS')
    type_emp = fields.Selection([("s","Salarié"),("o","Ouvrier")],string=u"Type d'employé",default="s")
    title_id = fields.Many2one("res.partner.title","Titre")
    #bank = fields.Many2one("bank","Banque")
    ville_bank = fields.Char(u"Ville")
    bank_agence = fields.Char(u"Agence")
    adress_personnel = fields.Char(u'Adresse personnel')
    bank_account = fields.Char(u'N° RIB')
    job = fields.Char("Fonction")
    cotisation = fields.Boolean("Activer Cotisation-CIMR")
    diplome = fields.Char(u"Diplôme")
    embaucher_par  = fields.Many2one("hr.responsable.chantier",u"Embaucher Par")
    recommander_par  = fields.Many2one("hr.responsable.chantier",u"Recommander Par")
    motif_enbauche  = fields.Selection([("1","Satisfaire un besoin"),("2","Remplacement"),("3","Autre")],u"Motif d'embauche")
    obs_embauche  = fields.Char(u"Observation")
    employee_age = fields.Integer(u"Âge",compute="_compute_age")
    date_naissance = fields.Date(u"Date Naissance")
    lieu_naissance = fields.Char(u"Lieu Naissance")
    montant_cimr = fields.Float(u"Montant Cotisation CIMR")

    date_start = fields.Date(related="contract_id.date_start",string='Date Debut')
    date_end = fields.Date(related="contract_id.date_end",string='Date Fin')
    remaining_days = fields.Char(compute="_compute_remaining_days",string='Jours Restants')
    date_cin = fields.Date(u'Date validité CIN')
    phone1 = fields.Char(u"Tél. Portable 1")
    phone2 = fields.Char(u"Tél. Portable 2")
    phone3 = fields.Char(u"Tél. Portable 3")
    #payslip_count = fields.Integer(compute='_compute_payslip')    
    #nbr_jour_ferie = fields.Float(u"Nombre de Jours Fériés",compute="_compute_jf")
    working_years = fields.Char(compute='_compute_working_years',string="Ancienneté")
    
    currency_f = fields.Many2one('res.currency', string='Currency')
    wage = fields.Monetary(related="contract_id.wage",string='Salaire', required=True, tracking=True, currency_field = "currency_f")
    chantier_id  = fields.Many2one("fleet.vehicle.chantier",u"Chantier")
    
    wage_jour = fields.Float(string='Salaire Journalier')
    state_employee_wtf = fields.Selection([("new","Nouveau Embauche"),("transfert","Transfert"),("active","Active"),("stc","STC")],u"Situation Employée",index=True, copy=False, default='new', tracking=True)
    active = fields.Boolean('Active', related='resource_id.active', default=True, store=True, readonly=False)
    chantier_id  = fields.Many2one("fleet.vehicle.chantier",u"Chantier")
    emplacement_chantier_id = fields.Many2one("fleet.vehicle.chantier.emplacement",u"Équipe")
    company_id = fields.Many2one('res.company', 'Company', required=True,default=1)
    nombre_enfants = fields.Integer(u"Nombre d'enfants")
    responsable_id = fields.Many2one("hr.responsable.chantier","Responsable")
    black_list = fields.Boolean("Liste Noire", readonly=True, default=False)
    blacklist_histo = fields.One2many('hr.blacklist', 'employee_id',readonly=True)
    motif_blacklist = fields.Char("Motif Blacklist", compute = "_compute_motif_blacklist")
   
    def _compute_age(self):
        for employee in self:
            if employee.date_naissance:
                today = date.today() 
                birthDate = fields.Date.from_string(employee.date_naissance)
                age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
                employee.employee_age = age
            else :
                employee.employee_age = 0           


    def _compute_remaining_days(self):
        for rec in self :
            query = """
                        select cast(date_part('day',date_end::timestamp - CURRENT_DATE::timestamp) as int) from hr_contract where
                        employee_id = %s;
                    """   % (rec.id)
            rec.env.cr.execute(query)
            res = rec.env.cr.fetchall()
            if len(res) > 0:
                rec.remaining_days = res[0][0]
            else :
                rec.remaining_days = 0
  

    def _compute_working_years(self):
        for employee in self:
            if employee.contract_id.date_start:
                res = ""
                today = date.today() 
                start_woring_year = fields.Date.from_string(employee.contract_id.date_start)
                diff = relativedelta(today, start_woring_year)
                if diff.years > 0 :
                    res += str(diff.years) + ' Années\n'
                if diff.months > 0 :
                    res += str(diff.months) + ' mois\n'
                if diff.days > 0 :
                    res += str(diff.days) + ' jours'
                employee.working_years = res
            else :
                employee.working_years = str(0) + ' jours'


    def _compute_salaire_jour(self):
        for employee in self:
            if employee.wage:
                if employee.contract_id.function.function_id.code != "Gc" :
                    employee.wage_jour = employee.wage/26
                else:
                    employee.wage_jour = employee.wage/30
            else :
                employee.wage_jour = 0


    @api.model
    def _contracts_salary(self):  
        parent_id = self.env.context.get('parent_id') 
        parent_model = self.env.context.get('parent_model')       
        if parent_id and parent_model:
            parent_obj = self.env[parent_model].browse(parent_id)
            Contract = self.env['hr.contract'].search([('employee_id', '=', parent_obj.employee_id)])
            return Contract.wage


    def view_employee_payslips(self):
        res = []
        view = self.env.ref('hr_payroll.view_hr_payslip_tree')
        form = self.env.ref('hr_payroll.view_hr_payslip_form')
 
        payslips = self.env['hr.payslip'].search([('employee_id', '=', self.id)])
        for data in payslips:
            res.append(data.id)
            
        return {    
            'type': 'ir.actions.act_window',
            'name': 'Listes des Employées',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hr.payslip',
            'views': [(view.id, 'tree'),(form.id,'form')],
            'target': 'current',
            'domain':[('id','in',res)]
            }


    @api.onchange("identification_id")
    def _verify_new_recruit(self):
        if self.identification_id:
            employee = self.env['hr.employee'].search([('identification_id', '=', self.identification_id)])
            if employee:
                if employee.black_list:
                    return {'warning': {
                    'title': 'Avertissement',
                    'message': u"Un employé avec le numéro CIN que vous avez saisi existe déjà et il est fiché dans la liste noire",
                        }
                    }
                else:
                    return {'warning': {
                    'title': 'Avertissement',
                    'message': u"Un employé avec le numéro CIN que vous avez saisi existe déjà ",
                        }
                    }
    
    def _get_active_employee(self,employee_type):
        pointeur = self.env['res.users'].has_group("nxtm_employee_mngt.group_pointage_user")
        res =  []
        query = ""
        if pointeur:
            query = """
                    select distinct(id) from hr_employee where chantier_id in (select chantier_id from chantier_responsable_relation where user_id = %s) and state_employee_wtf = 'active' and employee_type = '%s';
                """   % (self.env.user.id,str(employee_type))
        else:
            query = """
                    select distinct(id) from hr_employee where chantier_id in (select id from fleet_vehicle_chantier where employee_type = '%s' and lower(name) not like '%s' and lower(name) not ilike '%s') and state_employee_wtf = 'active' ;
                """  % (str(employee_type),str('%gasoil%'),str('%citern%'))

        self.env.cr.execute(query)
        for employee_id in self.env.cr.fetchall():
            res.append(employee_id[0])

        return res
    
    def _get_new_employee(self):
        pointeur = self.env['res.users'].has_group("nxtm_employee_mngt.group_pointage_user")
        res =  []
        query = ""

        if pointeur:
            query = """
                    select distinct(id) from hr_employee where chantier_id in (select chantier_id from chantier_responsable_relation where user_id = %s) and state_employee_wtf = 'new';
                """   % (self.env.user.id)
        else:
            query = """
                    select distinct(id) from hr_employee where chantier_id in (select id from fleet_vehicle_chantier where lower(name) not like '%gasoil%' and lower(name) not ilike '%citern%') and state_employee_wtf = 'new';
                """ 

        self.env.cr.execute(query)
        for employee_id in self.env.cr.fetchall():
            res.append(employee_id[0])

        return res


    def action_active_salarie(self):
        pointeur = self.env['res.users'].has_group("nxtm_employee_mngt.group_pointage_user")
        view = self.env.ref('nxtm_employee_mngt.hr_tree') if not pointeur else self.env.ref('nxtm_employee_mngt.hr_pointeur_tree')
        form = self.env.ref('nxtm_employee_mngt.hr_form') if not pointeur else self.env.ref('nxtm_employee_mngt.hr_pointeur_form')
        
        return {
            'name':'Liste des Salariés',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hr.employee',
            'views': [(view.id, 'tree'),(form.id,'form')],
            'target': 'current',
            'domain':[('id', 'in',self._get_active_employee('s'))]
        }
    
        
    def action_active_ouvrier(self):
        pointeur = self.env['res.users'].has_group("nxtm_employee_mngt.group_pointage_user")
        view = self.env.ref('nxtm_employee_mngt.hr_tree') if not pointeur else self.env.ref('nxtm_employee_mngt.hr_pointeur_tree')
        form = self.env.ref('nxtm_employee_mngt.hr_form') if not pointeur else self.env.ref('nxtm_employee_mngt.hr_pointeur_form')
        
        return {
            'name':'Liste des Ouvriers',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hr.employee',
            'views': [(view.id, 'tree'),(form.id,'form')],
            'target': 'current',
            'domain':[('id', 'in',self._get_active_employee('o'))]
        }


    def nouveau_embauche(self):
        pointeur = self.env['res.users'].has_group("nxtm_employee_mngt.group_pointage_user")
        view = self.env.ref('nxtm_employee_mngt.hr_tree') if not pointeur else self.env.ref('nxtm_employee_mngt.hr_pointeur_tree')
        form = self.env.ref('nxtm_employee_mngt.hr_form') if not pointeur else self.env.ref('nxtm_employee_mngt.hr_pointeur_form')
        
        return {
            'name':'Liste des Nouveaux Embauches',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hr.employee',
            'views': [(view.id, 'tree'),(form.id,'form')],
            'target': 'current',
            'domain':[('id', 'in',self._get_new_employee())]
        }
        
    def _get_fin_contrat(self,contract_type,periode):

        query = """
                    select distinct(employee_id) from hr_contract where
                    date_part('day',date_end::timestamp - CURRENT_DATE::timestamp) >= 0 
					and date_part('day',date_end::timestamp - CURRENT_DATE::timestamp) <= %s
					and contract_type = %s;
                """   % (periode,contract_type)

        self.env.cr.execute(query)
        res = []
        for employee in self.env.cr.fetchall():
            res.append(employee[0])
        return res


    def action_fin_contrat(self):
        
        view = self.env.ref('nxtm_employee_mngt.hr_fin_contrat_tree')
        form = self.env.ref('nxtm_employee_mngt.hr_form')
        
        return {
            'name':'Fin de Contrat',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hr.employee',
            'views': [(view.id, 'tree'),(form.id,'form')],
            'target': 'current',
            'domain':[('id','in',self._get_fin_contrat(2,90))]
        }
    
    def action_fin_contrat_6(self):
        
        view = self.env.ref('nxtm_employee_mngt.hr_fin_contrat_tree')
        form = self.env.ref('nxtm_employee_mngt.hr_form')
        
        return {
            'name':'Fin de Contrat 6 mois',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hr.employee',
            'views': [(view.id, 'tree'),(form.id,'form')],
            'target': 'current',
            'domain':[('id','in',self._get_fin_contrat(4,30))]
        }

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        args2 = ['|',['name',operator,name],['identification_id',operator,name], ['cin',operator,name], ['cnss',operator,name],['chantier_id',operator,name],['emplacement_chantier_id',operator,name]]
        
        args = args2+args
        recs = self.search(args, limit=limit)
        return recs.name_get()

    @api.model
    def create(self,vals):
        vals['state_employee_wtf'] ='new'
        return super(hr_employee,self).create(vals)


    def open_wizard(self):
        view = self.env.ref('hr_management.wizard_blacklist_view_form')

        if self.black_list:
            action_index = "debloque"
            action_value = "Débloquer"
        else:
            action_index = "bloque"
            action_value = "Bloquer"

        return {
            'name': ("\"" + action_value + "\" l'employée : " + self.name),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard_blacklist',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context' : {
                        'default_employee_id': self.id,
                        'default_chantier_id': self.chantier_id.id,
                        'default_action': action_index,
                        },
        }

    def _compute_motif_blacklist(self):
        for rec in self :
            query = """
                SELECT motif
                FROM hr_blacklist
                WHERE employee_id = %s
                ORDER BY id DESC
                LIMIT 1;
            """ % (rec.id)
            rec.env.cr.execute(query)
            res = rec.env.cr.fetchall()
            if len(res) > 0:
                rec.motif_blacklist = res[0][0]
            else :
                rec.motif_blacklist = ""

    def all_contracts(self):

        return {
            'name': 'Les contrats de ' + self.name,
            'res_model':'hr.contract',
            'view_type': 'list',
            'view_mode': 'list',
            'views': [[False, 'list'], [False, 'form']],
            'type':'ir.actions.act_window',
            'domain': [('employee_id', '=', self.id)],
            }