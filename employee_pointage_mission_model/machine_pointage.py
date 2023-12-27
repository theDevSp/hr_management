from odoo import models, fields


class MachinePointage(models.Model):
    _name = 'machine.pointage'
    _description = 'Mission Pointage'
    _inherit = 'hr.rapport.pointage'
