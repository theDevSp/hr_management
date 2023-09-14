# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime

class fiche_paie(models.Model):
    _name = "hr.payslip"
    _description = "Fiche de paie"
    _inherit = ['mail.thread','mail.activity.mixin']

    _profile_perso_obj = "hr.profile.paie.personnel"

    name =  fields.Char("Référence", readonly=True, copy=False)
    employee_id = fields.Many2one("hr.employee",string="Employé",required=True)
    working_years = fields.Char(related="employee_id.working_years",string="Ancienneté",readonly=True)
    contract_id = fields.Many2one("hr.contract", string = "Contrat",required=True)
    type_emp = fields.Selection(related="contract_id.type_emp",string=u"Type d'employé", store=True, readonly=True)
    job_id = fields.Many2one(related="contract_id.job_id", string='Poste', store=True, readonly=True)
    type_profile_related = fields.Selection(related="contract_id.type_profile_related",string=u"Type du profile", readonly=True)
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
        ("cal","Calculée"),
        ("approuved","Clôturé"),
        ("done","Payée"),
        ("annulee","Annulée"),
        ("blocked","Bloquée"),
        ],"Status", 
        default="draft",
    )

    cal_state = fields.Boolean('cal_state',default=False)
    
    affich_bonus_jour = fields.Float("Bonus jour", compute="_compute_affich_bonus_jour", readonly=True)
    affich_jour_conge = fields.Float("Panier congé", compute="_compute_panier", readonly=True, store=True)
    affich_jour_dimanche_conge = fields.Float("Panier dimanche", compute="_compute_panier", readonly=True, store=True)
    affich_jour_dimanche = fields.Float(related="rapport_id.count_nbr_dim_days",string="Dimanches Travailés")
    affich_jour_ferier = fields.Float(related="rapport_id.count_nbr_ferier_days",string="JF Travailés")
    affich_conge = fields.Float(related="rapport_id.count_nbr_holiday_days",string="Congé Payée")
    affich_jour_absence = fields.Float(related="rapport_id.count_nbr_absense_days",string="Absence")
    
    addition = fields.Float('Total Avantage',compute="_compute_total_addition",store=True)
    deduction = fields.Float('Total Déduction',compute="_compute_total_deduction",store=True)
    net_pay = fields.Float('Net à payer', compute="compute_net_a_payer", readonly=True)
    nbr_jour_travaille = fields.Float("Nombre de jours travaillés")
    nbr_heure_travaille = fields.Float("Nombre des heures travaillées")
    date_validation = fields.Date(u'Date de validation', readonly=True)
    salaire_actuel = fields.Float(related="contract_id.salaire_actuel", string='Salaire Actuel', store=True, readonly=True)
    salaire_jour = fields.Float(compute='_compute_salaire_jour',string="Salaire du jour", readonly=True)
    salaire_demi_jour = fields.Float(compute='_compute_salaire_demi_jour',string="Salaire du demi-jour", readonly=True)
    salaire_heure = fields.Float(compute='_compute_salaire_heure',string="Salaire d'heure", readonly=True)
    rapport_id = fields.Many2one("hr.rapport.pointage", string = "Rapport de pointage", readonly=True)
    stc_id = fields.Many2one("hr.stc", string = "STC", readonly=True)

    jr_travaille_par_chantier = fields.One2many("jr.travaille.par.chantier", 'fiche_paie_id',string='Jours travaillés par chantier')
    jr_par_prime = fields.One2many("days.per.addition", 'payroll_id',string='Jours par prime')

    notes = fields.Html('Notes')

    net_paye_archive = fields.Float('Net à Payer')
    new = fields.Boolean('field_name',default=False)

    @api.model
    def create(self, vals):
        today = datetime.now()
        year = today.year
        month = '{:02d}'.format(today.month)
        fiche_paie_sequence = self.env['ir.sequence'].next_by_code('hr.payslip.sequence')
        vals['name'] =  str(fiche_paie_sequence) + '/' + str(month) + '/' + str(year)   
        self.payroll_validation(vals['contract_id'],vals['period_id'])  
        self.unique_payroll_validation(vals['employee_id'],vals['period_id'],vals['quinzaine'])   
        return super(fiche_paie, self).create(vals)

    def write(self, vals):
        res = super(fiche_paie, self).write(vals)
        self.payroll_validation(self.contract_id.id,self.period_id.id) 
        if vals.get('cal_state') and self.cal_state == True:
            self.write({
                'state':'cal'
            })
        
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
    
    @api.depends('employee_id','period_id','contract_id')
    def _compute_panier(self):
        for rec in self:
            contract_period = self.env['account.month.period'].get_period_from_date(rec.contract_id.date_start)
            rec.affich_jour_conge = self.env['hr.allocations'].get_sum_allocation(rec.employee_id,rec.period_id,contract_period) if rec.employee_id and rec.period_id else 0
    
    @api.depends('employee_id','period_id','contract_id')
    def _compute_panier_dimanche(self):
        for rec in self:
            contract_period = self.env['account.month.period'].get_period_from_date(rec.contract_id.date_start)
            rec.affich_jour_conge = self.env['hr.allocations'].get_sum_allocation(rec.employee_id,rec.period_id,contract_period) if rec.employee_id and rec.period_id else 0
            rec.affich_jour_dimmanche_conge = self.env['hr.allocations'].get_sum_allocation(rec.employee_id,rec.period_id,contract_period,True) if rec.employee_id and rec.period_id else 0
    
    @api.depends('cal_state')
    def _compute_total_addition(self):
        for rec in self:
            res = 0
            if rec.employee_id and rec.period_id and rec.quinzaine != 'quinzaine1' and rec.cal_state:
                query = """
                    SELECT pl.montant_a_payer as amount,COALESCE(pt.payement_condition,0) as condition,p.date_fait as date_start
                    FROM hr_paiement_ligne pl
                    INNER JOIN hr_prime p ON pl.prime_id = p.id
                    INNER JOIN hr_prime_type pt ON p.type_prime = pt.id
                    WHERE pt.type_payement = 'm' and (p.employee_id = %s or p.employee_id is null) 
                    and p.state = 'validee' and pl.period_id = %s and pl.state = 'non_paye'

                    UNION

                    SELECT dp.jour_prime * p.montant_total_prime,0,current_date
                    FROM days_per_addition dp
                    INNER JOIN hr_prime p ON dp.prime_id = p.id
                    INNER JOIN hr_prime_type pt ON p.type_prime = pt.id
                    WHERE pt.type_payement = 'j' and pt.type_addition = 'perio' and (p.employee_id = %s or p.employee_id is null) 
                    and p.state = 'validee' and p.first_period_id = %s and dp.payroll_id = %s
                    
                """ %(rec.employee_id.id,rec.period_id.id,rec.employee_id.id,rec.period_id.id,rec.id)
                rec.env.cr.execute(query)
                for prime in rec.env.cr.dictfetchall():
                    if rec.employee_id.get_working_years_in_days(prime['date_start']) >= prime['condition']:
                        res += prime['amount']
                #res = rec.env.cr.dictfetchall()[0]['tt']
            rec.addition = res 

    @api.depends('cal_state')
    def _compute_total_deduction(self):
        for rec in self:
            res = 0
            if rec.employee_id and rec.period_id and rec.quinzaine != 'quinzaine1' and rec.cal_state:
                query = """
                    SELECT COALESCE(sum(pl.montant_a_payer),0) as tt
                    FROM hr_paiement_prelevement pl
                    INNER JOIN hr_prelevement p ON pl.prelevement_id = p.id
                    WHERE p.state = 'validee' and p.employee_id = %s and pl.period_id = %s and pl.state = 'non_paye';
                """ %(rec.employee_id.id,rec.period_id.id)
                rec.env.cr.execute(query)
                res = rec.env.cr.dictfetchall()[0]['tt']
            rec.deduction = res 
            
    @api.onchange('employee_id')
    def get_contract_actif(self):
        if self.employee_id:
            self.contract_id = self.employee_id.contract_id

    def _compute_affich_bonus_jour(self):
        
        for record in self:
            worked_time = 0
            base_time = 0
            res = 0

            profile_paie_p = record.contract_id.pp_personnel_id_many2one
            type_profile = profile_paie_p.type_profile
            code_profile = profile_paie_p.definition_nbre_jour_worked_par_mois
            worked_days_per_month = profile_paie_p.nbre_jour_worked_par_mois if code_profile == 'nbr_saisie' else record.period_id.get_number_of_days_per_month()
            record.affich_bonus_jour = 0
            
            if profile_paie_p:
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


    @api.depends('nbr_jour_travaille','nbr_heure_travaille','contract_id','salaire_actuel','addition','deduction')
    def compute_net_a_payer(self):
        resultat = 0
        for rec in self:
            if rec.contract_id:
                rec.net_pay = rec.nbr_heure_travaille * rec.salaire_heure if rec.type_profile_related == "h" else rec.nbr_jour_travaille * rec.salaire_jour
                rec.net_pay +=  (rec.addition - rec.deduction) 
            else:
                rec.net_pay = 0


    def to_draft(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft'} :
                self.state = 'draft'
                self.date_validation = ""
                self.cal_state = False
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )

    def to_done(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state == 'cal' :
                self.state = 'done'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )
    
    def reset(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state == 'cal' :
                self.state = 'validee'
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
    
    def block(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state in {'cal','done'} :
                self.state = 'blocked'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )
    
    def unblock(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            self.state = 'cal'
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )

    def payroll_validation(self,contract_id,period_id):

        contract_period = self.env['account.month.period'].get_period_from_date(self.env['hr.contract'].browse(contract_id).date_start)

        if self.env['account.month.period'].browse(period_id).date_stop <= contract_period.date_start:
            raise ValidationError(
                    "Anomalie détectée !!! la période choisie pour le payement ne correspond pas au contrat de l'employé veuillez choisir un contrat convenable."
                )
        
    def unique_payroll_validation(self,employee_id,period_id,quinzaine):

        unique_payroll_per_period = self.env[self._name].search_count([
                                                        ('employee_id', '=', employee_id),
                                                        ('period_id', '=', period_id),
                                                        ('quinzaine', '=', quinzaine)]) 
        if unique_payroll_per_period > 0:
            raise ValidationError(
                    "Anomalie d'unicité détectée !!! une fiche de paie existe déja pour la période %s." % self.env['account.month.period'].browse(period_id).name
                )

    def update_cal_state(self):
        self.cal_state = not self.cal_state
    
    def open_payslip(self):
        view = self.env.ref('hr_management.fiche_paie_formulaire')

        return {
            'name': ("Fiche de paie %s " % self.name),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.payslip',
            'res_id': self.id,
            'views': [(view.id, 'form')],
            'view_id': view.id,
        }


class days_per_addition(models.Model):
    
    _name = "days.per.addition"

    prime_id = fields.Many2one('hr.prime', string='prime')
    payroll_id = fields.Many2one('hr.payslip', string='payroll')
    jour_prime = fields.Float("Jour Prime") # ce champs didié pour sauvegarder les jours à payer d'un prime journalier exemple hrira
    is_cal = fields.Boolean('calculé',default=False)
    observations = fields.Text("Observations")



    