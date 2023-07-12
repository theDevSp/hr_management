# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class fiche_paie(models.Model):
    _name = "hr.payslip"
    _description = "Fiche de paie"
    _inherit = ['mail.thread','mail.activity.mixin']

    _profile_perso_obj = "hr.profile.paie.personnel"

    name =  fields.Char("Référence", readonly=True, copy=False)
    employee_id = fields.Many2one("hr.employee",string="Employé",required=True)
    contract_id = fields.Many2one("hr.contract", string = "Contrat",required=True)
    type_emp = fields.Selection(related="contract_id.type_emp",string=u"Type d'employé", store=True, readonly=True)
    job_id = fields.Many2one(related="contract_id.job_id", string='Poste', store=True, readonly=True)
    type_profile_related = fields.Selection(related="contract_id.type_profile_related",string=u"Type du profile", required=False, store=True, readonly=True)
    chantier_id = fields.Many2one('fleet.vehicle.chantier',string="Dérnier Chantier",required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Dérnier Code Engin')
    emplacement_chantier_id = fields.Many2one("fleet.vehicle.chantier.emplacement",u"Dérnière Équipe",required=True)
    period_id = fields.Many2one("account.month.period", string = "Période", required = True)
    quinzaine = fields.Selection([('quinzaine1',"Première quinzaine"),('quinzaine2','Deuxième quinzaine'),('quinzaine12','Q1 + Q2')],string="Quinzaine", required = True)
    
    type_fiche = fields.Selection([
        ("payroll","Payement Salaire"),
        ("refund","Rembourssement"),
        ("stc","STC")
        ],"Type de fiche", default="payroll"
    )

    state  = fields.Selection([
        ("draft","Brouillon"),
        ("validee","Validée"),
        ("annulee","Annulée"),
        ("blocked","Bloquée"),
        ],"Status", 
        default="draft",
    )
    
    affich_bonus_jour = fields.Float("Bonus jour", compute="compute_affich_bonus_jour", readonly=True)
    affich_jour_conge = fields.Float("Jour congé", compute="compute_affich_jour_conge", readonly=True)
    
    net_pay = fields.Float('Net à payer', compute="compute_net_a_payer", readonly=True)
    nbr_jour_travaille = fields.Float("Nombre de jours travaillés")
    nbr_heure_travaille = fields.Float("Nombre des heures travaillées")
    date_validation = fields.Date(u'Date de validation', readonly=True)
    salaire_actuel = fields.Float(related="contract_id.salaire_actuel", string='Salaire Actuel', store=True, readonly=True)
    salaire_jour = fields.Float(compute='_compute_salaire_jour',string="Salaire du jour", readonly=True)
    salaire_demi_jour = fields.Float(compute='_compute_salaire_demi_jour',string="Salaire du demi-jour", readonly=True)
    salaire_heure = fields.Float(compute='_compute_salaire_heure',string="Salaire d'heure", readonly=True)
    rapport_id = fields.Many2one("hr.rapport.pointage", string = "Rapport de pointage", readonly=True)
    stc_id = fields.Many2one("hr.stc", string = "STC", required=False)

    jr_travaille_par_chantier = fields.One2many("jr.travaille.par.chantier", 'fiche_paie_id',string='Jours travaillés par chantier', readonly=True)

    @api.model
    def create(self, vals):
        today = datetime.now()
        year = today.year
        month = '{:02d}'.format(today.month)
        fiche_paie_sequence = self.env['ir.sequence'].next_by_code('hr.payslip.sequence')
        vals['name'] =  str(fiche_paie_sequence) + '/' + str(month) + '/' + str(year)   
        res = super(fiche_paie, self).create(vals)
        res.payroll_validation()     
        return res

    def write(self, vals):
        res = super(fiche_paie, self).write(vals)
        self.payroll_validation()
        return res

    @api.depends('employee_id','period_id','contract_id')
    def _compute_salaire_jour(self):
        for rec in self:
            rec.salaire_jour = rec.contract_id.pp_personnel_id_many2one.get_wage_per_day(rec.period_id)

    @api.depends('employee_id','period_id','contract_id')
    def _compute_salaire_demi_jour(self):
        for rec in self:
            rec.salaire_demi_jour = rec.contract_id.pp_personnel_id_many2one.get_wage_per_half_day(rec.period_id)
    
    @api.depends('employee_id','period_id','contract_id')
    def _compute_salaire_heure(self):
        for rec in self:
            rec.salaire_heure = rec.contract_id.pp_personnel_id_many2one.get_wage_per_hour(rec.period_id)

    @api.onchange('employee_id')
    def get_contract_actif(self):
        if self.employee_id:
            self.contract_id = self.employee_id.contract_id

        
    def compute_affich_jour_conge(self):
        self.affich_jour_conge = self.employee_id.panier_conge + self.employee_id.panier_jr_ferie
       
       
    def compute_affich_bonus_jour(self):
        for record in self:
            worked_time = 0
            base_time = 0
            res = 0

            profile_paie_p = record.contract_id.pp_personnel_id_many2one
            type_profile = profile_paie_p.type_profile
            code_profile = profile_paie_p.definition_nbre_jour_worked_par_mois
            worked_days_per_month = profile_paie_p.nbre_jour_worked_par_mois if code_profile == 'nbr_saisie' else record.period_id.get_number_of_days_per_month()
            
            if type_profile == 'j':
                worked_time = record.nbr_jour_travaille
                base_time = profile_paie_p.nbre_jour_worked_par_mois if code_profile == 'nbr_saisie' else 30
            elif type_profile == 'h':
                worked_time = record.nbr_heure_travaille
                base_time = profile_paie_p.nbre_heure_worked_par_jour * worked_days_per_month
            res = worked_time / base_time * 1.5

            if profile_paie_p.periodicity == "m":
                record.affich_bonus_jour = min(res, 1.5)
            else:
                record.affich_bonus_jour = min(res,0.75)  


    @api.depends('nbr_jour_travaille','nbr_heure_travaille','contract_id','salaire_actuel')
    def compute_net_a_payer(self):
        resultat = 0
        for rec in self:
            if rec.contract_id:
                rec.net_pay = rec.nbr_heure_travaille * rec.salaire_heure if rec.type_profile_related == "h" else rec.nbr_jour_travaille * rec.salaire_jour
            else:
                rec.net_pay = 0


    def to_draft(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft'} :
                self.state = 'draft'
                self.date_validation = ""
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )

    def to_validee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'validee','annulee'} :
                self.state = 'validee'
                self.date_validation = datetime.now()
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )
    
    def to_annulee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'annulee'} :
                self.state = 'annulee'
                self.date_validation = ""
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )

    def payroll_validation(self):

        contract_period = self.env['account.month.period'].get_period_from_date(self.contract_id.date_start)
        unique_payroll_per_period = self.env[self._name].search_count([
                                                        ('employee_id', '=', self.employee_id.id),
                                                        ('period_id', '=', self.period_id.id),
                                                        ('quinzaine', '=', self.quinzaine)]) 

        if not self.contract_id or self.period_id.date_stop <= contract_period.date_start:
            raise ValidationError(
                    "Anomalie détectée !!! la période choisie pour le payement ne correspond pas au contrat de l'employé veuillez choisir un contrat convenable."
                )
        
        if unique_payroll_per_period > 0:
            raise ValidationError(
                    "Anomalie d'unicité détectée !!! une fiche de paie existe déja pour la période %s." % self.period_id.name
                )


class loan_list(models.Model):
    _name = "loan.list"

    emprunt_id = fields.Many2one("hr.prelevement",u'Emprunt',readonly=True)
    emprunt_balance = fields.Float(related="emprunt_id.reste_a_paye",string="Reste à payer",readonly=True)
    emprunt_montant = fields.Float(related="emprunt_id.montant_total_prime",string="Montant d'emprunt",readonly=True)
    montant_payer = fields.Float(u"Montant à payer")
    add = fields.Boolean('Ajouter au calcule', default=True)
    note = fields.Char('Observation')
    stc_id = fields.Many2one("hr.stc",u'STC',ondelete='cascade')



class fiche_paie_stc(models.Model):
    _name = "hr.payslip.stc"

    payslip_id = fields.Many2one("hr.payslip",u'Fiche de paie',readonly=True)
    period_id = fields.Many2one("account.month.period", string = "Période", required = True)
    net_pay = fields.Float('Net à payer')
    chantier_id = fields.Many2one('fleet.vehicle.chantier',string="Dernier Chantier")
    emplacement_chantier_id = fields.Many2one("fleet.vehicle.chantier.emplacement",u"Équipe")
    #vehicle = fields.Many2one('fleet.vehicle',string="Dernier Engin", states=READONLY_STATES)
    stc_id = fields.Many2one("hr.stc",u'STC',ondelete='cascade')