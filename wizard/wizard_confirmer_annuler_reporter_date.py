from odoo import models, fields,api
from datetime import datetime

class wizard_confirmer_annuler_reporter_date(models.TransientModel):
    _name = "wizard_confirmer_annuler_reporter_date"
    _description = "Wizard Confirmer Annuler Reporter Date"

    message = fields.Text("Message", readonly = True)

    def action_confirm_annuler_reporter_date(self):
        current_line_id = self._context["current_line"]
        current_line_objet = self.env['hr.paiement.ligne'].browse(current_line_id)
        last_line_non_paye_id = self._context["last_line_non_paye"]
        last_line_non_paye_objet = self.env['hr.paiement.ligne'].browse(last_line_non_paye_id)
        current_line_objet.annuler_reporter_date_apres_confirmation(last_line_non_paye_objet)