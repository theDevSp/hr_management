from math import ceil
from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError,UserError



class holiday_validation_wizard(models.TransientModel):       

    _name = "holiday.validation.wizard"

    holiday_id = fields.Many2one("hr.holidays",string="Congé")
    nbr_jour_compenser = fields.Float('Jours Validé',required=True)

    def update_holiday_day_valid(self):
        if self.nbr_jour_compenser > self.holiday_id.duree_jours:
            raise ValidationError("Vous essayez de valider nombre jours plus que mentionné dans le congé.")
        self.holiday_id.write({
            'nbr_jour_compenser': self.nbr_jour_compenser
        })
