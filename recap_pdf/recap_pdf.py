# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import date
import calendar

class recap_pdf(models.Model):
    _name = "hr.recap.pdf"
    _description = "Recap PDF"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Référence",compute='_compute_name')
    period_id = fields.Many2one("account.month.period", string = "Période", required = True)
    quinzaine = fields.Selection([('quinzaine1',"Première quinzaine"),('quinzaine2','Deuxième quinzaine'),('quinzaine12','Q1 + Q2')],string="Quinzaine", required = True)
    type_emp = fields.Selection([("s","Salarié"),("o","Ouvrier")],string=u"Type d'employé",default="s")
    responsable_id = fields.Many2one("res.users","Responsable de paie",domain=lambda self: [("groups_id", "=",self.env.ref("hr_management.group_agent_paie").id)],default=lambda self: self.env.user)
    line_ids= fields.One2many("hr.recap.line.pdf","recap_pdf_id",u"Lignes de Recap")
    
    @api.onchange('type_emp')
    def _onchange_type_emp(self):
        if self.type_emp == 's':
            self.quinzaine = 'quinzaine12'
        else:
            self.quinzaine = 'quinzaine1'
    
    @api.depends('responsable_id')
    def _compute_name(self):
        self.name = self.responsable_id.name