# -*- coding: utf-8 -*-

from odoo import models, fields, api

class profilepaie(models.Model):
    _name = "hr.profile.paie"
    _description = "Profile de paie"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    