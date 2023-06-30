# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from datetime import date
from math import *
from odoo.exceptions import ValidationError
from calendar import monthrange

class profilepaie(models.Model):
    _name = "hr.profile.paie"
    _description = "Profile de paie"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Nom", required=True)
    code = fields.Char('Code', required=True, copy=False)
    type_profile = fields.Selection(
        [("h","Horaire"),
        ("j","Journalier")],
        string=u"Type Profile",
        default="h",
        required=True)

    
    nbre_heure_worked_par_demi_jour = fields.Float("Heures travaillées par demi jour", required=True)
    nbre_heure_worked_par_jour = fields.Float("Heures travaillées par jour", required=True)
    nbre_jour_worked_par_mois = fields.Float("Jours travaillés par mois", required=True, default=26)

    definition_nbre_jour_worked_par_mois = fields.Selection(
        [("jr_mois","Jours du mois"),
        ("nbr_saisie","Nombre saisi")],
        string=u"Définition des jours travaillés",
        required=True,
        default='nbr_saisie')

    completer_salaire = fields.Boolean("Compléter le salaire", default=True)
    plafonner_bonus = fields.Boolean("Plafonner le bonus", default=True)
    avoir_conge = fields.Boolean("Peut avoir un congé", default=True)
    justification = fields.Boolean("Détails travaux obligé", default=True)
    period_id = fields.Many2one("account.month.period", string = "Période")
    periodicity = fields.Selection(
        [("q", "Quinzainier"),
         ("m", "mensuel")],
         string="Périodicité", required=True, default="q"
    )

    @api.constrains('nbre_heure_worked_par_jour')
    def _check_nbre_heure_worked_par_jour(self):
        if self.nbre_heure_worked_par_jour <= 0:
            raise ValidationError("Les Heures et Jours travaillés doivent être supérieurs de la valeur 0.")

    
    @api.constrains('nbre_heure_worked_par_demi_jour')
    def _check_nbre_heure_worked_par_demi_jour(self):
        if self.nbre_heure_worked_par_demi_jour <= 0:
            raise ValidationError("Les Heures et Jours travaillés doivent être supérieurs de la valeur 0.")


    @api.constrains('nbre_jour_worked_par_mois')
    def _check_nbre_jour_worked_par_mois(self):
        if self.nbre_jour_worked_par_mois <= 0:
            raise ValidationError("Les Heures et Jours travaillés doivent être supérieurs de la valeur 0.")
            
    @api.onchange('definition_nbre_jour_worked_par_mois')
    def _onchange_definition_nbre_jour_worked_par_mois(self):
        today = date.today()
        nbr_days = monthrange(today.year, today.month)[1]
        self.nbre_jour_worked_par_mois = nbr_days if self.definition_nbre_jour_worked_par_mois == 'jr_mois' else 26

    @api.model
    def create(self, vals):
        return super(profilepaie, self).create(vals)


    def write(self, vals):        
        return super(profilepaie, self).write(vals)