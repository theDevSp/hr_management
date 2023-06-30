# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class contrats(models.Model):
    _description = "Contrats"
    _inherit = ['hr.contract']

    name = fields.Char('Référence', readonly=True, copy=False, default='New')
    chantier_id = fields.Many2one('fleet.vehicle.chantier', string = "Chantier")
    profile_paie_id = fields.Many2one('hr.profile.paie', string = "Profile de paie")   
    tt_montant_a_ajouter = fields.Float(string="Montants d'Augmentation", required=True, readonly=True, tracking=True, compute = "_compute_augmentation_montants_valides")
    salaire_actuel = fields.Float('Salaire Prévu',compute = "_compute_salaire", readonly=True)


    type_emp = fields.Selection([("s","Salarié"),("o","Ouvrier")],string=u"Type d'employé",default="s")
    embaucher_par  = fields.Many2one("hr.responsable.chantier",u"Embauché Par")
    recommander_par  = fields.Many2one("hr.responsable.chantier",u"Recommandé Par")
    motif_enbauche  = fields.Selection([("1","Satisfaire un besoin"),("2","Remplacement"),("3","Autre")],u"Motif d'embauche")
    detail_motif = fields.Char('Raison d\'embauche')

    pp_personnel_id_many2one = fields.Many2one('hr.profile.paie.personnel',string = "Profile de paie")

    type_salaire = fields.Selection(
        [("j","Journalier"),
         ("m","Mensuel")],
        string=u"Type Salaire",
        default="m",
        required=True)

    type_profile_related = fields.Selection(related="pp_personnel_id_many2one.type_profile", readonly=False)
    code_profile_related = fields.Char(related="pp_personnel_id_many2one.code", readonly=True)
    nbre_heure_worked_par_demi_jour_related = fields.Float(related="pp_personnel_id_many2one.nbre_heure_worked_par_demi_jour", readonly=False)
    nbre_heure_worked_par_jour_related = fields.Float(related="pp_personnel_id_many2one.nbre_heure_worked_par_jour", readonly=False)
    nbre_jour_worked_par_mois_related = fields.Float(related="pp_personnel_id_many2one.nbre_jour_worked_par_mois", readonly=False)
    definition_nbre_jour_worked_par_mois_related = fields.Selection(related="pp_personnel_id_many2one.definition_nbre_jour_worked_par_mois", readonly=False)
    completer_salaire_related = fields.Boolean(related="pp_personnel_id_many2one.completer_salaire", readonly=False)
    plafonner_bonus_related = fields.Boolean(related="pp_personnel_id_many2one.plafonner_bonus", readonly=False)
    avoir_conge_related = fields.Boolean(related="pp_personnel_id_many2one.avoir_conge", readonly=False)
    period_id_related = fields.Many2one(related="pp_personnel_id_many2one.period_id", readonly=False)
    salaire_jour_related = fields.Float(related="pp_personnel_id_many2one.salaire_jour", readonly=True)
    salaire_demi_jour_related = fields.Float(related="pp_personnel_id_many2one.salaire_demi_jour", readonly=True)
    salaire_heure_related = fields.Float(related="pp_personnel_id_many2one.salaire_heure", readonly=True)
    periodicity_related = fields.Selection(related="pp_personnel_id_many2one.periodicity", readonly=True)
    contract_type = fields.Many2one('hr.contract.type',string = "Types de contrats")
    current_month = fields.Char("Le mois en cours",compute="_compute_current_month")

    _sql_constraints = [
		('name_contract_uniq', 'UNIQUE(name)', 'Cette référence est déjà utilisée.'),
	]

    def _compute_augmentation_montants_valides(self):
        period = self.env['account.month.period'].get_period_from_date(self.date_start) if self.date_start else 0
        query = """
                SELECT case when SUM(montant_valide) is null then 0 else SUM(montant_valide) end as sum
                FROM hr_augmentation 
                WHERE employee_id = %s AND state='acceptee' AND period_id >= %s 
            """ % (self.employee_id.id,period.id)
        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()
        self.tt_montant_a_ajouter = res[0]['sum']

    @api.depends('tt_montant_a_ajouter')
    def _compute_salaire(self):  
        self.salaire_actuel = self.wage + self.tt_montant_a_ajouter 
        
    def to_new(self):
        self.state = 'draft'

    def to_running(self):
        for rec in self :
            contract_ids = self.employee_id.contract_ids
            for rec in contract_ids:
                rec.state = 'cancel'
        self.state = 'open'


    def to_expired(self):
        self.state = 'close'

    def to_cancelled(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie'):
            self.state = 'cancel'

    @api.constrains('wage')
    def _check_wage_superieur_zero(self):
        if self.wage <= 0:
            raise ValidationError("Le Salaire doit être supérieur de la valeur 0.")

            
    @api.model
    def create(self, vals):
        query = """
            SELECT COUNT(*)
            FROM hr_contract
            WHERE employee_id=%s  and (state='draft' or state='open')
            ;
        """ % (vals['employee_id'])
        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()[0]
        if(res['count']==0):
            
            today = datetime.now()
            year = today.year
            month = '{:02d}'.format(today.month)
            contract_sequence = self.env['ir.sequence'].next_by_code('hr.contract.sequence')
            vals['name'] = vals['type_emp'] + '-' + str(month) + '/' + str(year) + '/' + str(contract_sequence)
        else:
            raise ValidationError(
                    "Erreur, Cet employé a déjà un contrat prêt à utilisé."
                )
        return super(contrats, self).create(vals)


    def write(self, vals):
        return super(contrats, self).write(vals)


    def generer_profile(self):
        if self.profile_paie_id :
            champs = {
                "name": self.profile_paie_id.name,
                "code": self.profile_paie_id.code,
                "type_profile": self.profile_paie_id.type_profile,
                "nbre_heure_worked_par_demi_jour": self.profile_paie_id.nbre_heure_worked_par_demi_jour,
                "nbre_heure_worked_par_jour": self.profile_paie_id.nbre_heure_worked_par_jour,
                "nbre_jour_worked_par_mois": self.profile_paie_id.nbre_jour_worked_par_mois,
                "definition_nbre_jour_worked_par_mois": self.profile_paie_id.definition_nbre_jour_worked_par_mois,
                "completer_salaire": self.profile_paie_id.completer_salaire,    
                "plafonner_bonus": self.profile_paie_id.plafonner_bonus,    
                "avoir_conge": self.profile_paie_id.avoir_conge,    
                "period_id": self.profile_paie_id.period_id.id,    
                "salaire_mois": self.salaire_actuel,
                "contract_id": self.id,
                "periodicity": self.periodicity_related   
                }
            obj = self.env['hr.profile.paie.personnel'].create(champs)
            self.pp_personnel_id_many2one = obj
        else:
           raise ValidationError(
                    "Erreur, Vous devez séléctionner un profil de paie pour le générer."
                )
        return True
    
    def _compute_current_month(self):
        today = datetime.now()
        year = today.year
        month = '{:02d}'.format(today.month)
        self.current_month = str(month) + "/" + str(year)

    
    def get_hours_per_day(self,hours):
        demi_jour = 0

        if self.profile_paie_id:
            demi_jour = self.nbre_heure_worked_par_demi_jour_related 
        elif self.employee_id.type_emp == 'o': 
            demi_jour = 6
        else:
            demi_jour = 4.5
        
        if float(hours) > 0 and float(hours) <= demi_jour:
            j_travaille = '0.5'
        elif float(hours) > demi_jour  and float(hours)<= 24:
            j_travaille = '1'
        else :
            j_travaille = '0'

        return j_travaille 

