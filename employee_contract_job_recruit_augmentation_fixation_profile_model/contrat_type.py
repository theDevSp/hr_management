# -*- coding: utf-8 -*-

from odoo import models, fields, api

class typecontrat(models.Model):
    _description = "Type Contrat"
    _inherit = ['hr.contract.type']

    description = fields.Html('Description')