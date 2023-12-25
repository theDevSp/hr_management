# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import itertools
from operator import itemgetter
import json


class HrAnalytique(http.Controller):
    @http.route('/hr_management/analytique_q12/', type='json', auth='user')
    def get_analytique_list_q12(self):
        pointage_records = request.env['hr.rapport.pointage'].search(
            [('period_id', '=', 141), ('state', '=', 'valide'), ('quinzaine', '=', 'quinzaine12')])

        sorted_records = sorted(
            pointage_records, key=lambda x: x.employee_id.name)
        grouped_records = {key: list(group) for key, group in itertools.groupby(
            sorted_records, key=lambda x: x.employee_id.name)}

        data = []

        for key, group in grouped_records.items():
            employee_data = {"employee": key, "records": []}

            for record in group:
                record_data = {"quinzaine": record.quinzaine}

                chantier_totals = []
                for ligne in record.rapport_lines:
                    chantier = ligne.chantier_id.simplified_name
                    equipe = ligne.emplacement_chantier_id.name
                    engin = ligne.vehicle_id.name
                    h_travailler = float(ligne.h_travailler)

                    if chantier and equipe:

                        # Check if chantier already exists in chantier_totals
                        existing_chantier = next(
                            (item for item in chantier_totals if item["chantier"] == chantier and item["equipe"] == equipe), None)

                        if existing_chantier:
                            existing_chantier["total_hours"] += h_travailler
                        else:
                            chantier_totals.append(
                                {"chantier": chantier, "equipe": equipe, "engin": engin, "total_hours": h_travailler})

                record_data["chantier_totals"] = chantier_totals

                employee_data["records"].append(record_data)

            data.append(employee_data)

        return data

    @http.route('/hr_management/analytique_q1_q2/', type='json', auth='user')
    def get_analytique_list_q1_q2(self):
        pointage_records = request.env['hr.rapport.pointage'].search(
            [
                ('period_id', '=', 142),
                ('quinzaine', 'in', ('quinzaine1', 'quinzaine2'))
            ]
        )

        sorted_records = sorted(
            pointage_records, key=lambda x: x.employee_id.name)
        grouped_records = {key: list(group) for key, group in itertools.groupby(
            sorted_records, key=lambda x: x.employee_id.name)}

        data = []

        for key, group in grouped_records.items():
            employee_data = {"employee": key, "records": []}

            for record in group:
                record_data = {"quinzaine": record.quinzaine}

                chantier_totals = []
                for ligne in record.rapport_lines:
                    chantier = ligne.chantier_id.simplified_name
                    equipe = ligne.emplacement_chantier_id.name
                    engin = ligne.vehicle_id.name
                    h_travailler = float(ligne.h_travailler)

                    if chantier and equipe:

                        # Check if chantier already exists in chantier_totals
                        existing_chantier = next(
                            (item for item in chantier_totals if item["chantier"] == chantier and item["equipe"] == equipe), None)

                        if existing_chantier:
                            existing_chantier["total_hours"] += h_travailler
                        else:
                            chantier_totals.append(
                                {"chantier": chantier, "equipe": equipe, "engin": engin, "total_hours": h_travailler})

                record_data["chantier_totals"] = chantier_totals

                employee_data["records"].append(record_data)

            data.append(employee_data)

        return data
