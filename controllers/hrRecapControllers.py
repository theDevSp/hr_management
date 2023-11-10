from odoo import http
from odoo.http import request
import json
from datetime import datetime
from collections import defaultdict


class hrRecapControllers(http.Controller):

    @http.route('/hr_management/get_recap_details/<int:id>', type='json', auth='user')
    def get_recap_details(self, id):
        recap = request.env['hr.recap.pdf'].browse(id)

        if recap:
            recap_lines = []

            for rec_line in recap.line_ids:
                fiche_paie = []
                paie_totals = {}

                paie = request.env['hr.payslip'].search([
                    ('chantier_id', '=', rec_line.chantier_id.id),
                    ('type_emp', '=', recap.type_emp),
                    ('period_id', '=', recap.period_id.id),
                    ('quinzaine', '=', recap.quinzaine)
                ])

                for p in paie:
                    fiche_paie.append({
                        'id': p.id,
                        'emp': p.employee_id.name,
                        'paie': p.employee_id.rib_number.payement_mode_id.name,
                        'nap': float(p.net_pay)
                    })

                    # Calculate sum of 'nap' for each 'paie' in fiche_paie
                    if p.employee_id.rib_number.payement_mode_id.name in paie_totals:
                        paie_totals[p.employee_id.rib_number.payement_mode_id.name] += float(
                            p.net_pay)
                    else:
                        paie_totals[p.employee_id.rib_number.payement_mode_id.name] = float(
                            p.net_pay)

                recap_lines.append({
                    'recap_chantier': rec_line.chantier_id.name,
                    'recap_equipe': rec_line.emplacement_chantier_id.abrv,
                    'recap_nbr_effectif': rec_line.nombre_effectif,
                    'recap_montant_total': rec_line.montant_total,
                    'fiche_paie': fiche_paie,
                    'paie_totals': paie_totals  # Include paie_totals in fiche_paie
                })

            data = {
                'recap_name': recap.name,
                'recap_period_id': recap.period_id.code,
                'recap_quinzaine': recap.quinzaine,
                'recap_type_emp': recap.type_emp,
                'recap_responsable': recap.responsable_id.name,
                'recap_lines': recap_lines
            }
            return data
        else:
            response_data = {
                'message': 'Aucune donnée trouvée pour ces critères',
                'timestamp': datetime.now().isoformat()
            }
            return response_data
