# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import fields, models, api
from odoo.exceptions import ValidationError
from math import *
from dateutil.relativedelta import relativedelta


class prime(models.Model):
    _name = "hr.prime"
    _description = "Prime"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char("Désignation")
    employee_id = fields.Many2one("hr.employee", string = "Employé")
    chantier_id = fields.Many2one("fleet.vehicle.chantier", string = "Chantier (Zone)")
    first_period_id = fields.Many2one("account.month.period", string = "Première Période", required=True,compute="_compute_first_period",store=True)
    paiement_prime_ids = fields.One2many("hr.paiement.ligne","prime_id", string = "Paiement Ligne")
    date_fait = fields.Date("Date de fait", tracking=True, index=True)
    date_start = fields.Date('Date de début')
    date_end = fields.Date('Date de fin')
    donneur_order = fields.Many2one("hr.directeur", string = "Directeur")
    responsable_id = fields.Many2one("hr.responsable.chantier", string = "Responsable")
    type_prime = fields.Many2one("hr.prime.type", string = "Type de Prime")

    montant_total_prime = fields.Float("Montant",required=True)
    echeance = fields.Float("Échéance",required=True)
    montant_paye = fields.Float("Montant payé",readonly=True, compute="_compute_montant_payer",store=True)
    reste_a_paye = fields.Float("Montant reste à payer",readonly=True, compute="_compute_reste_a_payer",store=True)
    state  = fields.Selection([
        ("draft","Brouillon"),
        ("validee","Validée"),
        ("annulee","Annulée"),
        ("cloture_paye","Clôturer et payer"),
        ("cloture","Clôturer"),
        ],"Status", 
        default="draft",
    )
    type_addition = fields.Selection(related="type_prime.type_addition")
    type_payement = fields.Selection(related="type_prime.type_payement")
    
    addition_deduction = fields.Selection([
        ("prime","Prime"),
        ("prelevement","Prélèvement"),
        ],"Addition/Déduction", 
        default="prime",
    )

    @api.depends('montant_total_prime', 'paiement_prime_ids.state')
    def _compute_montant_payer(self):
        for rec in self:
            rec.montant_paye = sum(line.montant_a_payer for line in rec.paiement_prime_ids.filtered(lambda ln: ln.state == 'paye'))
    
    @api.depends('montant_total_prime', 'montant_paye')
    def _compute_reste_a_payer(self):
        for rec in self:
            rec.reste_a_paye = rec.montant_total_prime - rec.montant_paye
    
    @api.depends('date_fait','date_start')
    def _compute_first_period(self):
        for record in self:
            date = record.date_fait 
            if record.date_end:
                date = record.date_end 
            record.first_period_id = self.env['account.month.period'].get_period_from_date(date)
    
    @api.onchange('montant_total_prime')
    def _onchange_montant_total_prime(self):
        for record in self:
            record.echeance = record.montant_total_prime

    @api.onchange('type_prime')
    def _onchange_type_prime(self):
        for record in self:
            record.montant_total_prime = record.type_prime.montant
            record.echeance = record.montant_total_prime 
            record.date_fait = False
            record.date_start = False
            record.date_end = False
    
    @api.onchange('date_fait')
    def _onchange_date_fait(self):
        for record in self:
            record.date_start = False
            record.date_end = False
    
    @api.onchange('date_start')
    def _onchange_date_start(self):
        for record in self:
            record.date_fait = False
    
    @api.onchange('date_end')
    def _onchange_date_end(self):
        for record in self:
            record.date_fait = False
    
    @api.constrains('echeance')
    def _check_echeance(self):
        if self.echeance <= 0 or self.echeance > self.montant_total_prime and self.type_payement == 'm':
            raise ValidationError("L'échéance doit être inférieur du montant et strictement supérieur à 0.")
    

    @api.model
    def create(self, vals):
        return super(prime, self).create(vals)


    def write(self, vals):
        if vals.get("echeance") or vals.get("montant_total_prime"):
            for ligne in self.paiement_prime_ids:
                if ligne.state == "paye":
                    raise ValidationError("Erreur, vous ne pouvez pas faire ce traitement.")
                
        if vals.get("montant_paye") and vals["montant_paye"] > self.montant_total_prime:
            raise ValidationError("Le montant payé doit être inférieur du montant et strictement supérieur à 0.")
        
        if vals.get("state") and vals["state"] == "draft" and self.state == "annulee":
            for ligne in self.paiement_prime_ids:
                if ligne.state == "paye":
                    raise ValidationError("Erreur, Vous avez au moins une période payée, vous devez régler la situation.")
                ligne.unlink()
    
        if vals.get("state") and vals["state"] == "annulee":
            for ligne in self.paiement_prime_ids:
                if ligne.state == "paye":
                    raise ValidationError("Erreur, Vous avez au moins une période payée, vous devez régler la situation.")
        return super(prime, self).write(vals)


    def compute_prime(self):
        if self.echeance > 0 and self.echeance <= self.montant_total_prime:
            res = self.montant_total_prime / self.echeance
            nbr_periodes = ceil(res)
            self.compute_alimenter_paiement(nbr_periodes)

    def compute_alimenter_paiement(self,nbr_periodes):
        for rec in self:
            first_period_date = rec.first_period_id.date_start

            last_period_date = rec.first_period_id.date_start + relativedelta(months=+nbr_periodes)

            paiement_lines=[]
            reste = 0
            for period in self.env['account.month.period'].search_read([('date_start','>=',first_period_date),('date_start','<',last_period_date)],['id']):
                var = rec.montant_total_prime - reste
                paiement_lines.append(
                    {
                        "period_id" : period['id'],
                        "prime_id" : rec.id,
                        "montant_a_payer" : rec.echeance if (var >= rec.echeance) else var,
                    }
                )
                reste += rec.echeance
            self.create_paiement(paiement_lines)


    def create_paiement(self,paiement_lines):
        if self.addition_deduction == "prime":
            for rec in paiement_lines:
                self.env["hr.paiement.ligne"].create(rec)
                
    def to_draft(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft','validee'} :
                if self.state == "cloture":
                    for ligne in self.paiement_prime_ids:
                        if ligne.state == "annule":
                            ligne.state = "non_paye"
                elif self.state == "cloture_paye":
                    for ligne in self.paiement_prime_ids:
                        if ligne.state == "paye":
                            ligne.state = "non_paye"
                self.state = 'draft'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut.")

    def to_validee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            self.state = 'validee'
            for ligne in self.paiement_prime_ids:
                ligne.unlink()
            self.compute_prime()
        else:
            raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut.")

    def to_annulee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            self.state = 'annulee'
        else:
            raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut.")


    def to_cloturer_payer(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state == "validee":
                for ligne in self.paiement_prime_ids:
                    if ligne.state == "non_paye":
                        ligne.state = "paye"
                self.state = 'cloture_paye'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut.")
    

    def to_cloturer(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state == "validee":
                for ligne in self.paiement_prime_ids:
                    if ligne.state == "non_paye":
                        ligne.state = "annule"
                self.state = 'cloture'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut.")

    def report_duree_nbr_periode(self):
        if self.echeance > 0 and self.echeance <= self.montant_total_prime:
            resultat = self.montant_total_prime / self.echeance
            nbr_periodes = ceil(resultat)
            return nbr_periodes
        
    def report_derniere_periode_prime(self):
        query = """
            SELECT period_id FROM hr_paiement_ligne 
            WHERE prime_id = %s
            ORDER BY id DESC
            LIMIT 1
        """ % (self.id)
        self.env.cr.execute(query)
        res = self.env.cr.fetchall()
        periode = self.env['account.month.period'].browse(res[0][0]).code
        return periode
    
    def accept_payement(self,period_id):

        for ln in self.paiement_prime_ids.filtered(lambda ln: ln.period_id.id == period_id.id and ln.state == "non_paye"):
            ln.write({
                'state':'paye'
            })
    
    def cancel_payement(self,period_id):

        for ln in self.paiement_prime_ids.filtered(lambda ln: ln.period_id.id == period_id.id and ln.state == "paye"):
            ln.write({
                'state':'non_paye'
            })