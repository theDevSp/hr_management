from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import date
import calendar


class ComplementAugmentation(models.Model):
    _name = "complement.augmentation"

    comp_aug_id = fields.Many2one("hr.payslip",u'AUG',ondelete='cascade')
    augmentation_id = fields.Many2one("hr.augmentation", string='Augmentation')
    period_id = fields.Many2one(related="augmentation_id.period_id", string = "Période")
    augmentation_date_fait = fields.Date(related="augmentation_id.date_fait", string="Date de fait")
    augmentation_montant_valide = fields.Float(related="augmentation_id.montant_valide", string="Montant Validé")
    augmentation_type = fields.Selection(related="augmentation_id.type", string="Type")
    augmentation_observation = fields.Text(related="augmentation_id.observation", string="Observation")

    state = fields.Selection([('validee', 'Validée'), ('annulee', 'Annulée')], string='State', default='validee')

    def action_validation(self):
        if self.state:
            self.state = 'validee'

    def action_annuler(self):
        if self.state:
            self.state = 'annulee'