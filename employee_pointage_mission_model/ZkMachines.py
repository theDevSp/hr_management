from odoo import models, fields, api

from zk import ZK, const
import pytz
from datetime import datetime, date, timedelta


class ZkMachines(models.Model):
    _name = 'zk.machines'
    _description = 'Zk Machines'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Machine Name', required=True)
    ip_address = fields.Char(string='IP Address', required=True)
    port = fields.Integer(string='Port', required=True)

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.name = self.name.upper()

    def test_connection(self):
        zk = ZK(self.ip_address, self.port, 5, 0, False, False)
        try:
            conn = zk.connect()
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Test de la Connexion',
                    'type': 'success',
                    'message': 'Connexion réussie avec la Machine',
                    'sticky': False
                }
            }
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Test de la Connexion',
                    'type': 'danger',
                    'message': f'Échec de la connexion avec la Machine. Erreur: {e}',
                    'sticky': False
                }
            }

    def connect_to_device(self, ip_address, port, timeout, password, force_udp, omit_ping):
        zk = ZK(ip_address, port, timeout, str(password),
                force_udp, omit_ping)
        conn = zk.connect()
        if not conn:
            raise RuntimeError("Failed to connect to the device")
        return conn

    def get_user(self, conn, user_id):
        conn.disable_device()
        users = conn.get_users()

        found_user = next((user for user in users if int(
            user.user_id) == int(user_id)), None)

        conn.enable_device()
        return found_user

    def get_pointage(self, conn, ids=None, date_start=None, date_fin=None):
        conn.disable_device()

        if ids is None or not ids:
            users = conn.get_users()
            ids = [user.user_id for user in users]

        users_founded = [self.get_user(conn, user_id) for user_id in ids]

        try:
            attendance = conn.get_attendance()
        except:
            attendance = False
            print(f"Error fetching attendance")

        if attendance and users_founded:
            user_attendance_dict = {}

            for each in attendance:
                atten_time = each.timestamp
                atten_time = datetime.strptime(atten_time.strftime(
                    '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                local_tz = pytz.timezone('GMT')
                local_dt = local_tz.localize(atten_time, is_dst=None)
                utc_dt = local_dt.astimezone(pytz.utc)
                utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                atten_time = datetime.strptime(utc_dt, "%Y-%m-%d %H:%M:%S")

                if date_start.date() <= atten_time.date() <= date_fin.date():
                    for user in users_founded:
                        if user.user_id == each.user_id:
                            user_id = int(user.user_id)
                            user_name = str(user.name).upper()

                            if user_id not in user_attendance_dict:
                                user_attendance_dict[user_id] = {
                                    "name": user_name, "attendance_times": []}
                            user_attendance_dict[user_id]["attendance_times"].append(
                                atten_time.date())

            """for user_id, data in sorted(user_attendance_dict.items()):
                print(f"-------------------------------------------")
                print(f"User ID: {user_id}")
                print(f"User Name: {data['name']}")
                for atten_time in data["attendance_times"]:
                    print(f"Attendance Time: {atten_time}")
                print(f"-------------------------------------------")"""

        conn.enable_device()
        return user_attendance_dict


class HrEmployeeMachines(models.Model):
    _inherit = 'hr.employee'

    machine_id = fields.Many2one(
        'zk.machines', string='Machine associée', help='La machine associée à cet employé(e)')
    user_machine_id = fields.Integer(string="ID de l'Utilisateur")
