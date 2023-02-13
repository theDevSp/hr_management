# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class primetype(models.Model):
    _name = "hr.prime.type"
    _description = "Prime Type"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Libellé')
    type_addition = fields.Selection([
        ('indiv', 'Individuelle'),
        ('perio', 'Périodique')
        ], 
        string="Type d'addition",
        default='indiv'
    )
    currency_id = fields.Many2one('res.currency', string = 'Symbole Monétaire')
    montant = fields.Monetary('Montant', currency_field = 'currency_id')

    @api.constrains('montant')
    def _check_montant(self):
        if self.montant <= 0:
            raise ValidationError("Le montant doit être supérieur de la valeur 0.")
  