from odoo import models, fields, api

# Assuming 'zk' module is available in your environment
from zk import ZK


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
                    'title': 'Test la Connexion',
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
                    'title': 'Test la Connexion',
                    'type': 'danger',
                    'message': f'Échec de la connexion avec la Machine. Erreur: {e}',
                    'sticky': False
                }
            }


class HrEmployeeMachines(models.Model):
    _inherit = 'hr.employee'

    machine_id = fields.Many2one(
        'zk.machines', string='Machine associée', help='La machine associée à cet employé(e)')
    user_machine_id = fields.Integer(string="ID de l'Utilisateur")
