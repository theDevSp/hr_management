# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class contrats(models.Model):
    _description = "Contrats"
    _inherit = ['hr.contract']

    name = fields.Char('Contract Name', readonly=True, copy=False, default='New')
    chantier_id = fields.Many2one('fleet.vehicle.chantier', string = "Chantier")
    profile_paie_id = fields.Many2one('hr.profile.paie', string = "Profile de paie")
        
    currency_id = fields.Many2one('res.currency', string = 'Symbole Monétaire')
    tt_montant_a_ajouter = fields.Monetary(string='Montans Validés', required=True, tracking=True, currency_field = "currency_id", compute = "_compute_augmentation_montants_valides")
    salaire_actuel = fields.Monetary('Salaire Actuel', readonly=True, currency_field = 'currency_id')

    profile_paie_personnel_id = fields.One2many('hr.profile.paie.personnel','contract_id', string = "Profile de paie")
    pp_personnel_id_many2one = fields.Many2one('hr.profile.paie.personnel',string = "Profile de paie m2o")

    type_profile_related = fields.Selection(related="pp_personnel_id_many2one.type_profile", readonly=False)
    nbre_heure_worked_par_demi_jour_related = fields.Float(related="pp_personnel_id_many2one.nbre_heure_worked_par_demi_jour", readonly=False)
    nbre_heure_worked_par_jour_related = fields.Float(related="pp_personnel_id_many2one.nbre_heure_worked_par_jour", readonly=False)
    nbre_jour_worked_par_mois_related = fields.Float(related="pp_personnel_id_many2one.nbre_jour_worked_par_mois", readonly=False)
    definition_nbre_jour_worked_par_mois_related = fields.Selection(related="pp_personnel_id_many2one.definition_nbre_jour_worked_par_mois", readonly=False)
    nbr_saisie_champs_related = fields.Integer(related="pp_personnel_id_many2one.nbr_saisie_champs", readonly=False)
    completer_salaire_related = fields.Boolean(related="pp_personnel_id_many2one.completer_salaire", readonly=False)
    plafonner_bonus_related = fields.Boolean(related="pp_personnel_id_many2one.plafonner_bonus", readonly=False)
    avoir_conge_related = fields.Boolean(related="pp_personnel_id_many2one.avoir_conge", readonly=False)
    period_id_related = fields.Many2one(related="pp_personnel_id_many2one.period_id", readonly=False)
    salaire_jour_related = fields.Float(related="pp_personnel_id_many2one.salaire_jour", readonly=True)
    salaire_demi_jour_related = fields.Float(related="pp_personnel_id_many2one.salaire_demi_jour", readonly=True)
    salaire_heure_related = fields.Float(related="pp_personnel_id_many2one.salaire_heure", readonly=True)


    _sql_constraints = [
		('name_contract_uniq', 'UNIQUE(name)', 'Cette référence est déjà utilisée.'),
	]

    def _compute_augmentation_montants_valides(self):
        query = """
                SELECT SUM(montant_valide)
                FROM hr_augmentation aug,hr_contract ctr, account_month_period mnth
                WHERE aug.employee_id=ctr.employee_id AND aug.period_id=mnth.id AND ctr.state='open' AND ctr.employee_id=%s
                AND mnth.date_start BETWEEN ctr.date_start AND CURRENT_DATE
            """ % (self.employee_id.id)
        self.env.cr.execute(query)
        res = self.env.cr.fetchall()
        if(res[0][0] is not None):
            self.salaire_actuel = self.wage + res[0][0]
        else:
            self.salaire_actuel = self.wage + 0


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
            type_emp = self.env['hr.employee'].browse(vals["employee_id"]).type_emp
            today = datetime.now()
            year = today.year
            month = '{:02d}'.format(today.month)
            contract_sequence = self.env['ir.sequence'].next_by_code('hr.contract.sequence')
            vals['name'] = type_emp + '-' + str(month) + '/' + str(year) + '/' + str(contract_sequence)
        else:
            raise ValidationError(
                    "Erreur, Cet employé a déjà un contrat 'New' ou 'Running'."
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
                "nbr_saisie_champs": self.profile_paie_id.nbr_saisie_champs,    
                "completer_salaire": self.profile_paie_id.completer_salaire,    
                "plafonner_bonus": self.profile_paie_id.plafonner_bonus,    
                "avoir_conge": self.profile_paie_id.avoir_conge,    
                "period_id": self.profile_paie_id.period_id.id,    
                "salaire_mois": self.salaire_actuel,
                "contract_id": self.id,    
                }

            obj = self.env['hr.profile.paie.personnel'].create(champs)
            self.pp_personnel_id_many2one = obj

        else:
           raise ValidationError(
                    "Erreur, Vous devez séléctionner un profile de paie pour le générer."
                )
        return True