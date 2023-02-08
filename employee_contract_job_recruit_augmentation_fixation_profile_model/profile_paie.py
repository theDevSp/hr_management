# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class profilepaie(models.Model):
    _name = "hr.profile.paie"
    _description = "Profile de paie"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Nom", required=True)
    code = fields.Char('Code', required=True, copy=False)
    type_profile = fields.Selection(
        [("h","Horaire"),
        ("j","Journalier")],
        string=u"Type du Profile",
        default="h",
        required=True)
    nbre_heure_worked_par_demi_jour = fields.Float("Heures travaillés par demi jour", required=True)
    nbre_heure_worked_par_jour = fields.Float("Heures travaillés par jour", required=True)
    nbre_heure_worked_par_mois = fields.Float("Heures travaillés par mois", required=True, default=26)

    definition_nbre_jour_worked_par_mois = fields.Selection(
        [("jr_mois","Jours du mois"),
        ("nbr_saisie","Nombre saisi")],
        string=u"Définition nombre jours travaillés par mois",
        required=True)

    nbr_saisie_champs = fields.Integer( string='Champs selon definition nombre jours')

    salaire_mois = fields.Float("Salaire du mois")
    salaire_jour = fields.Float("Salaire du jour")
    salaire_heure = fields.Float("Salaire d'heure")
    salaire_demi_jour = fields.Float("Salaire du demi-jour")

    completer_salaire = fields.Boolean("Compléter le salaire", default=True)
    plafonner_bonus = fields.Boolean("Plafonner le bonus", default=True)
    avoir_conge = fields.Boolean("Peut avoir un congé", default=True)
    period_id = fields.Many2one("account.month.period", string = "Période")

    @api.model
    def create(self, vals):
        return super(profilepaie, self).create(vals)


    def write(self, vals):
        return super(profilepaie, self).write(vals)