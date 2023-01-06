from odoo import fields, models

class responsable_chantier(models.Model):
    _name = "hr.responsable.chantier"
    _description = "Responsable_Chantier"
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char("Nom")
    poste = fields.Many2one("hr.job", "Poste occupé")
    type_responsabilite = fields.Selection([("1","Chef Chantier"),("2","Chef Matériel"),("3","Pointeur")],u"Type Responsabilité")
    
    chantiers_ids= fields.Many2many(
        'fleet.vehicle.chantier',
        string = 'Chantiers :'
    )