from odoo import http

from dateutil.relativedelta import relativedelta
import json
from datetime import datetime
from itertools import groupby


class hrConducteurDashboardControllers(http.Controller):

    def get_previous_period(self, date):
        res = http.request.env["account.month.period"].search(
            [('date_stop', '>=', date), ('date_start', '<=', date)], limit=1)
        return res[0] if len(res) > 0 else []

    @http.route('/hr_management/conducteur-dashboard/', type='json', auth='user')
    def get_chantiers_data_details(self, chantier_id, period_id):

        try:
            periode_id = int(period_id)
            chantier_id = int(chantier_id)

            chantier = http.request.env['fleet.vehicle.chantier'].sudo().browse(
                chantier_id)

            periode_actuelle = http.request.env['account.month.period'].sudo().browse(
                periode_id)

            periode_precedente = self.get_previous_period(
                periode_actuelle.date_start - relativedelta(months=1)
            )

            periode_courante = periode_actuelle
            periode_precedente = periode_precedente

            lignes_rapports = http.request.env['hr.rapport.pointage.line'].sudo().search([
                ('day',
                 '>=', periode_precedente.date_start),
                ('day', '<=', periode_courante.date_stop),
                ('chantier_id', '=', chantier_id)
            ])

            if lignes_rapports:

                rapports_lignes_periode_courante = lignes_rapports.filtered(
                    lambda ln: periode_courante.date_start <= ln.day <= periode_courante.date_stop
                )

                rapports_lignes_periode_precedente = lignes_rapports.filtered(
                    lambda ln: periode_precedente.date_start <= ln.day <= periode_precedente.date_stop
                )

                rapports_lignes_periode_courante_salaries = rapports_lignes_periode_courante.filtered(
                    lambda ln: ln.rapport_id.type_emp == 's'
                )

                rapports_lignes_periode_courante_ouvriers = rapports_lignes_periode_courante.filtered(
                    lambda ln: ln.rapport_id.type_emp == 'o'
                )

                rapports_lignes_periode_precedente_salaries = rapports_lignes_periode_precedente.filtered(
                    lambda ln: ln.rapport_id.type_emp == 's'
                )

                rapports_lignes_periode_precedente_ouvriers = rapports_lignes_periode_precedente.filtered(
                    lambda ln: ln.rapport_id.type_emp == 'o'
                )

                total_heures_periode_salaries = sum(
                    float(ln.h_travailler) for ln in rapports_lignes_periode_courante_salaries
                )
                total_heures_derniere_periode_salaries = sum(
                    float(ln.h_travailler) for ln in rapports_lignes_periode_precedente_salaries
                )

                total_heures_periode_ouvriers = sum(
                    float(ln.h_travailler) for ln in rapports_lignes_periode_courante_ouvriers
                )
                total_heures_derniere_periode_ouvriers = sum(
                    float(ln.h_travailler) for ln in rapports_lignes_periode_precedente_ouvriers
                )

                total_salaires_periode_salaries = sum(
                    float(ln.h_travailler) *
                    ln.employee_id.salaire_heure_related
                    for ln in rapports_lignes_periode_courante_salaries
                )
                total_salaires_derniere_periode_salaries = sum(
                    float(ln.h_travailler) *
                    ln.employee_id.salaire_heure_related
                    for ln in rapports_lignes_periode_precedente_salaries
                )

                total_salaires_periode_ouvriers = sum(
                    float(ln.h_travailler) *
                    ln.employee_id.salaire_heure_related
                    for ln in rapports_lignes_periode_courante_ouvriers
                )
                total_salaires_derniere_periode_ouvriers = sum(
                    float(ln.h_travailler) *
                    ln.employee_id.salaire_heure_related
                    for ln in rapports_lignes_periode_precedente_ouvriers
                )

                count_salaries_derniere_periode = len(
                    set(ln.rapport_id.id for ln in rapports_lignes_periode_precedente_salaries if ln.rapport_id.chantier_id.id == chantier_id)
                )
                count_salaries_periode = len(
                    set(ln.rapport_id.id for ln in rapports_lignes_periode_courante_salaries if ln.rapport_id.chantier_id.id == chantier_id)
                )

                count_ouvriers_q1_derniere_periode = len(
                    set(ln.rapport_id.id for ln in rapports_lignes_periode_precedente_ouvriers if ln.rapport_id.quinzaine ==
                        'quinzaine1' and ln.rapport_id.chantier_id.id == chantier_id)
                )
                count_ouvriers_q1_periode = len(
                    set(ln.rapport_id.id for ln in rapports_lignes_periode_courante_ouvriers if ln.rapport_id.quinzaine ==
                        'quinzaine1' and ln.rapport_id.chantier_id.id == chantier_id)
                )

                count_ouvriers_q2_derniere_periode = len(
                    set(ln.rapport_id.id for ln in rapports_lignes_periode_precedente_ouvriers if ln.rapport_id.quinzaine ==
                        'quinzaine2' and ln.rapport_id.chantier_id.id == chantier_id)
                )
                count_ouvriers_q2_periode = len(
                    set(ln.rapport_id.id for ln in rapports_lignes_periode_courante_ouvriers if ln.rapport_id.quinzaine == 'quinzaine2' and ln.rapport_id.chantier_id.id == chantier_id))

                return {
                    'code': 200,
                    'message': 'Les données ont été chargées avec succès.',
                    'timestamp': datetime.now().isoformat(),
                    'periode_courante': periode_courante.code,
                    'periode_precedente': periode_precedente.code,
                    "chantier": chantier.code + " - " + chantier.simplified_name,
                    'total_heures_periode_salaries': total_heures_periode_salaries,
                    'total_heures_derniere_periode_salaries': total_heures_derniere_periode_salaries,
                    'total_heures_periode_ouvriers': total_heures_periode_ouvriers,
                    'total_heures_derniere_periode_ouvriers': total_heures_derniere_periode_ouvriers,
                    'total_salaires_periode_salaries': total_salaires_periode_salaries,
                    'total_salaires_derniere_periode_salaries': total_salaires_derniere_periode_salaries,
                    'total_salaires_periode_ouvriers': total_salaires_periode_ouvriers,
                    'total_salaires_derniere_periode_ouvriers': total_salaires_derniere_periode_ouvriers,
                    'count_salaries_derniere_periode': count_salaries_derniere_periode,
                    'count_salaries_periode': count_salaries_periode,
                    'count_ouvriers_q1_derniere_periode': count_ouvriers_q1_derniere_periode,
                    'count_ouvriers_q1_periode': count_ouvriers_q1_periode,
                    'count_ouvriers_q2_derniere_periode': count_ouvriers_q2_derniere_periode,
                    'count_ouvriers_q2_periode': count_ouvriers_q2_periode
                }
            else:
                response_data = {
                    'code': 202,
                    'message': "Aucune donnée à charger.",
                    'timestamp': datetime.now().isoformat()
                }
                return response_data

        except Exception as e:
            error_message = {
                'code': 504,
                'error': f'An error occurred while processing the request. {e}',
                'message': "Une erreur s'est produite, veuillez réessayer !",
                'timestamp': datetime.now().isoformat()
            }
            return error_message

    @http.route('/hr_management/conducteur-dashboard/effectif-postes', type='json', auth='user')
    def get_postes_details(self, chantier_id, period_id):
        try:

            periode_id = int(period_id)
            chantier_id = int(chantier_id)

            periode_actuelle = http.request.env['account.month.period'].sudo().browse(
                periode_id)

            periode_precedente = self.get_previous_period(
                periode_actuelle.date_start - relativedelta(months=1)
            )

            periode_courante = periode_actuelle
            periode_precedente = periode_precedente

            query = """
                        select json_agg(e) from (
                            SELECT
                                v.job,
                                MIN(CAST(e.name AS VARCHAR)) AS job_name,
                                COUNT(1) FILTER (WHERE v.periode = %s) AS count_current,
                                COUNT(1) FILTER (WHERE v.periode = %s) AS count_before
                            FROM total_rapport v
                            LEFT JOIN hr_job e ON v.job = e.id
                            WHERE
                                v.chantier = %s
                            GROUP BY
                                v.job
                            ORDER BY
                                job_name ASC
                        ) e
                    """ % (periode_courante.id, periode_precedente.id, chantier_id)
            http.request.cr.execute(query)

            results = http.request.cr.fetchall()[0][0]
            res = []

            if results:
                for obj in results:
                    if obj['job_name'] is not None and obj['job'] is not None:
                        posteName = json.loads(obj['job_name'])
                        row = [
                            posteName['en_US'],
                            obj['count_before'],
                            obj['count_current'],
                        ]
                        res.append(row)

                return {
                    'code': 200,
                    'message': 'Les données ont été chargées avec succès.',
                    'timestamp': datetime.now().isoformat(),
                    'periode_actuelle':  periode_actuelle.code,
                    'periode_precedente':  periode_precedente.code,
                    'postesData': res
                }

            else:
                response_data = {
                    'code': 202,
                    'message': "Aucune donnée à charger",
                    'timestamp': datetime.now().isoformat()
                }
                return response_data

        except Exception as e:
            print("Error -> ", e)
            error_message = {
                'code': 504,
                'error': f'An error occurred while processing the request. {e}',
                'message': "Une erreur s'est produite, veuillez réessayer !",
                'timestamp': datetime.now().isoformat()
            }
            return error_message

    @http.route('/hr_management/conducteur-dashboard/equipes', type='json', auth='user')
    def get_equipes_data_details(self, chantier_id, period_id):
        try:
            chantier_id, period_id = int(chantier_id), int(period_id)

            chantier = http.request.env['fleet.vehicle.chantier'].sudo().browse(
                chantier_id)
            periode = http.request.env['account.month.period'].sudo().browse(
                period_id)

            lignes_rapports = http.request.env['hr.rapport.pointage.line'].sudo().search([
                ('day', '>=', periode.date_start),
                ('day', '<=', periode.date_stop),
                ('chantier_id', '=', chantier_id)
            ])

            id = 0

            equipes_data = {}

            for line in lignes_rapports:
                equipe = line.emplacement_chantier_id.name
                equipes_data.setdefault(equipe, []).append(line)

            data = []

            for equipe, data_list in equipes_data.items():

                rapports_salaries = [
                    ligne for ligne in data_list if ligne.rapport_id.type_emp == 's' and ligne.rapport_id.chantier_id.id == chantier_id]
                rapports_ouvriers = [
                    ligne for ligne in data_list if ligne.rapport_id.type_emp == 'o' and ligne.rapport_id.chantier_id.id == chantier_id]

                rapports_cadre = [
                    ligne for ligne in data_list if ligne.rapport_id.type_emp == False and ligne.rapport_id.chantier_id.id == chantier_id]

                total_heures_salaries = sum(
                    float(ln.h_travailler) for ln in rapports_salaries if ln.rapport_id.chantier_id.id == chantier_id)
                total_heures_ouvriers = sum(
                    float(ln.h_travailler) for ln in rapports_ouvriers if ln.rapport_id.chantier_id.id == chantier_id)

                total_salaires_salaries = sum(float(ln.h_travailler) * ln.employee_id.salaire_heure_related
                                              for ln in rapports_salaries if ln.rapport_id.chantier_id.id == chantier_id)

                total_salaires_ouvriers = sum(float(ln.h_travailler) * ln.employee_id.salaire_heure_related
                                              for ln in rapports_ouvriers if ln.rapport_id.chantier_id.id == chantier_id)

                count_salaries = {ln.employee_id.id for ln in rapports_salaries if ln.rapport_id.quinzaine == 'quinzaine12'
                                  and ln.rapport_id.chantier_id.id == chantier_id}

                count_ouvriers = {ln.employee_id.id for ln in rapports_ouvriers
                                  if ln.rapport_id.quinzaine in ('quinzaine1', 'quinzaine2')
                                  and ln.rapport_id.chantier_id.id == chantier_id}

                salarier_employee_data = {}
                for line in rapports_salaries:
                    employee = line.employee_id.name
                    salarier_employee_data.setdefault(
                        employee, []).append(line)

                salaries_data = []

                for employee, data_list in salarier_employee_data.items():
                    total_heure = 0
                    total_a_payer = 0.0

                    for ligne in data_list:
                        total_heure += float(ligne.h_travailler)
                        total_a_payer += float(float(ligne.h_travailler) *
                                               float(ligne.employee_id.salaire_heure_related))

                    employee_info = {
                        'employe_name': employee,
                        'employe_cin': data_list[0].employee_id.cin,
                        'employe_poste': data_list[0].employee_id.job_id.name,
                        'employe_total_heure': total_heure,
                        'employe_total_a_payer': total_a_payer,
                    }

                    salaries_data.append(employee_info)

                ouvrier_employee_data = {}
                for line in rapports_ouvriers:
                    employee = line.employee_id.name
                    ouvrier_employee_data.setdefault(
                        employee, []).append(line)

                ouvriers_data = []

                for employee, data_list in ouvrier_employee_data.items():
                    total_heure = 0
                    total_a_payer = 0.0

                    for ligne in data_list:
                        total_heure += float(ligne.h_travailler)
                        total_a_payer += float(float(ligne.h_travailler) *
                                               float(ligne.employee_id.salaire_heure_related))

                    employee_info = {
                        'employe_name': employee,
                        'employe_cin': data_list[0].employee_id.cin,
                        'employe_poste': data_list[0].employee_id.job_id.name,
                        'employe_total_heure': total_heure,
                        'employe_total_a_payer': total_a_payer,
                    }

                    ouvriers_data.append(employee_info)

                cadre_employee_data = {}
                for line in rapports_cadre:
                    employee = line.employee_id.name
                    cadre_employee_data.setdefault(
                        employee, []).append(line)

                cadres_data = []

                for employee, data_list in cadre_employee_data.items():
                    total_heure = 0
                    total_a_payer = 0.0

                    for ligne in data_list:
                        total_heure += float(ligne.h_travailler)
                        total_a_payer += float(float(ligne.h_travailler) *
                                               float(ligne.employee_id.salaire_heure_related))

                    employee_info = {
                        'employe_name': employee,
                        'employe_cin': data_list[0].employee_id.cin,
                        'employe_poste': data_list[0].employee_id.job_id.name,
                        'employe_total_heure': total_heure,
                        'employe_total_a_payer': total_a_payer,
                    }

                    cadres_data.append(employee_info)

                id += 1
                data.append({
                    'equipe': equipe,
                    'equipeID': id,
                    'total_salaires_ouvriers': total_salaires_ouvriers,
                    'total_salaires_salaries': total_salaires_salaries,
                    'total_heures_ouvriers': total_heures_ouvriers,
                    'total_heures_salaries': total_heures_salaries,
                    'count_salaries': len(count_salaries),
                    'count_ouvriers': len(count_ouvriers),
                    'salaries_data': salaries_data,
                    'ouvriers_data': ouvriers_data,
                    'equipes_data': equipes_data,
                    'cadres_data': cadres_data
                })

            if lignes_rapports:
                return {
                    'code': 200,
                    'message': 'Les données ont été chargées avec succès.',
                    'timestamp': datetime.now().isoformat(),
                    'data': data,
                    'chantier': chantier.simplified_name,
                    'periode': periode.code
                }
            else:
                response_data = {
                    'code': 202,
                    'message': "Aucune donnée à charger.",
                    'timestamp': datetime.now().isoformat()
                }
                return response_data

        except Exception as e:
            error_message = {
                'code': 504,
                'error': f'An error occurred while processing the request. {e}',
                'message': "Une erreur s'est produite, veuillez réessayer !",
                'timestamp': datetime.now().isoformat()
            }
            return error_message
