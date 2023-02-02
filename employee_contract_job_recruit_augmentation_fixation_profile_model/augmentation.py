from odoo import fields, models, api

class augmentation(models.Model):
    _name = "hr.augmentation"
    _description = "Augmentation"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    employee_id = fields.Many2one('hr.employee', string = "Employee", required=True)
    chantier_id = fields.Many2one('fleet.vehicle.chantier', string = "Chantier")
    responsable_id = fields.Many2one("hr.responsable.chantier", string = "Responsable")
    directeur_id = fields.Many2one("hr.directeur", string = "Directeur")
    period_id = fields.Many2one("account.month.period", string = "Période")
    date_fait = fields.Date("Date de fait", required=True, default=fields.Date.today, tracking=True,
        help="Date d'augmentation de salaire pour l'employé.", index=True)

    currency_id = fields.Many2one('res.currency', string = 'Symbole Monétaire')
    montant_propose = fields.Monetary('Montant Proposé', currency_field = 'currency_id')
    montant_valide = fields.Monetary('Montant Validé', currency_field = 'currency_id')

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('validee', 'Validée'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
        ('annulee', 'Annulée')
        ], 
        string='Status',
        default='draft'
    )

    motif =  fields.Selection([
        ('renouvlement', 'Renouvelement du contrat'),
        ('chang_fonction', 'Changement de la fonction'),
        ('anciennete', 'Ancienneté'),
        ('rendement', 'Rendement'),
        ('competence', 'Compétence'),
        ('chang_qualif', 'Changement de qualification'),
        ('autres', 'Autres')
        ], 
        string='Motif'
    )

    observation = fields.Html('Observation')
