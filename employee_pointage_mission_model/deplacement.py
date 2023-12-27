from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class Deplacement(models.Model):
    _name = 'hr.deplacement'
    _description = 'Déplacement'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(u"Référence", readonly=True, default="")
    employee_id = fields.Many2one("hr.employee", u"Employée", required=True)
    date_debut = fields.Date('Date Début', required=True)
    date_fin = fields.Date('Date Fin', required=True)
    motif = fields.Text('Motif', required=True)

    type = fields.Selection([
        ('dpl', 'Déplacement'),
        ('auth', 'Autorisation')
    ],
        string='type'
    )

    state = fields.Selection([
        ('draft', 'Brouillion'),
        ('approuved', 'Approuvée'),
        ('valide', 'Validée'),
    ], string='Status', default='draft')

    @api.model
    def create(self, vals):

        if vals.get('date_fin') and vals.get('date_debut') and vals['date_fin'] < vals['date_debut']:
            raise ValidationError(
                "Erreur : la date de fin doit être supérieure à la date de début.")

        res = super(Deplacement, self).create(vals)

        query = """
            SELECT COUNT(*) FROM hr_deplacement WHERE EXTRACT(YEAR FROM create_date) = %s AND type = %s
        """
        self.env.cr.execute(query, (datetime.today().year, res.type,))
        result = self.env.cr.fetchall()

        print("result[0][0] ", result[0][0])

        code = res.type[0].upper() if res.type else ''
        sequence_number = result[0][0]
        res.name = f"{code}{sequence_number:05d}-{datetime.today().month}/{datetime.today().year}"

        return res

    def to_draft(self):
        self.state = 'draft'

    def to_validee(self):
        self.state = 'valide'

    def to_approuver(self):
        self.state = 'approuved'
