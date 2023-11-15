# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import date
import calendar

class recap_pdf(models.Model):
    _name = "hr.recap.pdf"
    _description = "Recap PDF"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Référence",readonly=True)
    period_id = fields.Many2one("account.month.period", string = "Période", required = True)
    quinzaine = fields.Selection([('quinzaine1',"Première quinzaine"),('quinzaine2','Deuxième quinzaine'),('quinzaine12','Q1 + Q2')],string="Quinzaine", required = True)
    type_emp = fields.Selection([("s","Salarié"),("o","Ouvrier")],string=u"Type d'employé",default="s")
    responsable_id = fields.Many2one("res.users","Responsable de paie",domain=lambda self: [("groups_id", "=",self.env.ref("hr_management.group_agent_paie").id)],default=lambda self: self.env.user)
    line_ids= fields.One2many("hr.recap.line.pdf","recap_pdf_id",u"Lignes de Recap")

    show_line_ids = fields.Boolean(string="Show Line IDs", default=False)

    type_fiche = fields.Selection([
        ("payroll","Payement Salaire"),
        ("refund","Rembourssement"),
        ("noob","Nouveau Embauche / Réembauche")
        ],"Type de fiche", default="payroll"
    )

    state  = fields.Selection([
        ("draft","Brouillon"),
        ('valide', 'Validée'),
        ("cloture","Clôturé"),
        ],"Status", 
        default="draft",
    )

    status  = fields.Selection([
        ("done","Payée"),
        ("approuved","Clôturé"),
        ("blocked","Bloquée"),
        ],"Status",
        default="done",
    )

    def to_validee(self):
        self.write({'state': 'valide'})
        self.show_line_ids = True
        
    def to_draft(self):
        self.write({'state': 'draft'})
        self.show_line_ids = False
        self.line_ids.unlink()
        
    def to_done(self):
        self.write({'state': 'cloture'})
    
    @api.onchange('type_emp')
    def _onchange_type_emp(self):
        if self.type_emp == 's':
            self.quinzaine = 'quinzaine12'
        else:
            self.quinzaine = 'quinzaine1'
        
    @api.model
    def create(self, vals):

        res = super().create(vals)

        recap_sequence = self.env['ir.sequence'].next_by_code('recap.pdf')
        start = ''.join([word[0] for word in res.responsable_id.name.split()])
        res.name = start +'/'+ res.period_id.code +'/'+str(recap_sequence)
        
        return res