from odoo import models, fields
from datetime import datetime

class blacklist(models.Model):
    _name = 'hr.blacklist'
    _description = "Black List"

    employee_id = fields.Many2one("hr.employee", "Employee", readonly=True)
    responsable_id = fields.Many2one("hr.responsable.chantier", "Responsable :")
    directeur_id = fields.Many2one("hr.directeur", "Directeur :")
    chantier_id = fields.Many2one("fleet.vehicle.chantier", "Chantier :")
    motif = fields.Text("Motif :")
    date_effet = fields.Date("Date d'Effet :", default = datetime.today())
    action = fields.Selection([('bloque', 'Bloquer'),('debloque','Débloquer')], "Action :")
    user_doing_action = fields.Many2one("res.users","User doing action")
