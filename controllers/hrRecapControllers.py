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
            sum_total_recap_lines = 0

            for rec_line in recap.line_ids:

                recap_montant_total = sum(entry.get('total', 0) for entry in rec_line.json_data)
                sum_total_recap_lines += recap_montant_total
                
                recap_lines.append({
                    'recap_chantier': rec_line.chantier_id.simplified_name,
                    'recap_equipe': rec_line.emplacement_chantier_id.abrv,
                    'recap_nbr_effectif': rec_line.nombre_effectif,
                    'recap_montant_total': recap_montant_total,
                    'recap_mode_payes_total': rec_line.json_data
                })
            
            quinzine = ""
            if recap.quinzaine == "quinzaine1":
                quinzine = "Première Quinzaine"
            elif recap.quinzaine == "quinzaine2":
                quinzine = "Deuxième Quinzaine"
            elif recap.quinzaine == "quinzaine12":
                quinzine = "Q1 + Q2"

            data = {
                'recap_name': recap.name,
                'recap_period': recap.period_id.code,
                'recap_quinzaine': quinzine,
                'recap_type_emp': 'Ouvrier' if recap.type_emp == 'o' else ('Salarié' if recap.type_emp == 's' else 'Non défini'),
                'recap_responsable': recap.responsable_id.name,
                'recap_lines': recap_lines,
                'recap_lines_total': round(sum_total_recap_lines)
            }
            return data
        else:
            response_data = {
                'message': 'Aucune donnée trouvée pour ces critères',
                'timestamp': datetime.now().isoformat()
            }
            return response_data
