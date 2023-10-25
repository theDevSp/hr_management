# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import date


class employee_rib(models.Model):
    _name = 'employee.rib'
    _description = 'Employee Rib'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(u'N° RIB', size=24)
    bank = fields.Many2one("bank","Banque")
    ville_bank = fields.Many2one("city",u"Ville")
    bank_agence = fields.Char(u"Agence")
    payement_mode_id = fields.Many2one('payement.mode', string='Mode de paiement',required=True)


    employee_id = fields.Many2one("hr.employee",u"Employée", ondelete='cascade')

    _sql_constraints = [
		('code_uniq', 'UNIQUE(name)', 'Ce N° RIB déjà existe.'),
	]


    @api.constrains('name')
    def _check_RIB(self):
        if self.name:
            if self.name.isdigit() == False:
                raise ValidationError("Erreur, Format incorrect.")
            else:
                if len(self.name) < 24 or  len(self.name)>24:
                    raise ValidationError("Erreur, Le numéro de RIB doit avoir 24 caractères.")
    
    def to_enable(self):
        self.employee_id.write({'rib_number':self.id})
        title = _("Succès")
        message = _("Le RIB a été activé avec succès pour cet employé")
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': message,
                'sticky': False,
            }
        }
                    
    


    