from odoo import models, fields

class Bank(models.Model):
    _name = 'bank'
    _description = 'Bank'

    name = fields.Char(string='Bank Name')


class City(models.Model):
    _name = 'city'
    _description = 'City'

    name = fields.Char(string='City Name')