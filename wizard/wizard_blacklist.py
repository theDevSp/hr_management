from odoo import models, fields
from datetime import datetime

class wizard_blacklist(models.TransientModel):
    _name = 'wizard_blacklist'
    _description = "Wizard Black List"

    employee_id = fields.Many2one("hr.employee", "Employee")
    responsable_id = fields.Many2one("hr.responsable.chantier", "Responsable :")
    directeur_id = fields.Many2one("hr.directeur", "Directeur :")
    chantier_id = fields.Many2one("fleet.vehicle.chantier", "Chantier :")
    motif = fields.Text("Motif :")
    date_effet = fields.Date("Date d'Effet :", default = datetime.today())
    action = fields.Selection([('bloque', 'Bloquer'),('debloque','Débloquer')], "Action :")


    def action_confirm(self):
        # Perform some action here
        return {'type': 'ir.actions.act_window_close'}

