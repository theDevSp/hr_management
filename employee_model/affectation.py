# -*- coding: utf-8 -*-
from odoo import models, fields, api, SUPERUSER_ID, osv
# from io import StringIO
from datetime import date,datetime
from odoo.exceptions import ValidationError


class fleet_vehicle_chantier_affectation(models.Model):
    _name = "fleet.vehicle.chantier.affectation"
    _description = "Affectation"
    _inherit = ['mail.thread', 'mail.activity.mixin']
   
    name = fields.Char('Référence')
    # vehicle_id = fields.Many2one('fleet.vehicle','Machine',ondelete="restrict",required=True,readonly=True, states={'draft': [('readonly', False)]})
    # product_id = fields.Many2one('product.product',string='Désignation', related="vehicle_id.product_id",store=True,readonly=True)
    # capacity = fields.Char(string='Capacité', related="vehicle_id.capacity",store=True,readonly=True)
    # brand_id = fields.Many2one('product.brand', string='Marque', related="vehicle_id.brand_id",store=True,readonly=True)
    # type = fields.Char(string='Type', related="vehicle_id.designation",store=True,readonly=True)
    vehicle_chantier_id = fields.Many2one('fleet.vehicle.chantier','Chantier de départ',ondelete="restrict")
    chantier_id = fields.Many2one('fleet.vehicle.chantier','Chantier d\'arrivé',ondelete="restrict",required=True)
    date_start = fields.Date("Date de transfert",default=date.today(),required=True )
    date_end = fields.Date("Date de fin")
    state = fields.Selection([('draft','En saisie'),('done','Confirmé')],'Statut',default='draft')
    emplacement_source_id = fields.Many2one('fleet.vehicle.chantier.emplacement','Équipe de départ',ondelete="restrict")
    emplacement_chantier_id = fields.Many2one('fleet.vehicle.chantier.emplacement','Équipe d\'arrivé',ondelete="restrict")
    notes = fields.Text('Observation')

