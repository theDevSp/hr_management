from odoo import http
from odoo.http import request

class reportPointageController(http.Controller):
    @http.route('/hr_management/get_report_pointage_Salarie_lines/<int:id>', type='json', auth='user')
    def get_pointage_salarie_lines(self,id):
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
                'dates': data_lines,
            }
        )


        return data
    
    @http.route('/hr_management/get_report_pointage_report/<int:id>', type='json', auth='user')
    def get_pointage_report(self,id):
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
                'totalHeure': res.total_h if res.total_h else "",
                'typeEmployee': res.type_emp if res.type_emp else "",
                'dates': data_lines,
            }
        )


        return data