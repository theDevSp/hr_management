from odoo import fields, models

class directeur(models.Model):
    _name = "hr.directeur"
    _description = "Directeur"
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Nom")
    poste = fields.Many2one("hr.job", "Poste occupé")