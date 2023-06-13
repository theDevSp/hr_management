from odoo import models, fields, api

class typecontrat(models.Model):
    _description = "Type Contrat"
    _inherit = ['hr.contract.type']

    name = fields.Char('Libellé')
    depends_duration = fields.Boolean("Dépend de la durée")
    depends_emplacement = fields.Boolean("Dépend de l'emplacement")
    duree = fields.Float("Durée")
    
    @api.onchange("depends_duration")
    def onchange_depends_duration(self):
        if self.depends_duration:
            self.depends_emplacement = False

    @api.onchange("depends_emplacement")
    def onchange_depends_emplacement(self):
        if self.depends_emplacement:
            self.depends_duration = False
