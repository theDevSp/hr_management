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

    name = fields.Char("Référence")
    period_id = fields.Many2one("account.month.period", string = "Période", required = True)
    quinzaine = fields.Selection([('quinzaine1',"Première quinzaine"),('quinzaine2','Deuxième quinzaine'),('quinzaine12','Q1 + Q2')],string="Quinzaine", required = True)
    type_emp = fields.Selection([("s","Salarié"),("o","Ouvrier")],string=u"Type d'employé",default="s")
    responsable_id = fields.Many2one("hr.responsable.chantier","Responsable")
    line_ids= fields.One2many("hr.recap.line.pdf","recap_pdf_id",u"Lignes de Recap")
    
    #total depends de lignes.Montant_total

