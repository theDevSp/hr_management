# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import date

class jour_ferie(models.Model):
    _name = "hr.jours.feries"
    _descripion = "Jours feries"
    _inherit = ["mail.thread","mail.activity.mixin"]

    name = fields.Char("Libellé", required = True )
    period_id = fields.Many2one("account.month.period", string = "Période", required = True)
    date_start = fields.Date('Date de début',default=fields.Date.today, required = True)
    date_end = fields.Date('Date de fin',default=fields.Date.today, required = True)
    nbr_jour = fields.Float("Nombre de jours", required=True, readonly = True)

    @api.model
    def create(self, vals):
        date_difference = self.get_duree(vals["date_start"],vals["date_end"])
        vals["nbr_jour"] = date_difference
        return super(jour_ferie, self).create(vals)

    def write(self, vals):
        if vals.get("date_start") and vals.get("date_end"):
            date_difference = self.get_duree(vals["date_start"],vals["date_end"])
            vals["nbr_jour"] = date_difference
        return super(jour_ferie, self).write(vals)
    

    def get_duree(self,start_date,end_date):
        fmt = '%Y-%m-%d'
        d1 = datetime.strptime(str(start_date), fmt)
        d2 = datetime.strptime(str(end_date), fmt)
        date_difference = (d2 - d1).days
        return date_difference

    @api.onchange("date_start","date_end")
    def onchange_dates(self):
        date_difference = self.get_duree(self.date_start,self.date_end)
        self.nbr_jour = date_difference