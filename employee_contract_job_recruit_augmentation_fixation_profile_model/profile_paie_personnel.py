# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class profilepaiepersonnel(models.Model):
    _name = "hr.profile.paie.personnel"
    _description = "Profile de paie Personnel"
    _inherit = ['hr.profile.paie','mail.thread', 'mail.activity.mixin']

    contract_id = fields.Many2one("hr.contract", "Contrats")

    salaire_mois = fields.Float("Salaire du mois")
    salaire_jour = fields.Float("Salaire du jour")
    salaire_demi_jour = fields.Float("Salaire du demi-jour")
    salaire_heure = fields.Float("Salaire d'heure")

    @api.model
    def create(self, vals):
        res = super(profilepaiepersonnel, self).create(vals)
        
        res.salaire_jour = res.salaire_mois / res.nbre_jour_worked_par_mois
        res.salaire_demi_jour = res.salaire_jour / 2
        res.salaire_heure = res.salaire_jour / res.nbre_heure_worked_par_jour

        return res


    def write(self, vals):
        return super(profilepaiepersonnel, self).write(vals)