from odoo import http
from odoo.http import request

import json
from datetime import datetime

class hrCongesControllers(http.Controller):

    @http.route('/hr_management/get_conges_details/<int:id>', type='json', auth='user')
    def get_conges_details(self, id):

        res = http.request.env['hr.holidays'].search([('id', '=', id)])[0]
        data = []

        if res:
            data.append({
                'Conges_Employe_Name': res.employee_id.name,
                'Conges_Employe_CIN': res.employee_id.cin,
                'Conges_Employe_Chantier': res.chantier_id.code+" - "+res.chantier_id.simplified_name.upper(),
                'Conges_Employe_Fonction': res.employee_id.job,
                'Conges_Motif': res.motif,
                'Conges_Date_Start': res.date_start,
                'Conges_Date_End': res.date_end,
                'Conges_Nbr_Jours': res.duree_jours,
                'Conges_Demijour': res.demi_jour,
                'Conges_Demijour_Date_Start': res.date_select_half_perso
            })

            return data
        
        else:
            response_data = {
                'message': 'No data found for the given criteria',
                'timestamp': datetime.now().isoformat()
            }
            return json.dumps(response_data)