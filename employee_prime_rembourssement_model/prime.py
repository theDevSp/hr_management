# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from math import *

class prime(models.Model):
    _name = "hr.prime"
    _description = "Prime"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(related="type_prime.name", default="########")
    employee_id = fields.Many2one("hr.employee", string = "Employee")
    first_period_id = fields.Many2one("account.month.period", string = "Première Période", required=True)
    paiement_prime_ids = fields.One2many("hr.paiement.prime","prime_id", string = "Paiement prime")
    date_fait = fields.Date("Date de fait", required=True, default=fields.Date.today, tracking=True, index=True)
    donneur_order = fields.Many2one("hr.directeur", string = "Directeur")
    responsable_id = fields.Many2one("hr.responsable.chantier", string = "Responsable")
    type_prime = fields.Many2one("hr.prime.type", string = "Type de Prime", required=True)
    currency_id = fields.Many2one("res.currency", string = "Symbole Monétaire")
    montant_total_prime = fields.Monetary("Montant", currency_field = "currency_id", required=True)
    echeance = fields.Monetary("Échéance", currency_field = "currency_id", required=True)
    montant_paye = fields.Monetary("Montant payé", currency_field = "currency_id", readonly=True)
    reste_a_paye = fields.Monetary("Montant reste à payer", currency_field = "currency_id", readonly=True, compute="_compute_reste_a_payer")
    state  = fields.Selection([
        ("draft","Brouillon"),
        ("validee","Validée"),
        ("annulee","Annulée"),
        ("cloture_paye","Clôturer et payer"),
        ("cloture","Clôturer"),
        ],"Status", 
        default="draft",
    )
    type_addition = fields.Char("Type d'addition")
    
    addition_deduction = fields.Selection([
        ("addition","Addition"),
        ("deduction","Déduction"),
        ],"Addition/Déduction", 
        default="addition",
    )

    @api.depends('montant_total_prime', 'montant_paye')
    def _compute_reste_a_payer(self):
        for rec in self:
            rec.reste_a_paye = rec.montant_total_prime - rec.montant_paye
    
    @api.onchange("type_prime")
    def onchange_type_prime(self):
        self.montant_total_prime = self.type_prime.montant
        self.type_addition = self.type_prime.type_addition
    
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
            raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le status.")

    def to_validee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'validee','annulee','cloture_paye','cloture'} :
                self.state = 'validee'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le status.")

    def to_annulee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'annulee','cloture_paye','cloture'} :
                self.state = 'annulee'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le status.")


    def to_cloturer_payer(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft','annulee','cloture_paye','cloture'} :
                if self.state == "validee":
                    for ligne in self.paiement_prime_ids:
                        if ligne.state == "non_paye":
                            ligne.state = "paye"
                self.state = 'cloture_paye'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le status.")
    

    def to_cloturer(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft','annulee','cloture_paye','cloture'} :
                if self.state == "validee":
                    for ligne in self.paiement_prime_ids:
                        if ligne.state == "non_paye":
                            ligne.state = "annule"
                self.state = 'cloture'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le status.")


    @api.constrains('echeance')
    def _check_echeance(self):
        if self.echeance <= 0 or self.echeance > self.montant_total_prime :
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
                ligne.unlink()
        if vals.get("state") and vals["state"] == "validee":
            if vals.get("echeance") or vals.get("montant_total_prime"):
                for ligne in self.paiement_prime_ids:
                    ligne.unlink()
            self._compute_prime()
        return super(prime, self).write(vals)


    def _compute_prime(self):
        if self.echeance > 0 and self.echeance <= self.montant_total_prime:
            res = self.montant_total_prime / self.echeance
            nbr_periodes = ceil(res)
            self._compute_alimenter_paiement(nbr_periodes)


    def _compute_alimenter_paiement(self,nbr_periodes):
        for rec in self:
            query = """
                    SELECT id from account_month_period
                    WHERE id >= '%s'
                    LIMIT %s;
                """  % (rec.first_period_id.id, nbr_periodes)
            rec.env.cr.execute(query)
            res = rec.env.cr.fetchall()
            paiement_lines=[]
            reste = 0
            for id in res:
                var = rec.montant_total_prime - reste
                paiement_lines.append(
                    {
                        "period_id" : id[0],
                        "prime_id" : rec.id,
                        "montant_a_payer" : rec.echeance if (var >= rec.echeance) else var,
                    }
                )
                reste += rec.echeance
            self.create_paiement(paiement_lines)


    def create_paiement(self,paiement_lines):
        for rec in paiement_lines:
            self.env["hr.paiement.prime"].create(rec)

