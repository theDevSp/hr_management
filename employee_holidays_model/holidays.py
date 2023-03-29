# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from collections import namedtuple, defaultdict
from pytz import timezone, UTC
from datetime import datetime
from datetime import date

DummyAttendance = namedtuple('DummyAttendance', 'hour_from, hour_to, dayofweek, day_period, week_type')

class holidays(models.Model):
    _name = "hr.holidays"
    _description = "Holidays hr_management"
    _inherit = ['mail.thread','mail.activity.mixin']

    employee_id = fields.Many2one("hr.employee",string="Employé",required=True)
    chantier_id = fields.Many2one('fleet.vehicle.chantier',string="Chantier") 
    motif = fields.Selection([
        ('maladie','Maladie'),
        ('deces',"Décès"),
        ('nv_ne','Nouveau né'),
        ('mariage','Mariage'),
        ('conge_annuel','Congé annuel')
        ],"Motif", required=True
    )
        
    remplacant_employee_id = fields.Many2one("hr.employee",string="Remplaçant")
    state = fields.Selection([
        ('draft','Brouillon'),
        ('validee',"Validé"),
        ('approuvee',"Approuvé"),
        ('refusee',"Refusé"),
        ('annulee',"Annulé")
        ],"État",
        default='draft',
        readonly=True
    )

    date_start = fields.Date('Date de début',default=fields.Date.today)
    date_end = fields.Date('Date de fin',default=fields.Date.today)
    demi_jour = fields.Boolean("Demi Jour")
    heure_perso = fields.Boolean("Heures Personnalisées")
    heure_start = fields.Selection([
        ('0', '00:00'), ('0.5', '00:30'),
        ('1', '01:00'), ('1.5', '01:30'),
        ('2', '02:00'), ('2.5', '02:30'),
        ('3', '03:00'), ('3.5', '03:30'),
        ('4', '04:00'), ('4.5', '04:30'),
        ('5', '05:00'), ('5.5', '05:30'),
        ('6', '06:00'), ('6.5', '06:30'),
        ('7', '07:00'), ('7.5', '07:30'),
        ('8', '08:00'), ('8.5', '08:30'),
        ('9', '09:00'), ('9.5', '09:30'),
        ('10', '10:00'), ('10.5', '10:30'),
        ('11', '11:00'), ('11.5', '11:30'),
        ('12', '12:00'), ('12.5', '12:30'),
        ('13', '13:00'), ('13.5', '13:30'),
        ('14', '14:00'), ('14.5', '14:30'),
        ('15', '15:00'), ('15.5', '15:30'),
        ('16', '16:00'), ('16.5', '16:30'),
        ('17', '17:00'), ('17.5', '17:30'),
        ('18', '18:00'), ('18.5', '18:30'),
        ('19', '19:00'), ('19.5', '19:30'),
        ('20', '20:00'), ('20.5', '20:30'),
        ('21', '21:00'), ('21.5', '21:30'),
        ('22', '22:00'), ('22.5', '22:30'),
        ('23', '23:00'), ('23.5', '23:30')], string='Heure de début')
    heure_end = fields.Selection([
        ('0', '00:00'), ('0.5', '00:30'),
        ('1', '01:00'), ('1.5', '01:30'),
        ('2', '02:00'), ('2.5', '02:30'),
        ('3', '03:00'), ('3.5', '03:30'),
        ('4', '04:00'), ('4.5', '04:30'),
        ('5', '05:00'), ('5.5', '05:30'),
        ('6', '06:00'), ('6.5', '06:30'),
        ('7', '07:00'), ('7.5', '07:30'),
        ('8', '08:00'), ('8.5', '08:30'),
        ('9', '09:00'), ('9.5', '09:30'),
        ('10', '10:00'), ('10.5', '10:30'),
        ('11', '11:00'), ('11.5', '11:30'),
        ('12', '12:00'), ('12.5', '12:30'),
        ('13', '13:00'), ('13.5', '13:30'),
        ('14', '14:00'), ('14.5', '14:30'),
        ('15', '15:00'), ('15.5', '15:30'),
        ('16', '16:00'), ('16.5', '16:30'),
        ('17', '17:00'), ('17.5', '17:30'),
        ('18', '18:00'), ('18.5', '18:30'),
        ('19', '19:00'), ('19.5', '19:30'),
        ('20', '20:00'), ('20.5', '20:30'),
        ('21', '21:00'), ('21.5', '21:30'),
        ('22', '22:00'), ('22.5', '22:30'),
        ('23', '23:00'), ('23.5', '23:30')], string='Heure de fin')

    date_select_half_perso = fields.Date("Date",default=fields.Date.today) 
    matin_soir = fields.Selection([
            ('matin', 'Matinée'),
            ('soir', 'Après-Midi'),
        ], 
        string='Matin/Soir'
    )
    duree_jours = fields.Float("Durée jour", readonly=True)
    duree_heures = fields.Float("Durée heure")
    description = fields.Text("Description")
    
    @api.onchange("demi_jour")
    def onchange_demi_jour(self):
        if self.demi_jour:
            self.heure_perso = False
            self.duree_heures = 4
        elif not self.heure_perso:
            date_difference = self.get_duree(self.date_start,self.date_end)
            self.duree_jours = date_difference
    
    @api.onchange("heure_perso")
    def onchange_heure_perso(self):
        if self.heure_perso:
            self.demi_jour = False
            self.duree_heures = 0
        elif not self.demi_jour:
            date_difference = self.get_duree(self.date_start, self.date_end)
            self.duree_jours = date_difference

    @api.onchange("date_start","date_end")
    def onchange_dates(self):
        date_difference = self.get_duree(self.date_start,self.date_end)
        self.duree_jours = date_difference

    def get_duree(self,start_date,end_date):
        fmt = '%Y-%m-%d'
        d1 = datetime.strptime(str(start_date), fmt)
        d2 = datetime.strptime(str(end_date), fmt)
        date_difference = (d2 - d1).days
        return date_difference
        
    @api.model
    def create(self, vals):
        if vals["demi_jour"]:
            vals["duree_heures"] = 4
        if not vals["demi_jour"] and not vals["heure_perso"]:
            date_difference = self.get_duree(vals["date_start"],vals["date_end"])
            vals["duree_jours"] = date_difference
        return super(holidays, self).create(vals)

    def write(self, vals):
        return super(holidays, self).write(vals)


    def to_draft(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') or self.user_has_groups('hr_management.group_pointeur') :
            if self.state not in {'draft','validee','approuvee','refusee'} :
                self.state = 'draft'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs,les agents de paie et les pointeurs qui peuvent changer le statut."
                )

    def to_validee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') or self.user_has_groups('hr_management.group_pointeur') :
            if self.state not in {'validee','approuvee','refusee','annulee'} :
                self.state = 'validee'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs,les agents de paie et les pointeurs qui peuvent changer le statut."
                )
    
    def to_approuvee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie'):
            if self.state not in {'draft','approuvee','annulee'} :
                self.state = 'approuvee'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )

    def to_refusee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie'):
            if self.state not in {'draft', 'refusee', 'annulee'} :
                self.state = 'refusee'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )


    def to_annulee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') or self.user_has_groups('hr_management.group_pointeur') :
            if self.state not in {'annulee'} :
                self.state = 'annulee'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs,les agents de paie et les pointeurs qui peuvent changer le statut."
                )