from odoo import models, fields,api
from datetime import datetime

class wizard_blacklist(models.TransientModel):
    _name = 'wizard_blacklist'
    _description = "Wizard Black List"

    employee_id = fields.Many2one("hr.employee", "Employee", readonly=True)
    responsable_id = fields.Many2one("hr.responsable.chantier", "Responsable")
    directeur_id = fields.Many2one("hr.directeur", "Directeur")
    chantier_id = fields.Many2one("fleet.vehicle.chantier", "Chantier")
    motif = fields.Text("Motif")
    date_effet = fields.Date("Date d'Effet", default = datetime.today())
    action = fields.Selection([('bloque', 'Bloquer'),('debloque','Débloquer')], "Action :")


    def action_confirm_blacklist(self):
        user = self.env.user.id
        vals = {
            'employee_id': self.employee_id.id,
            'responsable_id': self.responsable_id.id,
            'directeur_id': self.directeur_id.id,
            'chantier_id': self.chantier_id.id,
            'motif': self.motif,
            'date_effet': self.date_effet,
            'action': self.action,
            'user_doing_action': user
        }

        res = self.env['hr.blacklist'].create(vals)

        if res :
            self.employee_id.write({"black_list": False if self.action == "debloque" else True })
