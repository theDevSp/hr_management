# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class contrats(models.Model):
    _description = "Contrats"
    _inherit = ['hr.contract']

    name = fields.Char('Contract Name', required=True, readonly=True, copy=False, default='New')
    chantier_id = fields.Many2one('fleet.vehicle.chantier', string = "Chantier")

    _sql_constraints = [
		('name_contract_uniq', 'UNIQUE(name)', 'Cette référence est déjà utilisée.'),
	]

    def to_new(self):
        self.state = 'draft'

    def to_running(self):
        for rec in self :
            contract_ids = self.employee_id.contract_ids
            for rec in contract_ids:
                rec.state = 'cancel'

        self.state = 'open'


    def to_expired(self):
        self.state = 'close'

    def to_cancelled(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie'):
            self.state = 'cancel'

    @api.model
    def create(self, vals):
        query = """
            SELECT COUNT(*)
            FROM hr_contract
            WHERE employee_id=%s  and (state='draft' or state='open')
            ;
        """ % (vals['employee_id'])
        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()[0]

        if(res['count']==0):
            type_emp = self.env['hr.employee'].browse(vals["employee_id"]).type_emp
            today = datetime.now()
            year = today.year
            month = '{:02d}'.format(today.month)
            contract_sequence = self.env['ir.sequence'].next_by_code('hr.contract.sequence')
            vals['name'] = type_emp + '-' + str(month) + '/' + str(year) + '/' + str(contract_sequence)
        else:
            raise ValidationError(
                    "Erreur, Cet employé a déjà un contrat 'New' ou 'Running'."
                )

        return super(contrats, self).create(vals)


    def write(self, vals):
        return super(contrats, self).write(vals)