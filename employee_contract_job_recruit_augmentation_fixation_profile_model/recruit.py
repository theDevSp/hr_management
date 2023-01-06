from odoo import fields, models, api

class recruit(models.Model):
    _name = "hr.recrutement"
    _description = "Recrutement"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    READONLY_STATES = {
        'draft': [('readonly', False)],
        'validee': [('readonly', True)],
        'encours': [('readonly', True)],
        'acceptee': [('readonly', True)],
        'refusee': [('readonly', True)],
        'annulee': [('readonly', True)],
        'terminee': [('readonly', True)]
    }

    READONLY_STATES_NBR_EFF_ACCEPTE = {
        'draft': [('readonly', True)],  
        'validee': [('readonly', False)],
        'encours': [('readonly', False)],
        'acceptee': [('readonly', False)],
        'refusee': [('readonly', False)],
        'annulee': [('readonly', False)],
        'terminee': [('readonly', False)]
    }

    chantier_id  = fields.Many2one("fleet.vehicle.chantier",u"Chantier", states = READONLY_STATES,track_visibility='onchange')
    responsable_id = fields.Many2one("hr.responsable.chantier","Responsable", states = READONLY_STATES)
    title_poste = fields.Many2one("hr.job","Titre du poste", states = READONLY_STATES)
    observation = fields.Char("Observation", states = READONLY_STATES)
    nbr_effectif_demande = fields.Integer("Nombre d'effectif demandé", states = READONLY_STATES)
   
    nbr_effectif_accepte = fields.Integer("Nombre d'effectif accepté", states = READONLY_STATES_NBR_EFF_ACCEPTE)
    compute_readonly_eff_accepte = fields.Boolean(string="check field", compute='get_user')

    state  = fields.Selection([
        ("draft","Brouillon"),
        ("validee","Validée"),
        ("encours","En cours de traitement"),
        ("acceptee","Acceptée"),
        ("refusee","Refusée"),
        ("annulee","Annulée"),
        ("terminee","Terminée")
        ],"Status", 
        default="draft",
        readonly = True  
    )

    @api.onchange("nbr_effectif_demande")
    def onchange_nbr_effectif_demande(self):
        self.nbr_effectif_accepte = self.nbr_effectif_demande


    @api.depends('compute_readonly_eff_accepte')
    def get_user(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('hr_management.group_pointeur'):
            self.compute_readonly_eff_accepte = True
        else:
            self.compute_readonly_eff_accepte = False

    def B0(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
