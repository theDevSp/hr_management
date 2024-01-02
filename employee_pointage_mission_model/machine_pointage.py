import json
from odoo import models, fields
import datetime as dt
from datetime import datetime


class MachinePointage(models.Model):
    _inherit = 'hr.rapport.pointage'

    def get_difference(self, startdatetime, enddatetime):
        diff = enddatetime - startdatetime
        return diff.total_seconds()

    def get_employee_pointage(self):
        machine_id = self.employee_id.machine_id
        conn = machine_id.connect_to_device(
            machine_id.ip_address, machine_id.port)

        user_machine_id = self.employee_id.user_machine_id
        period_start = self.period_id.date_start
        period_stop = self.period_id.date_stop

        pointage = machine_id.get_pointage(
            conn, [user_machine_id], period_start, period_stop)

        person_id = list(pointage.keys())[0]
        person_data = pointage[person_id]

        attendance_by_date = {}

        for attendance_datetime in person_data['attendance_times']:
            date_key = attendance_datetime.date()
            attendance_by_date.setdefault(
                date_key, []).append(attendance_datetime)

        result = []

        for date, date_list in attendance_by_date.items():
            formatted_date = date.strftime("%Y-%m-%d")

            if len(date_list) == 4:
                result.append({
                    "date": formatted_date,
                    "p1": date_list[0].strftime("%Y-%m-%d %H:%M:%S"),
                    "p2": date_list[1].strftime("%Y-%m-%d %H:%M:%S"),
                    "p3": date_list[2].strftime("%Y-%m-%d %H:%M:%S"),
                    "p4": date_list[3].strftime("%Y-%m-%d %H:%M:%S"),
                    "total_hours": f"{self.get_difference(date_list[0], date_list[1])/3600 + self.get_difference(date_list[2], date_list[3])/3600}",
                    "total_seconds": f"{self.get_difference(date_list[0], date_list[1]) + self.get_difference(date_list[2], date_list[3])}"
                })
            elif len(date_list) in [2, 3]:
                result.append({
                    "date": formatted_date,
                    "p1": date_list[0].strftime("%Y-%m-%d %H:%M:%S"),
                    "p2": date_list[1].strftime("%Y-%m-%d %H:%M:%S"),
                    "total_hours": f"{self.get_difference(date_list[0], date_list[1])/3600}",
                    "total_seconds": f"{self.get_difference(date_list[0], date_list[1])}",
                })
            elif len(date_list) == 1:
                result.append({
                    "date": formatted_date,
                    "p1": date_list[0].strftime("%Y-%m-%d %H:%M:%S"),
                    "total_hours": f"0.0"
                })

        today = dt.date.today().strftime("%Y-%m-%d")

        for entry in result:
            if entry['date'] != today:
                for line in self.rapport_lines:
                    line.note = ''
                    if str(line.day) == entry['date']:
                        line.h_travailler = f"{round(float(entry['total_hours']) * 2) / 2}"
                        time_strings = [datetime.strptime(entry[key], '%Y-%m-%d %H:%M:%S').strftime(
                            '%H:%M:%S') for key in entry if key.startswith('p')]
                        line.details = ', '.join(time_strings)
