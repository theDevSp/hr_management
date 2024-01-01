from odoo import fields, models, api
from odoo.osv import expression
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
from lxml import etree
from odoo.exceptions import ValidationError
import re

class hr_employee(models.Model):
    _description = "Employee"
    _order = 'name'
    _inherit = ['hr.employee']
    _mail_post_access = 'read'

    cin = fields.Char('CIN', required=True)

    @api.constrains('cin')
    def _check_cin(self):
        
        if not self.cin.isalnum():
            raise ValidationError("Erreur : Format incorrect. Aucun espace ou caractère spécial n'est accepté ; seuls les chiffres et les lettres le sont.")
        
        if not self._contains_letter_and_number(self.cin):
            raise ValidationError("Erreur : Format incorrect. Le N° CIN doit impérativement comporter à la fois au moins une lettre et un chiffre pour être valide.")

        for record in self:
            if record.cin:
                duplicate_records = self.search([('cin', '=', self._correct_cin_format(record.cin).upper())])
                if len(duplicate_records) > 1:
                    raise ValidationError("Erreur : N° CIN unique. Le numéro de CIN %s est déjà associé à un autre employé."%(self.cin.upper()))

    
    def _correct_cin_format(self,input_string):
        # Using list comprehension to filter out non-alphanumeric characters
        filtered_string = ''.join([char for char in input_string if char.isalnum()])
        return filtered_string
    
    def _contains_letter_and_number(self,input_string):
        # Regular expressions to check for at least one letter and one number
        letter_pattern = re.compile(r'[a-zA-Z]')
        number_pattern = re.compile(r'[0-9]')

        # Check if the string contains at least one letter and one number
        has_letter = bool(re.search(letter_pattern, input_string))
        has_number = bool(re.search(number_pattern, input_string))

        if has_letter and has_number:
            return True
        
        return False
                
    cnss = fields.Char('N° CNSS')

    @api.constrains('cnss')
    def _check_cnss(self):
        
        if self.cnss and not self.cnss.isdigit():
            raise ValidationError("Erreur : Format incorrect. Le N° CNSS doit exclusivement contenir des chiffres pour être considérée comme valide.")
        
    title_id = fields.Many2one("res.partner.title","Titre")
    bank = fields.Many2one("bank","Banque")
    ville_bank = fields.Many2one("city",u"Ville")
    bank_agence = fields.Char(u"Agence")
    adress_personnel = fields.Char(u'Adresse personnel')
    bank_account = fields.Char(u'N° RIB', size=24)
    rib_number = fields.Many2one("employee.rib",u'N° RIB',domain="[('employee_id', '=', id)]")
    bank_related = fields.Many2one(related='rib_number.bank')
    ville_bank_related = fields.Many2one(related='rib_number.ville_bank')
    bank_agence_related = fields.Char(related='rib_number.bank_agence')
    job = fields.Char("Fonction")
    diplome = fields.Char(u"Diplôme")
    obs_embauche  = fields.Char(u"Observation")
    employee_age = fields.Integer(u"Âge",compute="_compute_age")
    date_naissance = fields.Date(u"Date Naissance")
    lieu_naissance = fields.Char(u"Lieu Naissance")
    
    cotisation = fields.Boolean("Activer Cotisation-CIMR")
    montant_cimr = fields.Float(u"Montant Cotisation CIMR")
    
    vehicle_id = fields.Many2one("fleet.vehicle",u"Code engin",tracking=True)

    remaining_days = fields.Char(compute="_compute_remaining_days",string='Jours Restants')
    date_cin = fields.Date(u'Date validité CIN')
    phone1 = fields.Char(u"Tél. Portable 1")
    phone2 = fields.Char(u"Tél. Portable 2")
    phone3 = fields.Char(u"Tél. Portable 3")
    working_years = fields.Char(compute='_compute_working_years',string="Ancienneté")
    currency_f = fields.Many2one('res.currency', string='Currency')
    
    wage_jour = fields.Float(string='Salaire Journalier')
    state_employee_wtf = fields.Selection([("new","Nouveau Embauche"),("transfert","Transfert"),("active","Active"),("stc","STC")],u"Situation Employé",index=True, copy=False, default='new', tracking=True)
    active = fields.Boolean('Active', related='resource_id.active', default=True, store=True, readonly=False)
    chantier_id  = fields.Many2one("fleet.vehicle.chantier",u"Chantier")
    emplacement_chantier_id = fields.Many2one("fleet.vehicle.chantier.emplacement",u"Équipe")
    company_id = fields.Many2one('res.company', 'Company', required=True,default=1)
    nombre_enfants = fields.Integer(u"Nombre d'enfants")
    responsable_id = fields.Many2one("hr.responsable.chantier","Responsable")
    black_list = fields.Boolean("Liste Noire", readonly=True, default=False)
    blacklist_histo = fields.One2many('hr.blacklist', 'employee_id',readonly=True)
    motif_blacklist = fields.Char("Motif Blacklist", compute = "_compute_motif_blacklist")


    @api.model
    def fields_view_get(self,view_id=None, view_type='tree',toolbar=False, submenu=False):
        res = super(hr_employee, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=False)
        group_admin = self.env.user.has_group('hr_management.group_admin_paie')
        group_agent_paie = self.env.user.has_group('hr_management.group_agent_paie')
        update = view_type in ['form', 'tree']
        doc = etree.XML(res['arch'])
        if not group_admin and not group_agent_paie:
            if update:
                for node in doc.xpath("//"+view_type):
                    node.set('create', '0')
                res['arch'] = etree.tostring(doc)
        return res

    type_emp = fields.Selection(related="contract_id.type_emp",string=u"Type d'employé", required=False, store=True)
    job_id = fields.Many2one(related="contract_id.job_id", string='Poste', store=True)
    embaucher_par  = fields.Many2one(related="contract_id.embaucher_par", string = "Embauché Par", store=True)
    recommander_par  = fields.Many2one(related="contract_id.recommander_par", string="Recommandé Par", store=True)
    motif_enbauche  = fields.Selection(related="contract_id.motif_enbauche", string="Motif d'embauche", store=True)

    date_start = fields.Date(related="contract_id.date_start",string='Date de début', required=False)
    date_end = fields.Date(related="contract_id.date_end",string='Date de fin', required=False)
    chantier_related = fields.Many2one(related="contract_id.chantier_id",string='Chantier', required=False)
    type_contrat = fields.Many2one(related="contract_id.contract_type",string='Type du contrat', required=False)
    wage = fields.Monetary(related="contract_id.wage",string='Salaire de base', required=False, tracking=True, currency_field = "currency_f")
    salaire_actuel = fields.Float(related="contract_id.salaire_actuel",string='Salaire Actuel', required=False, tracking=True)
    pp_personnel_id_many2one = fields.Many2one(related="contract_id.pp_personnel_id_many2one",string='Profile de paie')
    periodicity_related = fields.Selection(related="contract_id.periodicity_related",string='Périodicité')

    name_profile_related = fields.Char(related="pp_personnel_id_many2one.name", readonly=True)
    code_profile_related = fields.Char(related="pp_personnel_id_many2one.code", readonly=True)
    type_profile_related = fields.Selection(related="pp_personnel_id_many2one.type_profile", readonly=True)
    nbre_heure_worked_par_demi_jour_related = fields.Float(related="pp_personnel_id_many2one.nbre_heure_worked_par_demi_jour", readonly=True)
    nbre_heure_worked_par_jour_related = fields.Float(related="pp_personnel_id_many2one.nbre_heure_worked_par_jour", readonly=True)
    nbre_jour_worked_par_mois_related = fields.Float(related="pp_personnel_id_many2one.nbre_jour_worked_par_mois", readonly=True)
    definition_nbre_jour_worked_par_mois_related = fields.Selection(related="pp_personnel_id_many2one.definition_nbre_jour_worked_par_mois", readonly=True)
    completer_salaire_related = fields.Boolean(related="pp_personnel_id_many2one.completer_salaire", readonly=True)
    plafonner_bonus_related = fields.Boolean(related="pp_personnel_id_many2one.plafonner_bonus", readonly=True)
    avoir_conge_related = fields.Boolean(related="pp_personnel_id_many2one.avoir_conge", readonly=True)
    payed_holidays_related = fields.Boolean(related="pp_personnel_id_many2one.payed_holidays", readonly=False)
    justification_related = fields.Boolean(related="pp_personnel_id_many2one.justification", readonly=False)
    saved_holidays_related = fields.Boolean(related="pp_personnel_id_many2one.saved_holidays", readonly=False)
    jo_related = fields.Boolean(related="pp_personnel_id_many2one.jo", readonly=False)
    autoriz_zero_cp_related = fields.Boolean(related="pp_personnel_id_many2one.autoriz_zero_cp", readonly=False)
    period_id_related = fields.Many2one(related="pp_personnel_id_many2one.period_id", readonly=True)
    salaire_jour_related = fields.Float(related="pp_personnel_id_many2one.salaire_jour", readonly=True)
    salaire_demi_jour_related = fields.Float(related="pp_personnel_id_many2one.salaire_demi_jour", readonly=True)
    salaire_heure_related = fields.Float(related="pp_personnel_id_many2one.salaire_heure", readonly=True)

    panier_conge = fields.Float("Panier de congé",compute='_compute_panier_conge')
    panier_jr_ferie = fields.Float("Panier des jours fériés", compute='_compute_panier_jr_ferie')
    panier_dimanches = fields.Float("Panier des dimanches", compute='_compute_panier_dimanches')

    nbr_contrats = fields.Integer("Les contrats",compute="count_smart_button")
    nbr_augmentations = fields.Integer("Les augmentations",compute="count_smart_button")
    nbr_primes = fields.Integer("Les primes",compute="count_smart_button")
    nbr_prelevements = fields.Integer("Les prélévements",compute="count_smart_button")
    nbr_credits = fields.Integer("Les crédits",compute="count_smart_button")
    nbr_holidays = fields.Integer("Les congés",compute="count_smart_button")
    nbr_fiches_de_paie = fields.Integer("Les fiches de paie",compute="count_smart_button")
    nbr_stc = fields.Integer("Les stc",compute="count_smart_button")
    nbr_rapports_pointage = fields.Integer("Les rapports de pointage",compute="count_smart_button")

    having_contrat = fields.Integer("Having contrat?",compute='compute_having_contrat')

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

    def get_working_years_in_days(self,date):
        start_woring_year = fields.Date.from_string(self.contract_id.date_start)
        return relativedelta(date, start_woring_year).years * 12 + relativedelta(date, start_woring_year).months + relativedelta(date, start_woring_year).days/30

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
    def create(self,vals):
<<<<<<< HEAD
=======

        print("Valsss ",vals)

        res_char = []
        char = "".join(re.split("[^a-zA-Z]*", vals['cin']))
        num = "".join(re.split("[^0-9]*", vals['cin']))
        res_char.append("position('%s' in lower(cin))>0 and position('%s' in lower(cin))>0 or " % (char.lower(),num))

        
        if vals['cin']:
            query = """
                    select id from hr_employee where 
                """ 
            for res in res_char:
                query += res
            query = query[:len(query) - 3]
            
            self.env.cr.execute(query)
            if len(self.env.cr.fetchall()) > 0:
                raise ValidationError(
                    "Erreur, Un Employée avec le N° CIN %s existe déjà"%(vals['cin'].upper())
                )        
            vals['cin'] = vals['cin'].upper()
>>>>>>> origin/Dev-Mostafa

        if vals.get('cin'):
            vals['cin'] = self._correct_cin_format(vals['cin']).upper()
        vals['state_employee_wtf'] ='new'
        return super(hr_employee,self).create(vals)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('cin', operator, name), '|',('name', operator, name),('cnss', operator, name)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
    
    def name_get(self):
        result = []
        for employee in self:
            name = employee.cin + ' - ' + employee.name
            result.append((employee.id, name))
        return result

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


    def _compute_panier_conge(self):
        for rec in self :
            rec.panier_conge = 0
            if rec.contract_id:
                period_debut_contrat = self.env['account.month.period'].get_period_from_date(rec.contract_id.date_start) if rec.contract_id else 0
                rec.panier_conge =  self.env['hr.allocations'].get_sum_allocation(rec,False,period_debut_contrat)
                

    def _compute_panier_jr_ferie(self):
        for rec in self :
            rec.panier_jr_ferie = 0
            if rec.contract_id:
                period_debut_contrat = self.env['account.month.period'].get_period_from_date(rec.contract_id.date_start) if rec.contract_id else 0
                rec.panier_conge =  self.env['hr.allocations'].get_sum_allocation(rec,False,period_debut_contrat,is_jf = True)


    def _compute_panier_dimanches(self):
        for rec in self :
            rec.panier_dimanches = 0
            if rec.contract_id:
                period_debut_contrat = self.env['account.month.period'].get_period_from_date(rec.contract_id.date_start) if rec.contract_id else 0
                rec.panier_conge =  self.env['hr.allocations'].get_sum_allocation(rec,False,period_debut_contrat,is_dimanche = True)



    def all_contracts(self):

        tree_id = self.env.ref('hr_management.contrats_nouveaux_tree').id
        form_id = self.env.ref('hr_management.contrats_nouveaux_view_form').id

        return {
            'name': 'Les contrats de ' + self.name,
            'res_model':'hr.contract',
            'view_mode': 'list,form',
            'views': [(tree_id, 'tree'),(form_id,'form')],
            'type':'ir.actions.act_window',
            'domain': [('employee_id', '=', self.id)],
            }
    
    def all_augmentations(self):

        tree_id = self.env.ref('hr_management.augmentation_par_employee_tree_view').id
        form_id = self.env.ref('hr_management.augmentation_formulaire').id

        return {
            'name': 'Les augmentations de ' + self.name,
            'res_model':'hr.augmentation',
            'view_mode': 'list,form',
            'views': [(tree_id, 'tree'),(form_id,'form')],
            'type':'ir.actions.act_window',
            'domain': [('employee_id', '=', self.id)],
            }
    
    def all_primes(self):

        tree_id = self.env.ref('hr_management.prime_par_employee_tree_view').id
        form_id = self.env.ref('hr_management.prime_view_form').id

        return {
            'name': 'Les primes de ' + self.name,
            'res_model':'hr.prime',
            'view_mode': 'list,form',
            'views': [(tree_id, 'tree'),(form_id,'form')],
            'type':'ir.actions.act_window',
            'domain': [('employee_id', '=', self.id)],
            }
    
    def all_prelevements(self):

        tree_id = self.env.ref('hr_management.prelevement_par_employee_tree_view').id
        form_id = self.env.ref('hr_management.prelevement_view_form').id

        return {
            'name': 'Les prélèvements de ' + self.name,
            'res_model':'hr.prelevement',
            'view_mode': 'list,form',
            'views': [(tree_id, 'tree'),(form_id,'form')],
            'type':'ir.actions.act_window',
            'domain': [('employee_id', '=', self.id),('is_credit', "!=", 'True')],
            }

    def all_credits(self):

        tree_id = self.env.ref('hr_management.credit_par_employee_tree_view').id
        form_id = self.env.ref('hr_management.credit_view_form').id

        return {
            'name': 'Les crédits de ' + self.name,
            'res_model':'hr.prelevement',
            'view_mode': 'list,form',
            'views': [(tree_id, 'tree'),(form_id,'form')],
            'type':'ir.actions.act_window',
            'domain': [('employee_id', '=', self.id),('is_credit', "=", 'True')],
            }

    def all_conges(self):

        tree_id = self.env.ref('hr_management.holidays_par_employee_tree').id
        form_id = self.env.ref('hr_management.holidays_formulaire').id

        return {
            'name': 'Les congés de ' + self.name,
            'res_model':'hr.holidays',
            'view_mode': 'list,form',
            'views': [(tree_id, 'tree'),(form_id,'form')],
            'type':'ir.actions.act_window',
            'domain': [('employee_id', '=', self.id)],
            }
    

    def all_fiche_paie(self):

        tree_id = self.env.ref('hr_management.fiche_paie_par_employee_tree').id
        form_id = self.env.ref('hr_management.fiche_paie_formulaire').id

        return {
            'name': 'Les fiches de paie de ' + self.name,
            'res_model':'hr.payslip',
            'view_mode': 'list,form',
            'views': [(tree_id, 'tree'),(form_id,'form')],
            'type':'ir.actions.act_window',
            'domain': [('employee_id', '=', self.id)],
            }

    def all_stc(self):
        tree_id = self.env.ref('hr_management.stc_par_employee_tree_view').id
        form_id = self.env.ref('hr_management.view_stc_form').id

        return {
            'name': 'Les STC de ' + self.name,
            'res_model':'hr.stc',
            'view_mode': 'list,form',
            'views': [(tree_id, 'tree'),(form_id,'form')],
            'type':'ir.actions.act_window',
            'domain': [('employee_id', '=', self.id)],
            }

    def all_rapports_pointage(self):
        tree_id = self.env.ref('hr_management.rapport_pointage_tree').id
        form_id = self.env.ref('hr_management.rapport_pointage_form').id

        return {
            'name': 'Les rapports de pointage de ' + self.name,
            'res_model':'hr.rapport.pointage',
            
            'view_mode': 'list,form',
            'views': [(tree_id, 'tree'),(form_id,'form')],
            'type':'ir.actions.act_window',
            'domain': [('employee_id', '=', self.id)],
            }

    def to_new(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            self.state_employee_wtf = 'new'
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )

    def to_active(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            self.state_employee_wtf = 'active'
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )

    def to_stc(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            self.state_employee_wtf = 'stc'
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )
        
    
    def count_smart_button(self):
        for rec in self :
            query = """
                    SELECT
                        (SELECT COUNT(*) FROM hr_contract WHERE employee_id = %s) AS contract_count,
                        (SELECT COUNT(*) FROM hr_augmentation WHERE employee_id = %s) AS augmentation_count,
                        (SELECT COUNT(*) FROM hr_prime WHERE employee_id = %s) AS prime_count,
                        (SELECT COUNT(*) FROM hr_prelevement WHERE employee_id = %s AND is_credit = false) AS prelevement_count,
                        (SELECT COUNT(*) FROM hr_prelevement WHERE employee_id = %s AND is_credit = true) AS credit_count,
                        (SELECT COUNT(*) FROM hr_holidays WHERE employee_id = %s) AS holiday_count,
                        (SELECT COUNT(*) FROM hr_payslip WHERE employee_id = %s) AS payslip_count,
                        (SELECT COUNT(*) FROM hr_stc WHERE employee_id = %s) AS stc_count,
                        (SELECT COUNT(*) FROM hr_rapport_pointage WHERE employee_id = %s) AS pointage_count;
                    
                    """%(rec.id,rec.id,rec.id,rec.id,rec.id,rec.id,rec.id,rec.id,rec.id)
        
            rec.env.cr.execute(query)
            res = rec.env.cr.dictfetchall()
            
            rec.nbr_contrats = res[0]['contract_count'] 
            rec.nbr_augmentations = res[0]['augmentation_count']
            rec.nbr_primes = res[0]['prime_count']
            rec.nbr_prelevements = res[0]['prelevement_count']
            rec.nbr_credits = res[0]['credit_count']
            rec.nbr_holidays = res[0]['holiday_count']
            rec.nbr_fiches_de_paie = res[0]['payslip_count']
            rec.nbr_stc = res[0]['stc_count']
            rec.nbr_rapports_pointage = res[0]['pointage_count']

    
    def creatiion_individuel_rapport_pointage(self):
        
        view = self.env.ref(
            'hr_management.creation_individuel_wizard')
        
        return {
            'name': ('Création pointage pour %s' % str(self.name)),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.filtre.pointage.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context':{
                'default_employee_id':self.id,
                'default_employee_type':self.type_emp
            }
        }
    
    def compute_having_contrat(self):
        if self.contract_id:
            self.having_contrat = 1
        else:
            self.having_contrat = 0

    def ajouter_contrat(self):
        view = self.env.ref('hr_management.contrats_nouveaux_view_form')
        return {
            'name': ("Ajouter un contrat à : \"" + str(self.name) + "\""),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.contract',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context' : {
                    'default_employee_id': self.id,
                    'default_chantier_id': self.chantier_id.id,
                },
        }
    
    def check_cin(input_string):
        # Using list comprehension to filter out non-alphanumeric characters
        filtered_string = ''.join([char for char in input_string if char.isalnum()])
        return filtered_string
