from odoo import http
from odoo.http import request

class reportPointageController(http.Controller):
    @http.route('/hr_management/get_report_pointage_salarie_ouvrier/<int:id>', type='json', auth='user')
    def get_pointage_salarie_lines(self,id):
        res = http.request.env['hr.rapport.pointage'].search([('id', '=', id)])[0]
        data = []
        data_lines = []

        for line in res.rapport_lines:
            code = "Null"

            if (len(line.vehicle_ids) > 1):
                code = line.vehicle_ids[len(line.vehicle_ids)-1].name.code+' +'+str(len(line.vehicle_ids)-1)
            elif(len(line.vehicle_ids) == 1):
                code = line.vehicle_ids[len(line.vehicle_ids)-1].name.code

            data_lines.append(
                {
                    'jour': line.name if line.name else "Null",
                    'th': line.h_travailler if line.h_travailler else "Null",
                    'chantier': line.chantier_id.simplified_name if line.chantier_id.simplified_name else "Null",
                    'equipe': line.emplacement_chantier_id.abrv if line.emplacement_chantier_id.abrv else "Null",
                    'observation': line.details if line.details else "Null",
                    'code': str(code),
                }
            )

        data.append(
            {
                'report_num': res.name if res.name else "Null",
                'month': res.period_id.display_name if res.period_id.display_name else "Null",
                'nometpnom': res.employee_id.name if res.employee_id.name else "Null",
                'cin': res.cin if res.cin else "Null",
                'fonction': res.job_id.name if res.job_id.name else "Null",
                'dChantier': res.chantier_id.name if res.chantier_id.name else "Null",
                'dEquipe': res.emplacement_chantier_id.abrv if res.emplacement_chantier_id.abrv else "Null",
                'dEngin': res.vehicle_id.code if res.vehicle_id.code else "Null",
                'totalheure': res.total_h if res.total_h else "Null",
                'typeEmployee': res.type_emp if res.type_emp else "Null",
                'dates': data_lines,
            }
        )


        return data
    