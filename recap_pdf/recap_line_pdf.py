# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import date
import calendar

class recap_line_pdf(models.Model):
    _name = "hr.recap.line.pdf"
    _description = "Recap Line PDF"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    chantier_id = fields.Many2one("fleet.vehicle.chantier",u"Chantier")
    emplacement_chantier_id = fields.Many2one("fleet.vehicle.chantier.emplacement","Équipe")
    nombre_effectif = fields.Integer("Nombre D'effectif")
    montant_total = fields.Float("Montant total")  #compute
    recap_pdf_id = fields.Many2one("hr.recap.pdf",u"Recap",ondelete="cascade")

