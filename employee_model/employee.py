from odoo import fields, models, api
from datetime import date

class hr_employee(models.Model):
    _description = "Employee"
    #_order = 'name'
    _inherit = ['hr.employee']
    #_inherit = ['hr.employee', 'mail.thread', 'mail.activity.mixin', 'resource.mixin', 'avatar.mixin']
    #_mail_post_access = 'read'

    cin = fields.Char('CIN', required=True)
    is_salary = fields.Boolean("Is Employee?")
    ### employee_type = fields.Selection([("employee1","Salarié"),("employee2","Ouvrier")],string=u"Type d'employé",default="employee1")
    #title_id = fields.Many2one("res.partner.title","Titre")
    #bank = fields.Many2one("bank","Banque")
    ville_bank = fields.Char(u"Ville")
    bank_agence = fields.Char(u"Agence")

    adress_personnel = fields.Char(u'Adresse personnel')
    bank_account = fields.Char(u'N° RIB')
    #property_bank_account = fields.Many2one(required=False)
    #employee_account = fields.Many2one(required=False)
    #salary_account = fields.Many2one(required=False)

    job = fields.Char("Fonction")
    bool_company = fields.Boolean("Cofabri-bitumes")
    cotisation = fields.Boolean("Activer Cotisation-CIMR")
    black_list = fields.Boolean("Liste Noire")
    motif_ln   = fields.Text("Motif Liste Noire")
    diplome = fields.Char(u"Diplôme")

    # Ces champs doivent etre de la table "hr.employee" ou "hr.employee.new"
    #embaucher_par  = fields.Many2one("hr.employee",u"Embaucher Par")
    #recommander_par  = fields.Many2one("hr.employee",u"Recommander Par")

    motif_enbauche  = fields.Selection([("1","Satisfaire un besoin"),("2","Remplacement"),("3","Autre")],u"Motif d'embauche")
    obs_embauche  = fields.Char(u"Observation")
    employee_age = fields.Integer(u"Âge",compute="_compute_age")
    
    date_naissance = fields.Date(u"Date Naissance")
    lieu_naissance = fields.Char(u"Lieu Naissance")
    
    montant_cimr = fields.Float(u"Montant Cotisation CIMR")
   # nbr_jour_ferie = fields.Float(u"Nombre de Jours Fériés",compute="_compute_jf")
   # date_start = fields.Date(related="contract_id.date_start",string='Date Debut')
   # date_end = fields.Date(related="contract_id.date_end",string='Date Fin')
    #remaining_days = fields.Char(compute="_compute_remaining_days",string='Jours Restant')
   # wage = fields.Float(related="contract_id.wage",string='Salaire')
    date_cin = fields.Date(u'Date validité CIN')
    phone1 = fields.Char(u"Tél. Portable 1")
    phone2 = fields.Char(u"Tél. Portable 2")
    phone3 = fields.Char(u"Tél. Portable 3")
    #payslip_count = fields.Integer(compute='_compute_payslip')
    #working_years = fields.Char(compute='_compute_working_years',string="Ancienneté")
    #wage_jour = fields.Float(compute='_compute_salaire_jour',string='Salaire Journalier')
    panier_done = fields.Boolean('Panier régler')
    state_employee_wtf = fields.Selection([("new","Nouveau Embauche"),("transfert","Transfert"),("active","Active"),("stc","STC")],u"Situation Employée")


    #profile_paie = fields.Many2one(related="contract_id.function.function_id",string='Profile de Paie')
    #chantier_affect = fields.One2many("hr.employee.affectation.chantier","employee_id",string="Affectation Chantier")
    #company_id = fields.Many2one('res.company', 'Company', required=True,default=1)


    #@api.multi
    def _compute_age(self):
        for employee in self:
            if employee.date_naissance:
                today = date.today() 
                birthDate = fields.Date.from_string(employee.date_naissance)
                age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
                employee.employee_age = age       

    #@api.multi
    #def _compute_jf(self):  
    #    for employee in self:  
    #        if employee:
    #            attributions = self.env['hr.holidays'].search([('employee_id','=',employee.id),('holiday_status_id','=',9)]) 
    #            employee.nbr_jour_ferie = sum([line.number_of_days_temp for line in attributions])      