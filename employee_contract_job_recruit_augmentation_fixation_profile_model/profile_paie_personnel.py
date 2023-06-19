# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class profilepaiepersonnel(models.Model):
    _name = "hr.profile.paie.personnel"
    _description = "Profile de paie Personnel"
    _inherit = ['hr.profile.paie','mail.thread', 'mail.activity.mixin']

    contract_id = fields.Many2one("hr.contract", "Contrats")

    salaire_mois = fields.Float("Salaire du mois")
    salaire_jour = fields.Float("Salaire du jour")
    salaire_demi_jour = fields.Float("Salaire du demi-jour")
    salaire_heure = fields.Float("Salaire d'heure")

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

    @api.model
    def create(self, vals):
        res = super(profilepaiepersonnel, self).create(vals)
        res.salaire_jour = res.salaire_mois / res.nbre_jour_worked_par_mois
        res.salaire_heure = res.salaire_jour / res.nbre_heure_worked_par_jour
        res.salaire_demi_jour = res.salaire_heure * res.nbre_heure_worked_par_demi_jour
        return res


    def write(self, vals):
        return super(profilepaiepersonnel, self).write(vals)

