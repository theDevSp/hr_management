# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from math import *
from calendar import monthrange
from datetime import datetime

class prelevement(models.Model):
    _name = "hr.prelevement"
    _description = "Prelevement"
    _inherit = ["hr.prime",'mail.thread', 'mail.activity.mixin']

    paiement_prelevement_ids = fields.One2many("hr.paiement.prelevement","prelevement_id", string = "Détails Paiement" )
    addition_deduction = fields.Selection([
        ("prime","Prime"),
        ("prelevement","Prélèvement"),
        ],"Addition/Déduction", 
        default="prelevement",
    )
    type_prelevement = fields.Selection([
        ("en_montant","Prélèvement En Montant"),
        ("en_jour","Prélèvement En Jour"),
        ],"Type de prélèvement",
    )
    nbr_jour = fields.Float("Nombre de jours")
    salaire_jour = fields.Float("Salaire du jour")
    
    is_credit = fields.Boolean("Crédit?", default = False)
    
    first_period_id = fields.Many2one("account.month.period", string = "Première Période", required=True,compute="_compute_first_period",store=True)
    objet_emprunt = fields.Char("Objet de l'Emprunt")
    stc_id = fields.Many2one("hr.stc", string = "STC", required=False)

    @api.model
    def create(self, vals):
        credit_seq = self.env['ir.sequence'].next_by_code('hr.credit.sequence')
        prelv_seq = self.env['ir.sequence'].next_by_code('hr.prelevement.sequence')
        if vals.get("type_prelevement") and vals["type_prelevement"] == "en_jour":
            periode_retournee = self.recuperer_id_periode(vals["date_fait"])
            vals["first_period_id"] = periode_retournee
        
        vals['name'] = credit_seq if vals['is_credit'] else prelv_seq
        return super(prelevement, self).create(vals)
        
    def write(self, vals):
        
        if vals.get("echeance") or vals.get("montant_total_prime"):
            for ligne in self.paiement_prelevement_ids:
                if ligne.state == "paye":
                    raise ValidationError("Erreur, vous ne pouvez pas faire ce traitement.")
                
        if vals.get("montant_paye") and vals["montant_paye"] > self.montant_total_prime:
            raise ValidationError("Le montant payé doit être inférieur du montant et strictement supérieur à 0.")
        
        if vals.get("state") and vals["state"] == "draft" and self.state == "annulee":
            for ligne in self.paiement_prelevement_ids:
                if ligne.state == "paye":
                    raise ValidationError("Erreur, Vous avez au moins une période payée, vous devez régler la situation.")
                ligne.unlink()

        if vals.get("state") and vals["state"] == "validee":
            for ligne in self.paiement_prelevement_ids:
                if ligne.state == "paye":
                    raise ValidationError("Erreur, Vous avez au moins une période payée, vous devez régler la situation.")
                ligne.unlink()

            self.compute_prelevement()

        if vals.get("state") and vals["state"] == "annulee":
            for ligne in self.paiement_prelevement_ids:
                if ligne.state == "paye":
                    raise ValidationError("Erreur, Vous avez au moins une période payée, vous devez régler la situation.")
                
        return super(prelevement, self).write(vals)
    
    @api.depends('date_fait')
    def _compute_first_period(self):
        for record in self:
            if record.date_fait:
                record.first_period_id = self.env['account.month.period'].get_period_from_date(record.date_fait)

    def compute_prelevement(self):
        
        if self.echeance > 0 and self.echeance <= self.montant_total_prime:
            res = self.montant_total_prime / self.echeance
            nbr_periodes = ceil(res)            
            self.compute_alimenter_paiement_prelevement(nbr_periodes)
        else:
            raise ValidationError("Probléme d'échéance, Le systéme ne peut pas lancer le calcule à cause d'une erreur au niveau de l'échéance.")
            
    def compute_alimenter_paiement_prelevement(self,nbr_periodes):
        print("inside compute prelevement")
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
                        "prelevement_id" : rec.id,
                        "montant_a_payer" : rec.echeance if (var >= rec.echeance) else var,
                    }
                )
                reste += rec.echeance
            
            self.create_paiement_prelevement(paiement_lines)

    def create_paiement_prelevement(self,paiement_lines):
        for rec in paiement_lines:
            self.env["hr.paiement.prelevement"].create(rec)
        
    @api.onchange('type_prelevement')
    def _onchange_type_prelevement(self):
        self._init_nbr_salaire_jour()
        if self.type_prelevement == 'en_jour':
            self.recuperer_salaire()
        self._compute_montant()
        self._compute_echeance()

    @api.onchange("employee_id")
    def _compute_salaire_jour(self):
        self._init_nbr_salaire_jour()
        if self.type_prelevement == 'en_jour':
            self.recuperer_salaire()
        self._compute_montant()
        self._compute_echeance()

    @api.onchange('montant_total_prime')
    def _onchange_montant_total_prime(self):
        self._compute_echeance()
    
    @api.onchange('nbr_jour')
    def _onchange_nbr_jour(self):
        if self.type_prelevement == 'en_jour':
            self.recuperer_salaire()
        self._compute_montant()
        self._compute_echeance()
    
    @api.onchange('salaire_jour')
    def _onchange_salaire_jour(self):
        if self.type_prelevement == 'en_jour':
            self.recuperer_salaire()
        self._compute_montant()
        self._compute_echeance()
    def recuperer_salaire(self):
        for record in self:
            period_id = record.recuperer_id_periode(record.date_fait)
            record.salaire_jour = record.employee_id.contract_id.pp_personnel_id_many2one.get_wage_per_day(period_id)

    def _init_nbr_salaire_jour(self):
        self.nbr_jour = 0
        if self.type_prelevement == 'en_montant':
            self.salaire_jour = 0

    def _compute_montant(self):
        self.montant_total_prime = self.nbr_jour * self.salaire_jour 

    def _compute_echeance(self):
        self.echeance = self.montant_total_prime if not self.is_credit else 0

    def recuperer_id_periode(self,date_fait):
        
        return self.env['account.month.period'].get_period_from_date(date_fait)
    
    def report_derniere_periode_emprunt(self):
        query = """
            SELECT period_id FROM hr_paiement_prelevement 
            WHERE prelevement_id = %s
            ORDER BY id DESC
            LIMIT 1
        """ % (self.id)
        self.env.cr.execute(query)
        res = self.env.cr.fetchall()
        periode = self.env['account.month.period'].browse(res[0][0]).code
        return periode
    
    def to_draft(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft','validee'} :
                for ligne in self.paiement_prelevement_ids:
                    if ligne.state in ("paye","annule"):
                        ligne.state = "non_paye"
                self.state = 'draft'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Action autorisée seulement pour les administrateurs et les agents de paie.")

    def to_validee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'validee','annulee','cloture_paye','cloture'} :
                self.state = 'validee'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Action autorisée seulement pour les administrateurs et les agents de paie.")

    def to_annulee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'annulee','cloture_paye','cloture'} :
                self.state = 'annulee'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Action autorisée seulement pour les administrateurs et les agents de paie.")

    def to_cloturer_payer(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft','annulee','cloture_paye','cloture'} :
                if self.state == "validee":
                    for ligne in self.paiement_prelevement_ids:
                        if ligne.state == "non_paye":
                            ligne.state = "paye"
                self.state = 'cloture_paye'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Action autorisée seulement pour les administrateurs et les agents de paie.")

    def to_cloturer(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft','annulee','cloture_paye','cloture'} :
                if self.state == "validee":
                    for ligne in self.paiement_prelevement_ids:
                        if ligne.state == "non_paye":
                            ligne.state = "annule"
                self.state = 'cloture'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Action autorisée seulement pour les administrateurs et les agents de paie.")
     