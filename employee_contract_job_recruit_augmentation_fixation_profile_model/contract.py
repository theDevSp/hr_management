# -*- coding: utf-8 -*-

from odoo import models, fields, api

class contrats(models.Model):
    _description = "Contrats"
    _inherit = ['hr.contract']

    name = fields.Char('Contract Name', required=True, readonly=True, copy=False, default='New')
    chantier_id = fields.Many2one('fleet.vehicle.chantier', string = "Chantier")
    
    #contract_ids = fields.One2many('hr.contract', 'employee_id' ,string = "Contrats")

    _sql_constraints = [
		('name_contract_uniq', 'UNIQUE(name)', 'Cette référence est déjà utilisée.'),
	]

    def to_new(self):
        self.state = 'draft'

    def to_running(self):
        self.state = 'open'

    def to_expired(self):
        self.state = 'close'

    def to_cancelled(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        contract_ids = self.env['hr.employee'].browse(vals["employee_id"]).contract_ids
       
        print(contract_ids)
        print("contract_ids")
        vals['name'] = self.env['ir.sequence'].next_by_code('hr.contract.sequence')
        vals['state'] = 'cancel'
        return super(contrats, self).create(vals)


    def write(self, vals):
        return super(contrats, self).write(vals)