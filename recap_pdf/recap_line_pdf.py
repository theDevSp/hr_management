# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json


class recap_line_pdf(models.Model):
    _name = "hr.recap.line.pdf"
    _description = "Recap Line PDF"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    chantier_id = fields.Many2one("fleet.vehicle.chantier", u"Chantier")
    emplacement_chantier_id = fields.Many2one(
        "fleet.vehicle.chantier.emplacement", "Équipe")
    nombre_effectif = fields.Integer(
        "Nombre D'effectif", compute='_compute_effectif', store=True)
    montant_total = fields.Float(
        "Montant total", compute='_compute_montant_total', store=True)  # compute
    recap_pdf_id = fields.Many2one(
        "hr.recap.pdf", u"Recap", ondelete="cascade")

    fiche_paie_ids = fields.One2many(
        'hr.payslip', 'recap_id', string='fiche_paie')

    json_data = fields.Json('JSONData')

    @api.depends('fiche_paie_ids.net_pay')
    def _compute_montant_total(self):
        for line in self:
            line.montant_total = round(sum(i.net_pay for i in line.fiche_paie_ids))

    @api.depends('fiche_paie_ids')
    def _compute_effectif(self):
        for line in self:
            line.nombre_effectif = len(line.fiche_paie_ids)

    @api.model
    def create(self, vals):

        res = super().create(vals)
        paie_totals = []

        fiche_paies = self.env['hr.payslip'].search(
            [
                ('period_id', '=', res.recap_pdf_id.period_id.id),
                ('chantier_id', '=', res.chantier_id.id),
                ('quinzaine', '=', res.recap_pdf_id.quinzaine),
                ('emplacement_chantier_id', '=', res.emplacement_chantier_id.id),
                #('state','=','validee'),
                #('state','=','done'),
            ]
        )

        for fiche in fiche_paies:
            fiche.write({'recap_id': res.id})

            # Check if payement_mode_id.name is already in paie_totals
            mode_found = next((mode_dict for mode_dict in paie_totals if mode_dict['mode'] == fiche.employee_id.rib_number.payement_mode_id.name), None)

            if mode_found:
                mode_found['total'] += float(fiche.net_pay)
            else:
                paie_totals.append({'mode': fiche.employee_id.rib_number.payement_mode_id.name, 'total': float(fiche.net_pay)})

        
        modes = self.env['payement.mode'].search([])

        for mode in modes:
            
            mode_found = next((mode_dict for mode_dict in paie_totals if mode_dict['mode'] == mode.name), None)

            if not mode_found:
                paie_totals.append({'mode': mode.name, 'total': float(0)})
                
        for mode_dict in paie_totals:
            mode_dict['total'] = round(mode_dict['total'])
        
        res.json_data = paie_totals

        return res

        """modes = ['ES','VIR','VER']
        for i in mode:
            sum"""

    """compute montant total -> sum of nap
    
    compute json data -> 
    {
        payement_mode_id,
        nap
    },
    {

    },
    {

    }
    compute nombre d'effectif -> taille of one2many"""
