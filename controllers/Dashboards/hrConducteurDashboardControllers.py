from odoo import http
from odoo.http import request

from itertools import groupby
from datetime import datetime
from dateutil.relativedelta import relativedelta


class hrConducteurDashboardControllers(http.Controller):

    def get_previous_period(self, date):
        res = http.request.env["account.month.period"].search(
            [('date_stop', '>=', date), ('date_start', '<=', date)], limit=1)
        return res[0] if len(res) > 0 else []

    @http.route('/hr_management/conducteur-dashboard/', type='json', auth='user')
    def get_chantiers_data_details(self, chantier_id, period_id):

        period_id = int(period_id)
        chantier_id = int(chantier_id)

        chantier = http.request.env['fleet.vehicle.chantier'].sudo().browse(
            chantier_id)

        current_period_record = http.request.env['account.month.period'].sudo().browse(
            period_id)

        previous_period = self.get_previous_period(
            current_period_record.date_start - relativedelta(months=1))
        current_period = current_period_record

        line_reports = http.request.env['hr.rapport.pointage.line'].sudo().search(
            [('rapport_id.period_id.date_start', '>=', previous_period.date_start),
             ('rapport_id.period_id.date_stop', '<=', current_period.date_stop),
             ('chantier_id', '=', chantier_id)])

        line_reports = sorted(line_reports, key=lambda r: (
            r.day.month, r.employee_id.type_emp))

        line_reports_grouped_by_month = groupby(
            line_reports, lambda x: x.day.month)

        for month_key, month_group in line_reports_grouped_by_month:
            month_group_sorted = sorted(
                month_group, key=lambda r: r.employee_id.type_emp)
            line_reports_grouped_by_type = groupby(
                month_group_sorted, lambda x: x.employee_id.type_emp)

            for type_key, type_group in line_reports_grouped_by_type:
                for line in type_group:
                    print(line.id)
        return

        total_hours_salarier_current_period = 0
        total_hours_ouvrier_current_period = 0

        total_hours_salarier_last_period = 0
        total_hours_ouvrier_last_period = 0

        salarier_count_current_period = 0
        ouvrier_count_current_period = 0

        salarier_count_last_period = 0
        ouvrier_count_last_period = 0

        salarier_amounts_last_period = 0
        ouvrier_amounts_last_period = 0

        salarier_amounts_current_period = 0
        ouvrier_amounts_current_period = 0

        for line in current_period_line_reports:
            h_travailler = float(line.h_travailler)

            if line.rapport_id.quinzaine == "quinzaine12":
                total_hours_salarier_current_period += h_travailler
                salarier_count_current_period += 1
                salarier_amounts_current_period += (
                    line.employee_id.salaire_heure_related * h_travailler)
            elif line.rapport_id.quinzaine in ('quinzaine1', 'quinzaine2'):
                total_hours_ouvrier_current_period += h_travailler
                ouvrier_count_current_period += 1
                ouvrier_amounts_current_period += (
                    line.employee_id.salaire_heure_related * h_travailler)

        for line in last_period_line_reports:
            h_travailler = float(line.h_travailler)

            if line.rapport_id.quinzaine == "quinzaine12":
                total_hours_salarier_last_period += h_travailler
                salarier_count_last_period += 1
                salarier_amounts_last_period += (
                    line.employee_id.salaire_heure_related * h_travailler)
            elif line.rapport_id.quinzaine in ('quinzaine1', 'quinzaine2'):
                total_hours_ouvrier_last_period += h_travailler
                ouvrier_count_last_period += 1
                ouvrier_amounts_last_period += (
                    line.employee_id.salaire_heure_related * h_travailler)

        current_period_line_reports = sorted(
            current_period_line_reports, key=lambda r: (r.employee_id.job_id.name))
        last_period_line_reports = sorted(
            last_period_line_reports, key=lambda r: (r.employee_id.job_id.name))

        current_period_grouped_data = {key: len(set(record.employee_id.id for record in group)) for key, group in groupby(
            current_period_line_reports, key=lambda r: r.employee_id.job_id.name)}
        last_period_grouped_data = {key: len(set(record.employee_id.id for record in group)) for key, group in groupby(
            last_period_line_reports, key=lambda r: r.employee_id.job_id.name)}

        return {
            "chantier": chantier.code + " - " + chantier.simplified_name,
            "current_period": current_period.code,
            "last_period": previous_period.code,
            "total_hours_salarier_current_period": total_hours_salarier_current_period,
            "total_hours_ouvrier_current_period": total_hours_ouvrier_current_period,
            "total_hours_salarier_last_period": total_hours_salarier_last_period,
            "total_hours_ouvrier_last_period": total_hours_ouvrier_last_period,
            "salarier_count_current_period": salarier_count_current_period,
            "ouvrier_count_current_period": ouvrier_count_current_period,
            "salarier_count_last_period": salarier_count_last_period,
            "ouvrier_count_last_period": ouvrier_count_last_period,
            "salarier_amounts_last_period": salarier_amounts_last_period,
            "ouvrier_amounts_last_period": ouvrier_amounts_last_period,
            "salarier_amounts_current_period": salarier_amounts_current_period,
            "ouvrier_amounts_current_period": ouvrier_amounts_current_period,
            "count_effectif_postes_period": current_period_grouped_data,
            "count_effectif_postes_last_period": last_period_grouped_data,
        }

        """current_period_reports = http.request.env['hr.rapport.pointage'].sudo().search(
            [('period_id', '=', current_period.id), ('chantier_id', '=', chantier_id)])
        last_period_reports = http.request.env['hr.rapport.pointage'].sudo().search(
            [('period_id', '=', previous_period.id), ('chantier_id', '=', chantier_id)])

        print(len(current_period_reports), len(last_period_reports))

        period_total_h_ouvrier = 0
        period_total_h_salarier = 0
        period_total_sal_ouvrier = 0
        period_total_sal_salarier = 0
        period_total_salarier = 0
        period_total_ouvrier = 0

        last_period_total_h_ouvrier = 0
        last_period_total_h_salarier = 0
        last_period_total_sal_ouvrier = 0
        last_period_total_sal_salarier = 0
        last_period_total_salarier = 0
        last_period_total_ouvrier = 0

        for rapport in current_period_reports:
            if rapport.quinzaine in ('quinzaine1', 'quinzaine2'):
                period_total_h_ouvrier += rapport.total_h
                period_total_sal_ouvrier += rapport.employee_id.wage
                period_total_ouvrier += 1
            elif rapport.quinzaine == 'quinzaine12':
                period_total_h_salarier += rapport.total_h
                period_total_sal_salarier += rapport.employee_id.wage
                period_total_salarier += 1

        for rapport in last_period_reports:
            if rapport.quinzaine in ('quinzaine1', 'quinzaine2'):
                last_period_total_h_ouvrier += rapport.total_h
                last_period_total_sal_ouvrier += rapport.employee_id.wage
                last_period_total_ouvrier += 1
            elif rapport.quinzaine == 'quinzaine12':
                last_period_total_h_salarier += rapport.total_h
                last_period_total_sal_salarier += rapport.employee_id.wage
                last_period_total_salarier += 1

        user = http.request.env.user

        return {
            'previous_period': previous_period.code,
            'current_period': current_period.code,
            'period_total_h_ouvrier': period_total_h_ouvrier,
            'period_total_h_salarier': period_total_h_salarier,
            'period_total_sal_ouvrier': period_total_sal_ouvrier,
            'period_total_sal_salarier': period_total_sal_salarier,
            'period_total_salarier': period_total_salarier,
            'period_total_ouvrier': period_total_ouvrier,
            'last_period_total_h_ouvrier': last_period_total_h_ouvrier,
            'last_period_total_h_salarier': last_period_total_h_salarier,
            'last_period_total_sal_ouvrier': last_period_total_sal_ouvrier,
            'last_period_total_sal_salarier': last_period_total_sal_salarier,
            'last_period_total_ouvrier': last_period_total_ouvrier,
            'last_period_total_salarier': last_period_total_salarier,
            'user': user.name.upper()
        }
"""
