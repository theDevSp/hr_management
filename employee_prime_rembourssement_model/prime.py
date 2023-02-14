# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError

class prime(models.Model):
    _name = "hr.prime"
    _description = "Prime"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    employee_id = fields.Many2one('hr.employee', string = "Employee", required=True)
    #period_ids = fields.One2many("account.month.period", string = "Période")
    date_fait = fields.Date("Date de fait", required=True, default=fields.Date.today, tracking=True, index=True)
    donneur_order = fields.Many2one("hr.directeur", string = "Directeur")
    responsable_id = fields.Many2one("hr.responsable.chantier", string = "Responsable")
    type_prime = fields.Many2one("hr.prime.type", string = "Type de Prime")
    currency_id = fields.Many2one('res.currency', string = 'Symbole Monétaire')
    montant = fields.Monetary('Montant', currency_field = 'currency_id')
    montant = fields.Monetary(related="type_prime.montant",string='Montant', required=True, tracking=True, currency_field = "currency_id")
