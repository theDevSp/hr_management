# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class jr_travaille_par_chantier(models.Model):
    _name = "jr.travaille.par.chantier"
    _description = "Jr Travaille Par Chantier"
    _inherit = ['mail.thread','mail.activity.mixin']

    chantier_id = fields.Many2one('fleet.vehicle.chantier',string="Chantier")
    emplacement_chantier_id = fields.Many2one("fleet.vehicle.chantier.emplacement",u"Équipe")
    #vehicle = fields.Many2one('fleet.vehicle',string="Dérnier Engin")
    nbr_jour = fields.Float("Nombre des jours")
    nbr_heure = fields.Float("Nombre des heures")
    nbr_dimanches_travaille = fields.Float("Nombre des dimanches travaillés")
    fiche_paie_id = fields.Many2one("hr.payslip", "Fiche de paie")
   

    @api.model
    def create(self, vals):
        return super(jr_travaille_par_chantier, self).create(vals)

    def write(self, vals):
        return super(jr_travaille_par_chantier, self).write(vals)