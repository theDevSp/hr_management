
from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime,date
from num2words import num2words

class fixation_salaire(models.Model):
    
    _name="hr.fixation.salaire"
    _description = "Fixation Salaire"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char("Ref",readonly=True)
    employee_id = fields.Many2one("hr.employee",string="Employé",required=True)
    cin = fields.Char(related='employee_id.cin',string="N° CIN",readonly=True)
    cnss = fields.Char(related='employee_id.cnss',string="N° CNSS",readonly=True)
    fonction = fields.Many2one(related='employee_id.job_id',string="Fonction",readonly=True,store=True)
    profile  = fields.Many2one(related="employee_id.contract_id.pp_personnel_id_many2one",string='Profile de paie',readonly=True,store=True)
    date_embauche = fields.Date(related="employee_id.contract_id.date_start",string='Date Début',readonly=True)
    chantier_id = fields.Many2one('fleet.vehicle.chantier',string="Chantier d'affectation")
    embaucher_par  = fields.Many2one(related='employee_id.embaucher_par',string="Embauché Par",readonly=True)
    recommander_par  = fields.Many2one(related='employee_id.recommander_par',string="Recommandé Par",readonly=True)
    offered_wage = fields.Float("Salaire Proposé",tracking=True)
    offered_wage_letters = fields.Char("Salaire Proposé en Lettre", readonly=True)
    officiel_wage = fields.Float("Salaire Validé",tracking=True)
    officiel_wage_letters = fields.Char("Salaire Validé en Lettre", readonly=True)
    period_id = fields.Many2one("account.month.period",u'Période',required=True)
    date = fields.Date('Date Fixation', default=datetime.today())
    obs = fields.Text("Observation")
    propose = fields.Boolean('Afficher Salaire validé',default=True)
    state = fields.Selection([
        ('draft',u'Nouvelle Fixation'),
        ('valide',u"Validé"),
        ('cancel',u"Annulé")
        ],u"État Fixation",
        default='draft',
        readonly=True
    )

    @api.model
    def create(self,vals):
        count = len(self.env['hr.fixation.salaire'].search([('period_id','=',vals['period_id'])])) +1
        period_id = self.env['account.month.period'].browse(vals['period_id'])
        vals['name'] = "F.S./%s/%s"%(str(count).zfill(3),period_id.code)
        if vals.get('offered_wage'):
            vals['offered_wage_letters'] = num2words(vals.get('offered_wage'), lang='fr').title()
        if vals.get('officiel_wage'):
            vals['officiel_wage_letters'] = num2words(vals.get('officiel_wage'), lang='fr').title()
        if vals['propose'] and vals['officiel_wage'] == 0:
            vals['officiel_wage'] = vals['offered_wage']
        return super(fixation_salaire,self).create(vals)
    
    def write(self,vals):
        if vals.get('period_id'):
            count = len(self.env['hr.fixation.salaire'].search([('period_id','=',vals['period_id'])])) +1
            period_id = self.env['account.month.period'].browse(vals['period_id'])
            self.name = "F.S./%s/%s"%(str(count).zfill(3),period_id.name)
        if vals.get('offered_wage'):
            vals['offered_wage_letters'] = num2words(vals.get('offered_wage'), lang='fr').title()
        if vals.get('officiel_wage'):
            vals['officiel_wage_letters'] = num2words(vals.get('officiel_wage'), lang='fr').title()
        if vals.get('propose'):
            if (vals['propose'] or self.propose) and vals['officiel_wage'] == 0:
                vals['officiel_wage'] = vals['offered_wage']
        if 'state' in vals:
            if vals['state'] == 'valide' :
                self.employee_id.contract_id.write({'wage':self.officiel_wage})
            if vals['state'] == 'cancel' :
                self.employee_id.contract_id.write({'wage':self.offered_wage})
        return super(fixation_salaire,self).write(vals)
    
    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id and self.employee_id.contract_id:
            self.offered_wage = self.officiel_wage = self.employee_id.contract_id.wage
            self.chantier_id = self.employee_id.chantier_id

    def action_valide(self):
        self.write({'state':'valide'})
    
    def action_cancel(self):
        self.write({'state':'cancel'})
    
    def action_draft(self):
        self.write({'state':'draft'})

    @api.onchange('offered_wage')
    def _onchange_offered_wage(self):
        lettre = num2words(self.offered_wage, lang='fr').title()
        self.offered_wage_letters = lettre

    @api.onchange('officiel_wage')
    def _onchange_officiel_wage(self):
        lettre = num2words(self.officiel_wage, lang='fr').title()
        self.officiel_wage_letters = lettre


    def to_draft(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft'} :
                self.state = 'draft'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )

    def to_validee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'validee','annulee'} :
                self.state = 'valide'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )
    
    def to_annulee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'annulee'} :
                self.state = 'cancel'
            else:
                raise ValidationError(
                        "Erreur, Cette action n'est pas autorisée."
                    )
        else:
            raise ValidationError(
                    "Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut."
                )