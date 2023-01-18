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

    name = fields.Char('Référence', readonly=True, required=True, copy=False, default='New')
    chantier_id  = fields.Many2one("fleet.vehicle.chantier",u"Chantier", states = READONLY_STATES, required=True)
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
    )

    _sql_constraints = [
		('name_uniq', 'UNIQUE(name)', 'Cette référence est déjà utilisée.'),
	]

    @api.onchange("nbr_effectif_demande")
    def onchange_nbr_effectif_demande(self):
        self.nbr_effectif_accepte = self.nbr_effectif_demande


    @api.depends('compute_readonly_eff_accepte')
    def get_user(self):
        self.compute_readonly_eff_accepte = self.user_has_groups('hr_management.group_pointeur')


    @api.model
    def create(self, vals):
        code_recrut = self.env['ir.sequence'].next_by_code('hr.recrutement.sequence') or ('New')
        code_chantier = self.env['fleet.vehicle.chantier'].browse(vals.get('chantier_id')).code
        vals['name'] = code_chantier + '/' + code_recrut
        return super(recruit, self).create(vals)

    def write(self, vals):
        return super(recruit, self).write(vals)


    def to_draft(self):
        self.state = 'draft'

    def to_validee(self):
        self.state = 'validee'

    def to_encours(self):
        self.state = 'encours'

    def to_acceptee(self):
        self.state = 'acceptee'
    
    def to_refusee(self):
        self.state = 'refusee'
    
    def to_annulee(self):
        if self.user_has_groups('hr_management.group_admin_paie'):
            self.state = 'annulee'
        elif self.user_has_groups('hr_management.group_agent_paie') and self.state in {'validee', 'encours', 'acceptee'} :
            self.state = 'annulee'
        elif self.user_has_groups('hr_management.group_pointeur') and self.state in {'draft', 'validee'} :
            self.state = 'annulee'

    def to_terminee(self):  
        self.state = 'terminee'
