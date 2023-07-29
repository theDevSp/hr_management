# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class jr_travaille_par_chantier(models.Model):
    _name = "jr.travaille.par.chantier"
    _description = "Jr Travaille Par Chantier"
    _inherit = ['mail.thread','mail.activity.mixin']

    chantier_id = fields.Many2one('fleet.vehicle.chantier',string="Chantier")
    emplacement_chantier_id = fields.Many2one("fleet.vehicle.chantier.emplacement",u"Équipe")
    vehicle_id = fields.Many2one('fleet.vehicle',string="Dérnier Engin")
    nbr_jour = fields.Float("Nombre des jours")
    nbr_heure = fields.Float("Nombre des heures")
    fiche_paie_id = fields.Many2one("hr.payslip", "Fiche de paie")
    employee_id = fields.Many2one("hr.employee", "Employé")
    rapport_id = fields.Many2one("hr.rapport.pointage", "Rapport")
    amount_wage_day = fields.Char(compute='_compute_amount_wage_day', string='Montant (Jr)')
    amount_wage_hours = fields.Char(compute='_compute_amount_wage_hours', string='Montant (H)')
    
    @api.depends('nbr_jour')
    def _compute_amount_wage_day(self):
        self.amount_wage_day = self.fiche_paie_id.salaire_jour * self.nbr_jour

    @api.depends('nbr_heure')
    def _compute_amount_wage_hours(self):
        self.amount_wage_hours = self.fiche_paie_id.salaire_heure * self.nbr_heure

    @api.model
    def create(self, vals):
        return super(jr_travaille_par_chantier, self).create(vals)

    def write(self, vals):
        return super(jr_travaille_par_chantier, self).write(vals)