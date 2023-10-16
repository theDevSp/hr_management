from odoo import http
from odoo.http import request

import requests
import calendar
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import json
from itertools import groupby


class printReportPointageController(http.Controller):
    @http.route('/hr_management/pointage/get_all_chantiers', type='json', auth='user')
    def get_all_chantiers(self):

        chantier_records = http.request.env['fleet.vehicle.chantier'].search([
            ('type_chantier', '!=', 'CG')
        ])

        data = []

        for record in chantier_records:

            data.append({
                'id': record.id,
                'name': record.name,
            })

        if data:
            return data
        else:
            return {
                'code': 504,
                'msg': 'error'
            }

    @http.route('/hr_management/pointage/get_all_Equipes', type='json', auth='user')
    def get_all_equipes(self):

        equipe_records = http.request.env['fleet.vehicle.chantier.emplacement'].search([
        ])

        data = []

        for record in equipe_records:

            data.append({
                'id': record.id,
                'name': record.name.upper(),
            })

        if data:
            return data
        else:
            return {
                'code': 504,
                'msg': 'error'
            }

    @http.route('/hr_management/pointage/get_all_periods', type='json', auth='user')
    def get_all_periods(self):

        today = date.today()
        this_year = today.year
        first_day_of_next_month = today + relativedelta(day=1, months=1)
        periods = request.env['account.month.period'].search([
            ('date_stop', '<', first_day_of_next_month),
            ('fiscalyear_id.fiscal_year_id.name',
             'in', [str(this_year), str(this_year-1)])
        ], order='date_start asc')

        data = []

        for record in periods:
            data.append({
                'id': record.id,
                'code': record.code,
                'year': record.fiscalyear_id.fiscal_year_id.display_name
            })

        if data:
            return data
        else:
            return http.request.make_json_response(data={'message': 'No data found'}, status=404)

    @http.route('/hr_management/get_report_pointage/', type='http', auth='user', methods=['POST'], csrf=False)
    def get_report_pointage_filtered(self):

        post = json.loads(request.httprequest.data.decode('utf-8'))

        chantier_id = post.get("chantier")
        period_id = post.get("date")
        quinz = post.get("quinzine")
        equipe = post.get("equipe")
        type_employe = post.get("typeemp")

        period_id = int(period_id)
        chantier_id = int(chantier_id)

        domains = [('period_id', '=', period_id),  # period 129
                   ('chantier_id', '=', chantier_id)]  # chantier_id 483

        if quinz:
            domains.append(('quinzaine', '=', quinz))

        if equipe:
            equipe = int(equipe)
            domains.append(('emplacement_chantier_id', '=', equipe))

        if type_employe:
            domains.append(('type_emp', '=', type_employe))

        res = http.request.env['hr.rapport.pointage'].search(domains)

        if res:
            data = []

            for re in res:
                dates_lines = []

                for re_line in re.rapport_lines:
                    code = ""
                    vehicle_ids_len = len(re_line.vehicle_ids)

                    if vehicle_ids_len > 1:
                        code = f"{re_line.vehicle_ids[-1].name.code} +{vehicle_ids_len - 1}"
                    elif vehicle_ids_len == 1:
                        code = re_line.vehicle_ids[-1].name.code

                    dates_lines.append({
                        'jour': re_line.name or "",
                        'th': re_line.h_travailler or "",
                        'chantier': re_line.chantier_id.simplified_name or "",
                        'equipe': re_line.emplacement_chantier_id.abrv or "",
                        'observation': re_line.details or "",
                        'code': str(code),
                    })

                data_entry = {
                    'employe_month': re.period_id.display_name or "",
                    'employe_name': re.employee_id.name or "",
                    'employe_cin': re.cin or "",
                    'employe_fonction': re.job_id.name or "",
                    'employe_chantier': re.chantier_id.name or "",
                    'employe_equipe': re.emplacement_chantier_id.name or "",
                    'employe_engin': re.vehicle_id.code or "",
                    'employe_totalheure': re.total_h or "",
                    'employe_totaljours': re.total_j or "",
                    'employe_type': re.type_emp or "",
                    'employe_dates': {
                        'quinzeine': re.quinzaine,
                        'dates_lines': dates_lines,
                    },
                    'report_Num': re.name
                }

                data.append(data_entry)
                data = sorted(data, key=lambda x: x['employe_equipe'])

            return http.request.make_json_response(data=data, status=200)
        else:
            return http.request.make_json_response(data={'message': 'No data found'}, status=204)

    @http.route('/hr_management/get_report_pointage_ouvrier/', type='http', auth='user', methods=['POST'], csrf=False)
    def get_report_pointage_ouvrier_filtered(self):
        post = json.loads(request.httprequest.data.decode('utf-8'))

        chantier_id = post.get("chantier")
        period_id = post.get("date")
        quinz = post.get("quinzine")
        equipe_id = post.get("equipe")
        type_employe = post.get("typeemp")

        period_id = int(period_id)
        chantier_id = int(chantier_id)

        domains = [('period_id', '=', period_id),  # period 129
                   ('chantier_id', '=', chantier_id)]  # chantier_id 483

        if quinz:
            domains.append(('quinzaine', '=', quinz))

        if equipe_id:
            equipe_id = int(equipe_id)
            domains.append(('emplacement_chantier_id', '=', equipe_id))

        if type_employe:
            domains.append(('type_emp', '=', type_employe))

        res = http.request.env['hr.rapport.pointage'].search(domains)

        chantier = http.request.env['fleet.vehicle.chantier'].browse(
            chantier_id)  # chantier_id
        period = http.request.env['account.month.period'].browse(
            period_id)  # period_id

        if res:
            res = sorted(res, key=lambda re: re.emplacement_chantier_id.name)
            final = []

            for group_key, group in groupby(res, key=lambda re: re.emplacement_chantier_id.name):
                obj = {
                    "equipe": group_key.upper(),
                    "data": []
                }

                for re in group:
                    dates_lines = []
                    sup = 0
                    for re_line in re.rapport_lines:

                        """report_line.details and 'gardien' not in report_line.employee_id.job_id.name.lower() and 
									(float(report_line.h_travailler) - report_line.get_normal_heur(report_line.day,report_line.chantier_id) > 0 or 
									float(report_line.h_travailler) > 0 and report_line.day_type == 2)"""

                        h_tr = float(re_line.h_travailler)
                        if ('gardien' not in re_line.employee_id.job_id.name.lower()):
                            if (re_line.day_type == '1' and re_line.h_sup_cal > 0):
                                sup = re_line.h_sup_cal
                            elif (re_line.day_type == '2' and h_tr > 0):
                                sup = float(re_line.day_type)
                        else:
                            sup = 0.0

                                
                        dates_lines.append({
                            'jour': re_line.name or "",
                            'th': re_line.h_travailler or "",
                            'sup': sup,
                            'observation': re_line.details or "",
                            'date': re_line.day
                        })

                    data_entry = {
                        'employe_name': re.employee_id.name or "",
                        'employe_cin': re.cin or "",
                        'employe_fonction': re.job_id.name or "",
                        'employe_totalheure': re.total_h or "",
                        'employe_totaljours': re.total_j or "",
                        'employe_type': re.type_emp or "",
                        'employe_dates': {
                            'dates_lines': dates_lines
                        },
                    }
                    obj["data"].append(data_entry)

                final.append(obj)

            return http.request.make_json_response(data={
                "chantier": chantier.name.upper(),
                "periode": period.name.upper(),
                "quinzine": "Première Quinzaine" if quinz == "quinzaine1" else "Deuxième Quinzaine",
                "lines": final,
                "nbrj_mois": period.get_number_of_days_per_month()-15 if quinz == "quinzaine2" else 15
            }, status=200)

        else:
            return http.request.make_json_response(data={'message': 'No data found'}, status=204)
