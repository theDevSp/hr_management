# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import date
import calendar

class addition_list(models.Model):
    _name = "addition.list"

    prime_id = fields.Many2one("hr.prime",u'Prime',readonly=True,required=True)
    prime_reste = fields.Float(related="prime_id.reste_a_paye",string="Reste à payer",readonly=True)
    prime_montant = fields.Float(related="prime_id.montant_total_prime",string="Montant d'emprunt",readonly=True)
    montant_payer = fields.Float(u"Montant à payer")
    add = fields.Boolean('Ajouter au calcule', default=True)
    note = fields.Char('Observation')
    stc_id = fields.Many2one("hr.stc",u'STC',ondelete='cascade')
    state = fields.Selection(related="prime_id.state",string="Status",readonly=True)


class deduction_list(models.Model):
    _name = "deduction.list"

    prelevement_id = fields.Many2one("hr.prelevement",u'Prélévement',readonly=True,required=True)
    prelevement_reste = fields.Float(related="prelevement_id.reste_a_paye",string="Reste à payer",readonly=True)
    prelevement_montant = fields.Float(related="prelevement_id.montant_total_prime",string="Montant d'emprunt",readonly=True)
    montant_payer = fields.Float(u"Montant à payer")
    add = fields.Boolean('Ajouter au calcule', default=True)
    note = fields.Char('Observation')
    stc_id = fields.Many2one("hr.stc",u'STC',ondelete='cascade')
    state = fields.Selection(related="prelevement_id.state",string="Status",readonly=True)


class fiche_paie_stc(models.Model):
    _name = "hr.payslip.stc"

    payslip_id = fields.Many2one("hr.payslip",u'Fiche de paie',readonly=True,required=True)
    period_id = fields.Many2one(related="payslip_id.period_id", string = "Période", required = True,readonly=True)
    net_pay = fields.Float(related="payslip_id.net_pay", string = 'Net à payer',readonly=True)
    chantier_id = fields.Many2one('fleet.vehicle.chantier',string="Dernier Chantier")
    emplacement_chantier_id = fields.Many2one("fleet.vehicle.chantier.emplacement",u"Équipe")
    vehicle_id = fields.Many2one('fleet.vehicle',string="Dernier Engin")
    add = fields.Boolean('Ajouter au calcule', default=True)
    stc_id = fields.Many2one("hr.stc",u'STC',ondelete='cascade')
    state = fields.Selection(related="payslip_id.state",string="Status",readonly=True)


    @api.onchange('payslip_id')
    def _onchange_payslip_id(self):
        self.chantier_id = self.payslip_id.chantier_id
        self.emplacement_chantier_id = self.payslip_id.emplacement_chantier_id
        self.vehicle_id = self.payslip_id.vehicle_id