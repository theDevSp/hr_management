# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class fiche_paie(models.Model):
    _name = "hr.payslip"
    _description = "Fiche de paie"
    _inherit = ['mail.thread','mail.activity.mixin']

    name =  fields.Char("Libellé")
    employee_id = fields.Many2one("hr.employee",string="Employé",required=True)
    chantier_id = fields.Many2one('fleet.vehicle.chantier',string="Dernier Chantier")
    period_id = fields.Many2one("account.month.period", string = "Période", required = True)
    net_pay = fields.Float('Net à payer')
    nbr_jour_travaille =  fields.Float("Nombre de jours travaillés")
    jr_travaille_par_chantier = fields.One2many("jr.travaille.par.chantier", 'fiche_paie_id',string='Jours travaillés par chantier')
    type_fiche = fields.Selection([
        ("stc","STC"),
        ("type1","Type 1"),
        ("type2","Type 2"),
        ("type3","Type 3"),
        ("type4","Type 4"),
        ],"Type de fiche", 
    )

    state  = fields.Selection([
        ("draft","Brouillon"),
        ("validee","Validée"),
        ("annulee","Annulée"),
        ],"Status", 
        default="draft",
    )
    
    affich_bonus_jour = fields.Float("Afficher bonus jour")
    affich_jour_conge = fields.Float("Afficher jour congé")
    date = fields.Date("Date")
    stc_id = fields.Many2one("hr.stc", string = "STC", required=False)
    
    @api.model
    def create(self, vals):
        return super(fiche_paie, self).create(vals)

    def write(self, vals):
        return super(fiche_paie, self).write(vals)



class loan_list(models.Model):
    _name = "loan.list"

    emprunt_id = fields.Many2one("hr.prelevement",u'Emprunt',readonly=True)
    emprunt_balance = fields.Float(related="emprunt_id.reste_a_paye",string="Reste à payer",readonly=True)
    emprunt_montant = fields.Float(related="emprunt_id.montant_total_prime",string="Montant d'emprunt",readonly=True)
    montant_payer = fields.Float(u"Montant à payer")
    add = fields.Boolean('Ajouter au calcule', default=True)
    note = fields.Char('Observation')
    stc_id = fields.Many2one("hr.stc",u'STC',ondelete='cascade')



class fiche_paie_stc(models.Model):
    _name = "hr.payslip.stc"

    payslip_id = fields.Many2one("hr.payslip",u'Fiche de paie',readonly=True)
    period_id = fields.Many2one("account.month.period", string = "Période", required = True)
    net_pay = fields.Float('Net à payer')
    chantier_id = fields.Many2one('fleet.vehicle.chantier',string="Dernier Chantier")
    emplacement_chantier_id = fields.Many2one("fleet.vehicle.chantier.emplacement",u"Équipe")
    #vehicle = fields.Many2one('fleet.vehicle',string="Dernier Engin", states=READONLY_STATES)
    stc_id = fields.Many2one("hr.stc",u'STC',ondelete='cascade')