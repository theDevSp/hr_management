from odoo import models, fields,api
from datetime import datetime

class wizard_reporter_dates(models.TransientModel):
    _name = "wizard_reporter_dates"
    _description = "Wizard Reporter Dates"

    notes = fields.Text("Notes")

    def action_confirm_reporter_dates(self):
        observations = self.notes 
        current_ligne_id = self._context["line_id"]
        current_model = self._context["current_model"]
        if current_model == "prime":
            current_ligne_objet = self.env['hr.paiement.ligne'].browse(current_ligne_id)
            current_ligne_objet.recompute_prime(observations)
        elif current_model == "prelevement":
            current_ligne_objet = self.env['hr.paiement.prelevement'].browse(current_ligne_id)
            current_ligne_objet.recompute_prelevement(observations)