# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import date

class jour_ferie(models.Model):
    _name = "hr.jours.feries"
    _descripion = "Jours feries"
    _inherit = ["mail.thread","mail.activity.mixin"]

    name = fields.Selection([
        ('1', '1er janvier : Nouvel an'),
        ('2', "11 janvier : Anniversaire de l'Indépendance"),
        ('3', '30 juillet : Fête du Trône'),
        ('4', '14 août : Commémoration de l’allégeance de l’oued Eddahab'),
        ('5', '20 août : Anniversaire de la révolution, du roi et du peuple'),
        ('6', '6 novembre : Anniversaire de la Marche verte'),
        ('7', '18 novembre : Fête de l’Indépendance'),
        ('8', 'فاتح محرم رأس السنة الهجرية'),
        ('9', 'عيد المولد النبوي الشريف'),
        ('10', 'عيد الفطر'),
        ('11', 'عيد الأضحى'),
    ], string='name',required=True)
    period_id = fields.Many2one("account.month.period", string = "Période", required = True)
    date_start = fields.Date('Date de début',default=fields.Date.today, required = True)
    date_end = fields.Date('Date de fin',default=fields.Date.today, required = True)
    nbr_jour = fields.Float("Nombre de jours", required=True, readonly = True)
    state = fields.Selection([
        ('draft','Brouillon'),
        ('validee',"Validé")
        ],"État",
        default='draft',
        readonly=True
    )

    @api.model
    def create(self, vals):
        date_difference = self.get_duree(vals["date_start"],vals["date_end"])
        vals["nbr_jour"] = date_difference
        return super(jour_ferie, self).create(vals)

    def write(self, vals):
        if vals.get("date_start") and vals.get("date_end"):
            date_difference = self.get_duree(vals["date_start"],vals["date_end"])
            vals["nbr_jour"] = date_difference
        res = super().write(vals)
        if res and 'state' in vals:
            if vals['state'] == 'draft':
                self.update_corresponding_lines('1','3')
            else:
                self.update_corresponding_lines('3','1')
        return res
    
    def get_duree(self,start_date,end_date):
        date_difference = 0
        if start_date and end_date:
            fmt = '%Y-%m-%d'
            d1 = datetime.strptime(str(start_date), fmt)
            d2 = datetime.strptime(str(end_date), fmt)
            sun_count = self.env['account.month.period'].get_count_sundays(start_date,self.env['account.month.period'].add_days_to_date(d2.date(),1))
            date_difference = (d2 - d1).days + 1 - sun_count
        return date_difference
    
    @api.onchange("date_start","date_end")
    def onchange_dates(self):
        date_difference = self.get_duree(self.date_start,self.date_end)
        self.nbr_jour = date_difference
    
    def get_sum_days_jf_between_two_dates(self,date_start,date_end):
        count = 0
        
        for jf in self.env[self._name].search_read([('date_start','>=',date_start),('date_end','<=',date_end)],['nbr_jour']):
            count += jf['nbr_jour']
        return count

    def update_corresponding_lines(self,day_type,type_condition):
        lines = self.env['hr.rapport.pointage.line'].search([
                ('day','>=',self.date_start),
                ('day','<=',self.date_end),
                ('day_type','=',type_condition)
                ])
        
        for line in lines:
            line.write({
                'day_type': day_type,
                'details' :dict(self.fields_get(allfields=['name'])['name']['selection'])[self.name] if type_condition == '1' else False,
                'chantier_id': line.rapport_id.chantier_id.id if type_condition == '1' else False,
                'emplacement_chantier_id': line.rapport_id.emplacement_chantier_id.id if type_condition == '1' else False
                })
        return
    
    def to_draft(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') or self.user_has_groups('hr_management.group_pointeur') :
        
            self.state = 'draft'
        
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs,les agents de paie et les pointeurs qui peuvent changer le statut."
                )

    def to_validee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') or self.user_has_groups('hr_management.group_pointeur') :
        
            self.state = 'validee'
        
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs,les agents de paie et les pointeurs qui peuvent changer le statut."
                )
    