from odoo import http
from odoo.http import request

import requests,calendar
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import json
from itertools import groupby


class printReportPointageController(http.Controller):
    @http.route('/hr_management/pointage/get_all_chantiers', type='json', auth='user')
    def get_all_chantiers(self):

        chantier_records = http.request.env['fleet.vehicle.chantier'].search([
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

        domains = [('period_id', '=', 129),  # period 129
                   ('chantier_id', '=', 483)]  # chantier_id 483

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
                    code = "Null"
                    vehicle_ids_len = len(re_line.vehicle_ids)

                    if vehicle_ids_len > 1:
                        code = f"{re_line.vehicle_ids[-1].name.code} +{vehicle_ids_len - 1}"
                    elif vehicle_ids_len == 1:
                        code = re_line.vehicle_ids[-1].name.code

                    dates_lines.append({
                        'jour': re_line.name or "Null",
                        'th': re_line.h_travailler or "Null",
                        'chantier': re_line.chantier_id.simplified_name or "Null",
                        'equipe': re_line.emplacement_chantier_id.abrv or "Null",
                        'observation': re_line.details or "Null",
                        'code': str(code),
                        # diff
                    })

                data_entry = {
                    'employe_month': re.period_id.display_name or "Null",
                    'employe_name': re.employee_id.name or "Null",
                    'employe_cin': re.cin or "Null",
                    'employe_fonction': re.job_id.name or "Null",
                    'employe_chantier': re.chantier_id.name or "Null",
                    'employe_equipe': re.emplacement_chantier_id.name or "Null",
                    'employe_engin': re.vehicle_id.code or "Null",
                    'employe_totalheure': re.total_h or "Null",
                    'employe_type': re.type_emp or "Null",
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

        domains = [('period_id', '=', 129),  # period 129
                   ('chantier_id', '=', 483)]  # chantier_id 483

        if quinz:
            domains.append(('quinzaine', '=', quinz))

        if equipe_id:
            equipe_id = int(equipe_id)
            domains.append(('emplacement_chantier_id', '=', equipe_id))

        if type_employe:
            domains.append(('type_emp', '=', type_employe))

        res = http.request.env['hr.rapport.pointage'].search(domains)

        chantier = http.request.env['fleet.vehicle.chantier'].browse(483) #chantier_id
        period = http.request.env['account.month.period'].browse(129) #period_id

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
                    for re_line in re.rapport_lines:
                        dates_lines.append({
                            'jour': re_line.name or "",
                            'th': re_line.h_travailler or "",
                            'sup': re_line.h_sup_cal,
                            'observation': re_line.details or "",
                            'date': re_line.day
                        })
                        
                    data_entry = {
                        'employe_name': re.employee_id.name or "",
                        'employe_cin': re.cin or "",
                        'employe_fonction': re.job_id.name or "",
                        'employe_totalheure': re.total_h or "",
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

        post = json.loads(request.httprequest.data.decode('utf-8'))

        chantier_id = post.get("chantier")
        period_id = post.get("date")
        quinz = post.get("quinzine")
        equipe_id = post.get("equipe")
        type_employe = post.get("typeemp")

        period_id = int(period_id)
        chantier_id = int(chantier_id)

        domains = [('period_id', '=', 129),  # period 129
                   ('chantier_id', '=', 483)]  # chantier_id 483

        if quinz:
            domains.append(('quinzaine', '=', quinz))

        if equipe_id:
            equipe_id = int(equipe_id)
            domains.append(('emplacement_chantier_id', '=', equipe_id))

        if type_employe:
            domains.append(('type_emp', '=', type_employe))

        res = http.request.env['hr.rapport.pointage'].search(domains)

        chantier = http.request.env['fleet.vehicle.chantier'].browse(
            chantier_id)
        period = http.request.env['account.month.period'].browse(period_id)

        if res:
            finalDataList = []

            # Group data by equipe_id
            grouped_data = {}
            for re in res:
                equipe_name = re.emplacement_chantier_id.name
                if equipe_name not in grouped_data:
                    grouped_data[equipe_name] = []

            print(grouped_data.items())

            for equipe_id, equipe_data in grouped_data.items():
                equipe_final_data = {
                    "chantier": chantier.name,
                    "periode": period.code,
                    "equipe": equipe_data[0].employee_id.job_id.name,
                    "quinz": 'Première Quinzaine' if quinz == 'quinzaine1' else 'Deuxième Quinzaine',
                    "data": []
                }

                for re in equipe_data:
                    dates_lines = []

                    for re_line in re.rapport_lines:
                        dates_lines.append({
                            'jour': re_line.name or "Null",
                            'th': re_line.h_travailler or "Null",
                            'observation': re_line.details or "Null"
                        })

                    data_entry = {
                        'employe_name': re.employee_id.name or "Null",
                        'employe_cin': re.cin or "Null",
                        'employe_fonction': re.job_id.name or "Null",
                        'employe_totalheure': re.total_h or "Null",
                        'employe_type': re.type_emp or "Null",
                        'employe_dates': {
                            'dates_lines': dates_lines
                        }
                    }

                    equipe_final_data["data"].append(data_entry)

                finalDataList.append(equipe_final_data)

            return http.request.make_json_response(data=finalDataList, status=200)
        else:
            return http.request.make_json_response(data={'message': 'No data found'}, status=204)

