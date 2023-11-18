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
            total_recap_lines, total_virement, total_versement, total_espece = 0, 0, 0, 0

            for rec_line in recap.line_ids:

                recap_montant_total = sum(entry.get('total', 0)
                                          for entry in rec_line.json_data)
                sum_virement = sum(entry.get(
                    'total', 0) for entry in rec_line.json_data if entry.get('mode') == "Virement")
                sum_versement = sum(entry.get(
                    'total', 0) for entry in rec_line.json_data if entry.get('mode') == "Versement")
                sum_espece = sum(entry.get(
                    'total', 0) for entry in rec_line.json_data if entry.get('mode') == "Espece")

                total_recap_lines += recap_montant_total
                total_virement += sum_virement
                total_versement += sum_versement
                total_espece += sum_espece

                formatted_recap_mode_payes_total = [
                    {'mode': entry['mode'], 'total': '{:,}'.format(entry['total']).replace(',', ' ')}
                    for entry in rec_line.json_data
                ]


                recap_lines.append({
                    'recap_chantier': rec_line.chantier_id.name,
                    'recap_equipe': rec_line.emplacement_chantier_id.abrv,
                    'recap_nbr_effectif': rec_line.nombre_effectif,
                    'recap_montant_total': '{:,}'.format(round(recap_montant_total)).replace(',', ' '),
                    'recap_mode_payes_total': formatted_recap_mode_payes_total
                })

            quinzine_mapping = {'quinzaine1': 'Première Quinzaine',
                                'quinzaine2': 'Deuxième Quinzaine',
                                'quinzaine12': 'Q1 + Q2'}

            data = {
                'recap_name': recap.name,
                'recap_period': recap.period_id.code,
                'recap_quinzaine': quinzine_mapping.get(recap.quinzaine, ''),
                'recap_type_emp': 'Ouvrier' if recap.type_emp == 'o' else ('Salarié' if recap.type_emp == 's' else 'Non défini'),
                'recap_responsable': recap.responsable_id.name,
                'recap_lines': recap_lines,
                'recap_lines_total': f'{round(total_recap_lines):,}'.replace(',', ' '),
                'recap_total_virement': f'{round(total_virement):,}'.replace(',', ' '),
                'recap_total_versement': f'{round(total_versement):,}'.replace(',', ' '),
                'recap_total_espece': f'{round(total_espece):,}'.replace(',', ' ')
            }
            return data
        else:
            response_data = {
                'message': 'Aucune donnée trouvée pour ces critères',
                'timestamp': datetime.now().isoformat()
            }
            return response_data
