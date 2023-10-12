from odoo import http
from odoo.http import request

import json
from datetime import datetime

class reportPointageController(http.Controller):
    @http.route('/hr_management/get_report_pointage_salarie_ouvrier/<int:id>', type='json', auth='user')
    def get_pointage_salarie_ouvrier(self,id):
        res = http.request.env['hr.rapport.pointage'].search([('id', '=', id)])[0]
        data = []
        data_lines = []

        for line in res.rapport_lines:
            code = ""

            if (len(line.vehicle_ids) > 1):
                code = line.vehicle_ids[len(line.vehicle_ids)-1].name.code+' +'+str(len(line.vehicle_ids)-1)
            elif(len(line.vehicle_ids) == 1):
                code = line.vehicle_ids[len(line.vehicle_ids)-1].name.code

            data_lines.append(
                {
                    'jour': line.name if line.name else "",
                    'th': line.h_travailler if line.h_travailler else "",
                    'chantier': line.chantier_id.simplified_name if line.chantier_id.simplified_name else "",
                    'equipe': line.emplacement_chantier_id.abrv if line.emplacement_chantier_id.abrv else "",
                    'observation': line.details if line.details else "",
                    'code': str(code),
                }
            )

        data.append(
            {
                'report_num': res.name if res.name else "",
                'month': res.period_id.display_name if res.period_id.display_name else "",
                'nometpnom': res.employee_id.name if res.employee_id.name else "",
                'cin': res.cin if res.cin else "",
                'fonction': res.job_id.name if res.job_id.name else "",
                'dChantier': res.chantier_id.name if res.chantier_id.name else "",
                'dEquipe': res.emplacement_chantier_id.abrv if res.emplacement_chantier_id.abrv else "",
                'dEngin': res.vehicle_id.code if res.vehicle_id.code else "",
                'totalheure': res.total_h if res.total_h else "",
                'totaljours': res.total_j if res.total_j else "",
                'typeEmployee': res.type_emp if res.type_emp else "",
                'dates': data_lines,
            }
        )


        return data
    

    @http.route('/hr_management/get_dashboard_report_pointage_salarie_ouvrier/<int:mois>', type='json', auth='user')
    def get_report_pointage_filtered(self, period_id=None, chantier_id=None, type_employe=None, quinz=None, equipe_id=None):

        #chantier_id = chantier_id
        #period_id = period_id
        #equipe_id = 4
        # quinz = 'quinzaine12'
        #type_employe = "s"

        domains = [('period_id', '=', period_id), ('chantier_id', '=', chantier_id)]

        if quinz:
            domains.append(('quinzaine', '=', quinz))

        res = http.request.env['hr.rapport.pointage'].search(domains)

        if type_employe:
            res = [emp for emp in res if emp.type_emp == type_employe]

        if equipe_id:
            res = [emp for emp in res if emp.emplacement_chantier_id.id == equipe_id]

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

        if not data:
            response_data = {
                'message': 'No data found for the given criteria',
                'timestamp': datetime.now().isoformat()
            }
            return json.dumps(response_data)

        return data
