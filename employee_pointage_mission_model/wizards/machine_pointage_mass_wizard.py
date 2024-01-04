from math import ceil
from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import datetime as dt
from datetime import datetime
import time
from collections import defaultdict


class hr_machine_rapport_mass_pointage_wizard(models.TransientModel):

    _name = 'hr.machine.rapport.mass.pointage.wizard'

    def _get_ab_default(self):
        domain = [('id', '=', '-1')]
        year = date.today().year
        period_ids = []
        for mois_id in self.env["account.month.period"].search([('date_stop', '<=', str(year)+'-12-31'), ('date_start', '>=', str(year-1)+'-01-01')]):
            period_ids.append(mois_id.id)
        if period_ids:
            domain = [('id', 'in', period_ids)]

        return domain

    period_id = fields.Many2one(
        "account.month.period", u'Période', domain=_get_ab_default, required=True)

    employee_type = fields.Selection([
        ("a", "Administration")
    ], string=u"Type d'employé", default='a', readonly=True)

    machine_id = fields.Many2one(
        'zk.machines', string='Machine Pointage', help='La machine de pointage', required=True)

    def get_difference(self, startdatetime, enddatetime):
        diff = enddatetime - startdatetime
        return diff.total_seconds()

    def get_pointage_from_machine(self):
        start_time = time.time()

        machine_id = self.machine_id
        conn = machine_id.connect_to_device(
            machine_id.ip_address, machine_id.port)

        period_start = self.period_id.date_start
        period_stop = self.period_id.date_stop

        pointage = machine_id.get_pointage(
            conn, [], period_start, period_stop)

        print(f"pointage_by_date {pointage}")

    def create_rapports_machine_pointage_mass(self):

        self.get_pointage_from_machine()
