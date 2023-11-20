from odoo import http
import json
from datetime import datetime
from odoo.http import request
from odoo.tools import html2plaintext
from itertools import groupby
from operator import itemgetter

from colorama import Fore, Back, Style


class HrDashboardControllers(http.Controller):

    @http.route('/hr_management/dashboard/', type='json', auth='user')
    def get_dashboard_details(self, chantier_id, period_id, periodicite):

        period_id = int(period_id)
        chantier_id = int(chantier_id)

        domains = [('period_id', '=', period_id),
                   ('chantier_id', '=', chantier_id),
                   ('quinzaine', '=', periodicite)]

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

            return data
        
        else:
            response_data = {
                'message': 'No data found for the given criteria',
                'timestamp': datetime.now().isoformat()
            }
            return json.dumps(response_data)

