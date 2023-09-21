from odoo import http
from odoo.http import request

import json
from datetime import datetime


class printReportPointageController(http.Controller):
    @http.route('/hr_management/pointage/get_all_chantiers', type='json', auth='user')
    def get_all_chantier(self):

        chantier_records = http.request.env['fleet.vehicle.chantier'].search([])

        data = []

        for record in chantier_records:

            data.append({
                'id': record.id,
                'name': record.name,
            })

        return data

    @http.route('/hr_management/pointage/get_all_Equipes', type='json', auth='user')
    def get_all_equipe(self):

        equipe_records = http.request.env['fleet.vehicle.chantier.emplacement'].search([])

        data = []

        for record in equipe_records:

            data.append({
                'id': record.id,
                'name': record.name,
            })

        return data
