from odoo import fields, models, api
from odoo.exceptions import ValidationError

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

    motif_autres = fields.Char("Motif Autres")

    observation = fields.Html('Observation')

    @api.model
    def create(self, vals):
        return super(augmentation, self).create(vals)

    def write(self, vals):
        return super(augmentation, self).write(vals)


    def to_draft(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft','acceptee','refusee'} :
                self.state = 'draft'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le status."
                )

    def to_validee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'validee','acceptee','refusee','annulee'} :
                self.state = 'validee'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le status."
                )

    def to_acceptee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft','acceptee','annulee'} :
                self.state = 'acceptee'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le status."
                )

    def to_refusee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft', 'refusee', 'annulee'} :
                self.state = 'refusee'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le status."
                )
    
    def to_annulee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'annulee'} :
                self.state = 'annulee'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le status."
                )