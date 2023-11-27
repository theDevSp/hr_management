from odoo import http
import json
from datetime import datetime
from itertools import groupby


class HrDashboardControllers(http.Controller):

    @http.route('/hr_management/dashboard/', type='json', auth='user')
    def get_dashboard_details(self, chantier_id, period_id, periodicite, equipe):

        try:

            period_id = int(period_id)
            chantier_id = int(chantier_id)

            domains = [('period_id', '=', period_id),
                       ('chantier_id', '=', chantier_id),
                       ('quinzaine', '=', periodicite)
                       ]

            if equipe:
                equipe = int(equipe)
                domains.append(('emplacement_chantier_id', '=', equipe))

            payslips = http.request.env['hr.payslip'].search(domains)

            data = []

            if payslips:

                # Sort the payslips by emplacement_chantier_id
                payslips = payslips.sorted(
                    key=lambda r: r.emplacement_chantier_id.id)

                for key, group in groupby(payslips, key=lambda r: (r.emplacement_chantier_id.name, r.emplacement_chantier_id.id)):
                    payslips_group = list(group)

                    name, id_ = key

                    member_count = len(payslips_group)
                    rapport_total, rapport_total_done, rapport_total_draft = 0, 0, 0

                    for payslip in payslips_group:
                        if payslip.rapport_id:
                            rapport_total += 1
                            if payslip.rapport_id.state == 'draft':
                                rapport_total_draft += 1
                            if payslip.rapport_id.state == 'done':
                                rapport_total_done += 1

                    payroll_details = []

                    payroll_count, payroll_payment, payroll_refund, payroll_stc, payroll_blocked = 0, 0, 0, 0, 0
                    montant_total, montant_sad, montant_net_paye = 0, 0, 0

                    for paie in payslips_group:

                        payroll_count += 1
                        montant_total += paie.total
                        montant_sad += paie.sad
                        montant_net_paye += paie.net_pay

                        if paie.type_fiche == 'payroll' and paie.state in ('done', 'approved'):
                            payroll_payment += 1
                        if paie.type_fiche == 'refund' and paie.state in ('done', 'approved'):
                            payroll_refund += 1
                        if paie.type_fiche == 'stc' and paie.state in ('done', 'approved'):
                            payroll_stc += 1
                        if paie.state == 'blocked':
                            payroll_blocked += 1

                        payroll_details.append({
                            "payroll_id": paie.id,
                            "employee_obj": [
                                paie.employee_id.id,
                                paie.employee_id.name,
                                paie.employee_id.cin,
                                paie.employee_id.job_id.name,
                            ],
                            "net_paye": round(paie.net_pay),
                            "status": paie.state
                        })

                    obj = {
                        'id': id_,
                        'chantierID': chantier_id,
                        'periodID': period_id,
                        'quinz': periodicite,
                        'equipe': [id_, name],
                        'resume_rapport': {
                            'member_count': member_count,
                            'total': rapport_total,
                            'done': rapport_total_done,
                            'draft': rapport_total_draft,
                        },
                        'resume_payroll': {
                            'payroll_count': payroll_count,
                            'payement': payroll_payment,
                            'refund': payroll_refund,
                            'stc': payroll_stc,
                            'blocked': payroll_blocked,
                            'montant_total': round(montant_total),
                            'montant_sad': round(montant_sad),
                            'montant_net_paye': round(montant_net_paye)
                        },
                        'payroll_details': payroll_details
                    }
                    data.append(obj)

                return {
                    'code': 200,
                    'message': "Les détails de l'équipe ont été mis à jour avec succès",
                    'timestamp': datetime.now().isoformat(),
                    'data': data
                }

            else:
                response_data = {
                    'code': 202,
                    'message': "Une erreur s'est produite, veuillez réessayer !",
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

    @http.route('/hr_management/dashboard/update_fp_status/', type='json', auth='user')
    def update_fp_status(self, id, status):
        try:

            fp_record = http.request.env['hr.payslip'].sudo().browse(id)

            if fp_record.exists():

                fp_record.write({'state': status})

                data = {
                    'code': 200,
                    'message': 'Statut mis à jour avec succès',
                    'timestamp': datetime.now().isoformat(),
                    'ligne': {
                        "payroll_id": fp_record.id,
                        "employee_obj": [
                            fp_record.employee_id.id,
                            fp_record.employee_id.name,
                            fp_record.employee_id.cin,
                            fp_record.employee_id.job_id.name,
                        ],
                        "net_paye": round(fp_record.net_pay),
                        "status": fp_record.state
                    }
                }
                return data

            else:
                response_data = {
                    'code': 202,
                    'message': "Statut n'est pas mis à jour avec succès",
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

    @http.route('/hr_management/dashboard/update_all_fp_status', type='json', auth='user')
    def update_all_fp_status(self, ids, status):

        try:

            fp_record = http.request.env['hr.payslip'].sudo().browse(ids)

            if fp_record.exists():

                data = []

                for record in fp_record:

                    record.write({'state': status})

                    data.append(
                        {
                            "payroll_id": record.id,
                            "employee_obj": [
                                record.employee_id.id,
                                record.employee_id.name,
                                record.employee_id.cin,
                                record.employee_id.job_id.name,
                            ],
                            "net_paye": round(record.net_pay),
                            "status": record.state
                        }
                    )

                return {
                    'code': 200,
                    'message': 'Statut mis à jour avec succès',
                    'timestamp': datetime.now().isoformat(),
                    'lignes': data
                }

            else:
                response_data = {
                    'code': 202,
                    'message': "Statut n'est pas mis à jour avec succès",
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

    @http.route('/hr_management/dashboard/delete_reports', type='json', auth='user')
    def delete_reports(self, chantier_id, period_id, periodicite, equipe):
        try:
            period_id = int(period_id)
            chantier_id = int(chantier_id)
            equipe = int(equipe)

            query = """
                DELETE FROM hr_rapport_pointage
                WHERE period_id = %s
                AND chantier_id = %s
                AND quinzaine = %s
                AND emplacement_chantier_id = %s
                AND total_h = 0
                AND total_j = 0
            """

            params = (period_id, chantier_id, periodicite, equipe)
            cr = http.request.env.cr

            cr.execute(query, params)
            count_deleted = cr.rowcount

            if count_deleted > 0:
                return {
                    'code': 200,
                    'message': f'Les rapports vides ont été supprimés avec succès : {count_deleted} rapport supprimé',
                    'timestamp': datetime.now().isoformat(),
                }
            else:
                return {
                    'code': 202,
                    'message': "Il n'y a aucun rapport vide à supprimer.",
                    'timestamp': datetime.now().isoformat(),
                }

        except Exception as e:
            error_message = {
                'code': 504,
                'error': f'An error occurred while processing the request. {e}',
                'message': "Une erreur s'est produite, veuillez réessayer !",
                'timestamp': datetime.now().isoformat()
            }
            return error_message
