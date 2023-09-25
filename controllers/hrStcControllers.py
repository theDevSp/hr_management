from odoo import http
from odoo.exceptions import UserError
from odoo.http import request, Controller, route


class stcController(http.Controller):

    @http.route('/hr_management/get_stc/<int:id>', type='json', auth='user')
    def get_stc_by_id(self, id):

        try:
            if not id:
                raise UserError('Invalid ID')

            stc_record = request.env['hr.stc'].sudo().search(
                [('id', '=', id)], limit=1)

            if not stc_record:
                raise UserError('Record not found')
            
            prime = stc_record.prime + stc_record.sum_prime

            data = {
                'stc_reference': stc_record.name if stc_record.name not in [False, True, 0, ""] else "-",
                'stc_date': stc_record.date_debut if stc_record.date_debut not in [False, True, 0, ""] else "-",
                'stc_employee_nom_prenom': stc_record.employee_id.name if stc_record.employee_id.name not in [False, True, 0, ""] else "-",
                'stc_employee_cin': stc_record.employee_id.cin if stc_record.employee_id.cin not in [False, True, 0, ""] else "-",
                'stc_employee_fonction': stc_record.job if stc_record.job not in [False, True, 0, ""] else "-",
                'stc_employee_salaire': stc_record.salaire if stc_record.salaire not in [False, True, 0, "-"] else "-",
                'stc_employee_bank': stc_record.bank if stc_record.bank not in [False, True, 0, ""] else "-",
                'stc_employee_paiment': dict(stc_record.fields_get(allfields=['modePay'])['modePay']['selection'])[stc_record.modePay] if stc_record.modePay not in [False, True, 0, ""] else "-",
                'stc_employee_periode': f"{stc_record.date_start} AU {stc_record.date_fin}" if (stc_record.date_start, stc_record.date_fin) != (False, True, 0, "") else "-",
                'stc_par_ordre': dict(stc_record.fields_get(allfields=['ordre'])['ordre']['selection'])[stc_record.ordre] if stc_record.ordre not in [False, True, 0, ""] else "-",
                'stc_employee_chantier': stc_record.chantier_id.simplified_name if stc_record.chantier_id.simplified_name not in [False, True, 0, ""] else "-",
                'stc_employee_poste': stc_record.job_id.name if stc_record.job_id.name not in [False, True, 0, ""] else "-",
                'stc_employee_numero': stc_record.count_by_year if stc_record.count_by_year not in [False, True, 0, ""] else "-",
                'stc_panier_conges_jours': stc_record.jr_conge if stc_record.jr_conge not in [False, True, 0, ""] else "",
                'stc_panier_conges_dh': "{:.2f}".format(stc_record.jr_conge_m) if stc_record.jr_conge_m not in [False, True, 0, ""] else "",
                'stc_nbr_dimanche_jours': stc_record.jr_dim if stc_record.jr_dim not in [False, True, 0, ""] else "",
                'stc_nbr_dimanche_dh': "{:.2f}".format(stc_record.montant_dim) if stc_record.montant_dim not in [False, True, 0, ""] else "",
                'stc_preavis_ajouter_jours': stc_record.preavis_ajouter if stc_record.preavis_ajouter not in [False, True, 0, ""] else "",
                'stc_preavis_ajouter_dh': "{:.2f}".format(stc_record.preavis_ajouter_m) if stc_record.preavis_ajouter_m not in [False, True, 0, ""] else "",
                'stc_liceciment': "{:.2f}".format(stc_record.licenciement) if stc_record.licenciement not in [False, True, 0, ""] else "",
                'stc_frais_de_depence': "{:.2f}".format(stc_record.frais_depense) if stc_record.frais_depense not in [False, True, 0, ""] else "",
                'stc_frais_de_route': "{:.2f}".format(stc_record.frais_route) if stc_record.frais_route not in [False, True, 0, ""] else "",
                'stc_prime': "{:.2f}".format(prime) if prime not in [False, True, 0, ""] else "",
                'stc_rest_salaire': "{:.2f}".format(stc_record.reste_salaire) if stc_record.reste_salaire not in [False, True, 0, ""] else "",
                'stc_preavis_retenir_jours': stc_record.preavis_retenu if stc_record.preavis_retenu not in [False, True, 0, ""] else "",
                'stc_preavis_retenir_dh': "{:.2f}".format(stc_record.preavis_retenu_m) if stc_record.preavis_retenu_m not in [False, True, 0, ""] else "",
                'stc_amende': "{:.2f}".format(stc_record.amande) if stc_record.amande not in [False, True, 0, ""] else "",
                'stc_cotisation_cimr': "{:.2f}".format(stc_record.cimr) if stc_record.cimr not in [False, True, 0, ""] else "",
                'stc_prelevement': "{:.2f}".format(stc_record.retenu) if stc_record.retenu not in [False, True, 0, ""] else "",
                'stc_prelevement_credit': "{:.2f}".format(stc_record.sum_prelevement) if stc_record.sum_prelevement not in [False, True, 0, ""] else "",
                'stc_notes': stc_record.notes if stc_record.notes not in [False, True, 0, ""] else "",
                'stc_montant_apayer': round(stc_record.montant_total) if stc_record.montant_total not in [False, True, 0, ""] else "",
                'stc_montant_valider': round(stc_record.valide_salaire) if stc_record.valide_salaire not in [False, True, 0, ""] else "",
            }

            return data

        except UserError as e:
            return {'error': str(e)}
