<<<<<<< Updated upstream
=======
from odoo import fields, models, api

class recruit(models.Model):
    _name = "hr.recrutement"
    _description = "Recrutement"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    chantier_id  = fields.Many2one("fleet.vehicle.chantier",u"Chantier:")
    responsable_id = fields.Many2one("hr.responsable.chantier","Responsable:")
    title_poste = fields.Many2one("hr.job","Titre du poste:")
    nbr_effectif_demande = fields.Integer("Nombre d'effectif demandé:")
    nbr_effectif_accepte = fields.Integer("Nombre d'effectif accepté:")
    status  = fields.Selection([("brouillon","Brouillon"),("validee","Validée"),("encours","En cours de traitement"),("acceptee","Acceptée"),("refusee","Refusée"),("annulee","Annulée"),("terminee","Terminée")],u"Status:")
    observation = fields.Char("Observation:")

    
>>>>>>> Stashed changes
