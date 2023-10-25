from odoo import http
from odoo.http import request

import json
from datetime import datetime


class hrCongesControllers(http.Controller):

    @http.route('/hr_management/get_employe_details/<int:id>', type='json', auth='user')
    def get_conges_details(self, id):

        res = http.request.env['hr.employee'].sudo().search(
                [('id', '=', id)], limit=1)
        data = []

        if res:
            data.append({
                'employe_name': res.name if res.name not in [False, True, 0, 0.0, ""] else "-",
                'employe_cin': res.cin if res.cin not in [False, True, 0, 0.0, ""] else "-",
                'employe_chantier': res.chantier_id.code + " - " + res.chantier_id.simplified_name.upper(),
                'employe_fonction': res.job if res.job not in [False, True, 0, 0.0, ""] else "-",
                'employe_cnss': res.cnss if res.cnss not in [False, True, 0, 0.0, ""] else "-",
                'employe_date_naissance': res.date_naissance if res.date_naissance not in [False, True, 0, 0.0, ""] else "-",
                'employe_val_cin': res.date_cin if res.date_cin not in [False, True, 0, 0.0, ""] else "-",
                'employe_lieu_naissance': res.lieu_naissance if res.lieu_naissance not in [False, True, 0, 0.0, ""] else "-",
                'employe_genre': res.gender if res.gender not in [False, True, 0, 0.0, ""] else "-",
                'employe_etat_civil': res.marital if res.marital not in [False, True, 0, 0.0, ""] else "-",
                'employe_nbr_enfant': res.nombre_enfants if res.nombre_enfants not in [False, True, 0, 0.0, ""] else "-",
                'employe_num_tele': res.mobile_phone if res.mobile_phone not in [False, True, 0, 0.0, ""] else "-",
                'employe_type': res.type_emp if res.type_emp not in [False, True, 0, 0.0, ""] else "-",
                'employe_contract_type': res.contract_id.contract_type if res.contract_id.contract_type not in [False, True, 0, 0.0, ""] else "-",
                'employe_salaire': res.contract_id.wage if res.contract_id.wage not in [False, True, 0, 0.0, ""] else "-",
                'employe_contract_debut': res.contract_id.date_start if res.contract_id.date_start not in [False, True, 0, 0.0, ""] else "-",
                'employe_contract_fin': res.contract_id.date_end if res.contract_id.date_end not in [False, True, 0, 0.0, ""] else "-",
                'employe_profile_paie': res.contract_id.profile_paie_id.display_name if res.contract_id.profile_paie_id.display_name not in [False, True, 0, 0.0, ""] else "-",
                'employe_periodictite': res.contract_id.periodicity_related if res.contract_id.periodicity_related not in [False, True, 0, 0.0, ""] else "-",
                'employe_embaucher_par': res.embaucher_par.name if res.embaucher_par.name not in [False, True, 0, 0.0, ""] else "-",
                'employe_recomander_par': res.recommander_par.name if res.recommander_par.name not in [False, True, 0, 0.0, ""] else "-",
                'employe_motif_embauche': res.motif_enbauche if res.motif_enbauche not in [False, True, 0, 0.0, ""] else "-",
                'employe_rib': res.rib_number.name if res.rib_number.name not in [False, True, 0, 0.0, ""] else "-",
                'employe_agence': res.rib_number.bank_agence if res.rib_number.bank_agence not in [False, True, 0, 0.0, ""] else "-",
                'employe_bank': res.rib_number.bank.name if res.rib_number.bank.name not in [False, True, 0, 0.0, ""] else "-",
                'employe_bank_ville': res.rib_number.ville_bank.name if res.rib_number.ville_bank.name not in [False, True, 0, 0.0, ""] else "-",
                'employe_mode_paiment': "-"
            })

            return data

        else:
            response_data = {
                'message': 'No data found for the given criteria',
                'timestamp': datetime.now().isoformat()
            }
            return json.dumps(response_data)
