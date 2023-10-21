from odoo import http
import json
from datetime import datetime
from odoo.http import request
from odoo.tools import html2plaintext
from itertools import groupby


class HrFicheDePaieController(http.Controller):

    @http.route('/hr_management/get_fiche_de_paie_details/', type='http', auth='user', methods=['POST'], csrf=False)
    def get_fiche_de_paie_details(self):

        post = json.loads(request.httprequest.data.decode('utf-8'))

        chantier_id = post.get("chantier")
        period_id = post.get("date")
        quinz = post.get("quinzine")
        equipe_id = post.get("equipe")
        type_employe = post.get("typeemp")

        period_id = int(period_id)
        chantier_id = int(chantier_id)

        domains = [('period_id', '=', period_id),
                   ('chantier_id', '=', chantier_id)]

        if quinz:
            domains.append(('quinzaine', '=', quinz))

        if equipe_id:
            equipe_id = int(equipe_id)
            domains.append(('emplacement_chantier_id', '=', equipe_id))

        if type_employe:
            domains.append(('type_emp', '=', type_employe))

        payslips = http.request.env['hr.payslip'].search(domains)
        chantier = http.request.env['fleet.vehicle.chantier'].browse(
            chantier_id)  # chantier_id
        period = http.request.env['account.month.period'].browse(
            period_id)  # period_id

        if payslips:

            res = sorted(
                payslips, key=lambda re: re.emplacement_chantier_id.name)
            final = []

            for group_key, group in groupby(res, key=lambda re: re.emplacement_chantier_id.name):
                obj = {
                    "equipe": group_key.upper(),
                    "data": []
                }

                total_employe_total = 0
                total_employe_deduction = 0
                total_employe_cotisation = 0
                total_employe_sad = 0
                total_employe_nap = 0
                total_employe_addition = 0

                for grp in group:

                    if grp.employee_id.cotisation:
                        cotisation = grp.employee_id.montant_cimr
                    else:
                        cotisation = 0

                    if grp.employee_id.type_profile_related == 'j':
                        total = grp.salaire_jour * grp.nbr_jour_travaille
                        jours_heure = grp.nbr_jour_travaille
                    elif grp.employee_id.type_profile_related == 'h':
                        total = grp.salaire_heure * grp.nbr_heure_travaille
                        jours_heure = grp.nbr_heure_travaille
                    else:
                        jours_heure = 0
                        total = 0

                    if grp.type_fiche == 'stc' and grp.state == 'blocked':
                        salaire_sad = 0
                        salaire_nap = 0
                    else:
                        salaire_sad = total - (cotisation + grp.deduction)
                        salaire_nap = salaire_sad + grp.addition

                    data_entry = {
                        'ref': grp.name or "",
                        'employe_name': grp.employee_id.name or "",
                        'employe_cin': grp.employee_id.cin or "",
                        'employe_fonction': grp.employee_id.job_id.name or "",
                        'employe_type': grp.type_emp or "",
                        'employe_code_engin': grp.employee_id.vehicle_id.code or "",
                        'employe_date_embauche': grp.employee_id.date_start.strftime("%d-%m-%Y") if grp.employee_id.date_start else "",
                        'employe_panier_cp': grp.cp_number or 0,
                        'employe_profile_de_paie': grp.employee_id.name_profile_related or "",
                        'employe_bank': grp.employee_id.bank.name or "",
                        'employe_salaire_de_base': grp.salaire_actuel or 0,
                        'employe_deduction': grp.deduction or 0,
                        'employe_cotisation': cotisation or 0,
                        'employe_jours_heure': jours_heure or 0,
                        'employe_total': total or 0,
                        'employe_prime_ftor': grp.addition or 0,
                        'employe_sad': salaire_sad or 0,
                        'employe_nap': salaire_nap or 0,
                        'observation': "" if html2plaintext(grp.notes) == 'False' else html2plaintext(grp.notes)
                    }

                    total_employe_total += data_entry['employe_total']
                    total_employe_deduction += data_entry['employe_deduction']
                    total_employe_cotisation += data_entry['employe_cotisation']
                    total_employe_sad += data_entry['employe_sad']
                    total_employe_nap += data_entry['employe_nap']
                    total_employe_addition += data_entry['employe_prime_ftor']

                    obj["data"].append(data_entry)
                

                obj["total_employe_total"] = total_employe_total
                obj["total_employe_deduction"] = total_employe_deduction
                obj["total_employe_cotisation"] = total_employe_cotisation
                obj["total_employe_sad"] = total_employe_sad
                obj["total_employe_nap"] = total_employe_nap
                obj["total_employe_addition"] = total_employe_addition
                final.append(obj)

            
            if quinz == "quinzaine1":
                quinzine = "Première Quinzaine"
            elif quinz == "quinzaine2":
                quinzine = "Deuxième Quinzaine"
            elif quinz == "quinzaine12":
                quinzine = "Q1 + Q2"
            
            return http.request.make_json_response(data={
                "chantier": chantier.name.upper(),
                "periode": period.name.upper(),
                "quinzine": quinzine,
                "type": 'Salariées' if type_employe == 's' else 'Ouvriers',
                'payslips': final,
            }, status=200)
        else:
            return http.request.make_json_response(data={'message': 'No data found'}, status=204)

