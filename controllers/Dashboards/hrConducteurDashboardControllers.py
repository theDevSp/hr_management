from odoo import http

from dateutil.relativedelta import relativedelta
import json
from datetime import datetime


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
            error_message = {
                'code': 504,
                'error': f'An error occurred while processing the request. {e}',
                'message': "Une erreur s'est produite, veuillez réessayer !",
                'timestamp': datetime.now().isoformat()
            }
            return error_message
