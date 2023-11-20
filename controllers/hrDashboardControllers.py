from odoo import http
import json
from datetime import datetime
from odoo.http import request
from odoo.tools import html2plaintext
from itertools import groupby

from colorama import Fore, Back, Style


class HrDashboardControllers(http.Controller):

    @http.route('/hr_management/dashboard/', type='json', auth='user')
    def get_dashboard_details(self, chantier_id, period_id, periodicite):

        period_id = int(period_id)
        chantier_id = int(chantier_id)

        domains = [('period_id', '=', period_id),
                   ('chantier_id', '=', chantier_id),
                   ('quinzaine', '=', periodicite)]

        payslips = http.request.env['hr.payslip'].search(domains)

        grouped_data = {}

        if payslips:

            res = sorted(payslips, key=lambda re: re.emplacement_chantier_id.name)

            for ligne in res:
                emplacement_name = ligne.emplacement_chantier_id.name

                if emplacement_name not in grouped_data:
                    grouped_data[emplacement_name] = []

                grouped_data[emplacement_name].append({
                    'id': ligne.id,
                    'name': ligne.name
                })

        return grouped_data
