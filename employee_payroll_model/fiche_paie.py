# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class fiche_paie(models.Model):
    _name = "hr.payslip"
    _description = "Fiche de paie"
    _inherit = ['mail.thread','mail.activity.mixin']

    name =  fields.Char("Référence", readonly=True, copy=False, default='New')
    employee_id = fields.Many2one("hr.employee",string="Employé",required=True)
    chantier_id = fields.Many2one('fleet.vehicle.chantier',string="Dernier Chantier")
    period_id = fields.Many2one("account.month.period", string = "Période", required = True)
    net_pay = fields.Float('Net à payer', compute="compute_net_a_payer", readonly=True)
    jr_travaille_par_chantier = fields.One2many("jr.travaille.par.chantier", 'fiche_paie_id',string='Jours travaillés par chantier', readonly=True)
    type_fiche = fields.Selection([
        ("stc","STC"),
        ("type1","Type 1"),
        ("type2","Type 2"),
        ("type3","Type 3"),
        ("type4","Type 4"),
        ],"Type de fiche", 
    )

    state  = fields.Selection([
        ("draft","Brouillon"),
        ("validee","Validée"),
        ("annulee","Annulée"),
        ],"Status", 
        default="draft",
    )
    
    affich_bonus_jour = fields.Float("Bonus jour", compute="compute_affich_bonus_jour", readonly=True)
    affich_jour_conge = fields.Float("Jour congé", compute="compute_affich_jour_conge", readonly=True)
    stc_id = fields.Many2one("hr.stc", string = "STC", required=False)
    
    nbr_jour_travaille =  fields.Float("Nombre de jours travaillés")
    nbr_heure_travaille =  fields.Float("Nombre des heures travaillées")
    contract_id = fields.Many2one("hr.contract", string = "Contrat")
    type_emp = fields.Selection(related="contract_id.type_emp",string=u"Type d'employé", required=False, store=True, readonly=True)
    job_id = fields.Many2one(related="contract_id.job_id", string='Poste', store=True, readonly=True)
    salaire_actuel = fields.Float(related="contract_id.salaire_actuel", string='Salaire Actuel', store=True, readonly=True)
    date_validation = fields.Date(u'Date de validation', readonly=True)
    salaire_jour = fields.Float(compute='compute_salaires',string="Salaire du jour", readonly=True)
    salaire_demi_jour = fields.Float(compute='compute_salaires',string="Salaire du demi-jour", readonly=True)
    salaire_heure = fields.Float(compute='compute_salaires',string="Salaire d'heure", readonly=True)
    quinzaine = fields.Selection([('quinzaine1',"Première quinzaine"),('quinzaine2','Deuxième quinzaine'),('quinzaine12','Q1 + Q2')],string="Quinzaine")
    emplacement_chantier_id = fields.Many2one("fleet.vehicle.chantier.emplacement",u"Équipe")
    type_profile_related = fields.Selection(related="contract_id.type_profile_related",string=u"Type du profile", required=False, store=True, readonly=True)
    rapport_id = fields.Many2one("hr.rapport.pointage", string = "Rapport de pointage")
    # vehicle_id = ...................

    @api.model
    def create(self, vals):
        today = datetime.now()
        year = today.year
        month = '{:02d}'.format(today.month)
        fiche_paie_sequence = self.env['ir.sequence'].next_by_code('hr.payslip.sequence')
        vals['name'] =  str(fiche_paie_sequence) + '/' + str(month) + '/' + str(year)        
        return super(fiche_paie, self).create(vals)

    def write(self, vals):
        return super(fiche_paie, self).write(vals)

    
    @api.depends('employee_id','period_id','contract_id')
    def compute_salaires(self):
        for rec in self:
            if self.contract_id:
                query = """ select nbre_jour_worked_par_mois,
                                nbre_heure_worked_par_jour,
                                nbre_heure_worked_par_demi_jour,
                                definition_nbre_jour_worked_par_mois
                            from hr_profile_paie_personnel 
                            where contract_id = %s;
                        """ % (rec.contract_id.id)
                
                rec.env.cr.execute(query)
                res = rec.env.cr.fetchall()

                if len(res) > 0:
                    jr_worked_par_mois = res[0][0]
                    heure_worked_par_jour = res[0][1]
                    heure_worked_par_demi_jour = res[0][2]

                    rec.salaire_jour = rec.salaire_actuel / jr_worked_par_mois
                    rec.salaire_heure = rec.salaire_jour / heure_worked_par_jour
                    rec.salaire_demi_jour = rec.salaire_heure * heure_worked_par_demi_jour
                else :
                    rec.salaire_jour = 0
                    rec.salaire_heure = 0
                    rec.salaire_demi_jour = 0
            else: 
                rec.salaire_jour = 0
                rec.salaire_heure = 0
                rec.salaire_demi_jour = 0


    @api.onchange('employee_id')
    def get_contract_actif(self):
        if self.employee_id:
            self.contract_id = ""
            self.type_emp = ""
            self.job_id = ""
            self.salaire_actuel = ""
            self.salaire_jour = ""
            self.salaire_demi_jour = ""
            self.salaire_heure = ""
            self.contract_id = self.employee_id.contract_id

        
    def compute_affich_jour_conge(self):
        self.affich_jour_conge = self.employee_id.panier_conge + self.employee_id.panier_jr_ferie
       
       
    def compute_affich_bonus_jour(self):
        worked_time = 0
        base_time = 0
        res = 0

        profile_paie_p = self.contract_id.pp_personnel_id_many2one
        type_profile = self.type_profile_related
        definition_nbre_jour_worked_par_mois = profile_paie_p.definition_nbre_jour_worked_par_mois
        
        if type_profile == 'j':
            worked_time = self.nbr_jour_travaille
            base_time = profile_paie_p.nbre_jour_worked_par_mois
        elif type_profile == 'h':
            worked_time = self.nbr_heure_travaille
            base_time = profile_paie_p.nbre_heure_worked_par_jour * profile_paie_p.nbre_jour_worked_par_mois

        res = worked_time / base_time * 1.5

        if profile_paie_p.periodicity == "m":
            self.affich_bonus_jour = min(res, 1.5)
        else:
            self.affich_bonus_jour = min(res,0.75)  


    @api.depends('nbr_jour_travaille','nbr_heure_travaille','contract_id','salaire_actuel')
    def compute_net_a_payer(self):
        resultat = 0
        for rec in self:
            if self.contract_id:
                type_profile = rec.type_profile_related
                if type_profile == "h":
                    resultat = rec.nbr_heure_travaille * rec.salaire_heure
                elif type_profile == "j":
                    resultat = rec.nbr_jour_travaille * rec.salaire_jour
        self.net_pay = resultat


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