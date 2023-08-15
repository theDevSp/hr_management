from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError,UserError
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
import calendar
import locale
import math


class hr_mission(models.Model):
    _name = 'hr.mission'
    _description = 'Class de gestion des mission des employeés ayant des déplacements fréquents et non planifiés'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    READONLY_STATES = {
        'working': [('readonly', True)],
        'valide': [('readonly', True)],
        'compute': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)]
    }
    
    def _get_period_default(self):
        domain = [('id','=','-1')]
        year = date.today().year
        period_ids = []
        for mois_id in self.env["account.month.period"].search([('date_stop','<=',str(year)+'-12-31'),('date_start','>=',str(year)+'-01-01')]):  
            period_ids.append(mois_id.id) 
        if period_ids :
            domain = [('id', 'in',period_ids)]  
        return domain
    
    name = fields.Char("Référence",readonly=True)
    employee_id = fields.Many2one("hr.employee",u"Employée",readonly=True, ondelete='cascade')
    cin = fields.Char(related='employee_id.cin',string="N° CIN",readonly=True)
    fonction = fields.Char(related='employee_id.job',string="Fonction",readonly=True)
    job_id = fields.Many2one(related='employee_id.job_id',string="Poste occupé",readonly=True)

    chantier_id = fields.Many2one("fleet.vehicle.chantier",u"Dernier Chantier",readonly=True)
    periodicite = fields.Selection(related='chantier_id.periodicite',readonly=True)
    grant_modification = fields.Boolean(related='chantier_id.grant_modification',readonly=True)

    vehicle_id = fields.Many2one("fleet.vehicle",u"Dérnier Code engin",readonly=True)
    emplacement_chantier_id = fields.Many2one("fleet.vehicle.chantier.emplacement","Dernière Équipe",readonly=True)
    