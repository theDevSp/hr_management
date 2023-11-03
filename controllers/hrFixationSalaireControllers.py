from odoo import http
from odoo.http import request

import json
from datetime import datetime


class hrFixationSalaireControllers(http.Controller):

    @http.route('/hr_management/get_fixation_salaire_details/<int:id>', type='json', auth='user')
    def get_conges_details(self, id):

        res = http.request.env['hr.fixation.salaire'].search([('id', '=', id)])[
            0]
        data = []

        if res:
            data.append({
                'fixation_num': res.name if res.name else "",
                'employe_name': res.employee_id.name if res.employee_id.name else "",
                'employe_cin': res.employee_id.cin if res.employee_id.cin else "",
                'employe_cnss': res.employee_id.cnss if res.employee_id.cnss else "",
                'employe_chantier': res.chantier_id.code + " - " + res.chantier_id.name.upper() if res.chantier_id.code else "",
                'employe_fonction': res.employee_id.job if res.employee_id.job else "",
                'employe_profile': res.profile.name if res.profile.name else "",
                'employe_date_embauche': res.date_embauche if res.date_embauche else "",
                'employe_emb_par': res.embaucher_par if res.embaucher_par.name else "",
                'employe_rec_par': res.recommander_par if res.recommander_par.name else "",
                'employe_sal_propose': res.offered_wage if res.offered_wage else "",
                'employe_sal_propose_lettres': res.offered_wage_letters if res.offered_wage_letters else "",
                'employe_sal_valider': res.officiel_wage if res.officiel_wage else "",
                'employe_sal_valider_lettres': res.officiel_wage_letters if res.officiel_wage_letters else "",
            })

            return data

        else:
            response_data = {
                'message': 'No data found for the given criteria',
                'timestamp': datetime.now().isoformat()
            }
            return json.dumps(response_data)
