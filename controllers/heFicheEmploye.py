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
        pointeur = http.request.env['res.users'].has_group("hr_management.group_pointeur")
        if res:

            genre = dict(res.fields_get(allfields=['gender'])['gender']['selection'])[res.gender]
            etat = dict(res.fields_get(allfields=['marital'])['marital']['selection'])[res.marital]

            data.append({
                'employe_name': res.name if res.name not in [False, True, 0, 0.0, ""] else "-",
                'employe_cin': res.cin if res.cin not in [False, True, 0, 0.0, ""] else "-",
                'employe_chantier': res.chantier_id.code + " - " + res.chantier_id.simplified_name.upper(),
                'employe_fonction': res.job if res.job not in [False, True, 0, 0.0, ""] else "-",
                'employe_cnss': res.cnss if res.cnss not in [False, True, 0, 0.0, ""] else "-",
                'employe_date_naissance': res.date_naissance if res.date_naissance not in [False, True, 0, 0.0, ""] else "-",
                'employe_val_cin': res.date_cin if res.date_cin not in [False, True, 0, 0.0, ""] else "-",
                'employe_lieu_naissance': res.lieu_naissance if res.lieu_naissance not in [False, True, 0, 0.0, ""] else "-",
                'employe_genre': genre if genre not in [False, True, 0, 0.0, ""] else "-",
                'employe_etat_civil': etat if etat not in [False, True, 0, 0.0, ""] else "-",
                'employe_nbr_enfant': str(res.nombre_enfants) if str(res.nombre_enfants) not in [False, True, ""] else "-",
                'employe_num_tele': res.mobile_phone if res.mobile_phone not in [False, True, 0, 0.0, ""] else "-",
                'employe_type': res.type_emp if res.type_emp not in [False, True, 0, 0.0, ""] else "-",
                'employe_contract_type': res.contract_id.contract_type.name if res.contract_id.contract_type.name not in [False, True, 0, 0.0, ""] else "-",
                'employe_salaire': res.contract_id.wage if res.contract_id.wage not in [False, True, 0, 0.0, ""] and not pointeur else "-",
                'employe_contract_debut': res.contract_id.date_start if res.contract_id.date_start not in [False, True, 0, 0.0, ""] else "-",
                'employe_contract_fin': res.contract_id.date_end if res.contract_id.date_end not in [False, True, 0, 0.0, ""] else "-",
                'employe_profile_paie': res.contract_id.profile_paie_id.display_name if res.contract_id.profile_paie_id.display_name not in [False, True, 0, 0.0, ""] and not pointeur else "-",
                'employe_periodictite':dict(res.fields_get(allfields=['periodicity_related'])['periodicity_related']['selection'])[res.contract_id.periodicity_related].upper()  if res.contract_id.periodicity_related not in [False, True, 0, 0.0, ""] else "-",
                'employe_embaucher_par': res.embaucher_par.name if res.embaucher_par.name not in [False, True, 0, 0.0, ""] else "-",
                'employe_recomander_par': res.recommander_par.name if res.recommander_par.name not in [False, True, 0, 0.0, ""] else "-",
                'employe_motif_embauche': res.motif_enbauche if res.motif_enbauche not in [False, True, 0, 0.0, ""] else "-",
                'employe_rib': res.rib_number.name if res.rib_number.name not in [False, True, 0, 0.0, ""] else "-",
                'employe_agence': res.rib_number.bank_agence if res.rib_number.bank_agence not in [False, True, 0, 0.0, ""] else "-",
                'employe_bank': res.rib_number.bank.name if res.rib_number.bank.name not in [False, True, 0, 0.0, ""] else "-",
                'employe_bank_ville': res.rib_number.ville_bank.name if res.rib_number.ville_bank.name not in [False, True, 0, 0.0, ""] else "-",
                'employe_mode_paiment': res.rib_number.payement_mode_id.name if res.rib_number.payement_mode_id.name not in [False, True, 0, 0.0, ""] else "-",
            })

            return data

        else:
            response_data = {
                'message': 'No data found for the given criteria',
                'timestamp': datetime.now().isoformat()
            }
            return json.dumps(response_data)
