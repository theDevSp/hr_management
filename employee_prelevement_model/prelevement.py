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

    paiement_prelevement_ids = fields.One2many("hr.paiement.prelevement","prelevement_id", string = "Paiement prélèvement" )
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
    type_prelevemenet_en_jour_nbrjour = fields.Float("Nombre de jours", default="1")
    type_prelevemenet_en_jour_salairejour = fields.Float("Salaire du jour")
    
    is_credit = fields.Boolean("Crédit?", default = False)
    
    first_period_id = fields.Many2one("account.month.period", string = "Première Période", required=False)
    echeance = fields.Float("Échéance", required=False)
    objet_emprunt = fields.Text("Objet de l'Emprunt")
    stc_id = fields.Many2one("hr.stc", string = "STC", required=False)

    @api.model
    def create(self, vals):
        if vals.get("type_prelevement") and vals["type_prelevement"] == "en_jour":
            periode_retournee = self.recuperer_id_periode(vals["date_fait"])
            vals["first_period_id"] = periode_retournee
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
    

    def compute_prelevement(self):
        if self.echeance > 0 and self.echeance <= self.montant_total_prime:
            res = self.montant_total_prime / self.echeance
            nbr_periodes = ceil(res)            
            self.compute_alimenter_paiement_prelevement(nbr_periodes)
            

    def compute_alimenter_paiement_prelevement(self,nbr_periodes):
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
        

    def to_draft(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft','validee'} :
                if self.state == "cloture":
                    for ligne in self.paiement_prelevement_ids:
                        if ligne.state == "annule":
                            ligne.state = "non_paye"
                elif self.state == "cloture_paye":
                    for ligne in self.paiement_prelevement_ids:
                        if ligne.state == "paye":
                            ligne.state = "non_paye"
                self.state = 'draft'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut.")


    def to_validee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'validee','annulee','cloture_paye','cloture'} :
                self.state = 'validee'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut.")


    def to_annulee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'annulee','cloture_paye','cloture'} :
                self.state = 'annulee'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut.")


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
            raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut.")
    

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
            raise ValidationError("Erreur, Seulement les administrateurs et les agents de paie qui peuvent changer le statut.")
        

    def nbr_days_of_current_month(self):
        year_val = self.date_fait.year
        month_val = self.date_fait.month
        nbr_days = monthrange(year_val, month_val)[1]
        return nbr_days

    def recuperer_salaire(self):
        profile_paie_employee = self.env['hr.employee'].browse(self.employee_id.id)
        definition_nbr_jour = profile_paie_employee.pp_personnel_id_many2one.definition_nbre_jour_worked_par_mois
        if definition_nbr_jour == "nbr_saisie":
            self.type_prelevemenet_en_jour_salairejour = profile_paie_employee.pp_personnel_id_many2one.salaire_jour
        elif definition_nbr_jour == "jr_mois":
            nbr_days_of_current_month = self.nbr_days_of_current_month()
            self.type_prelevemenet_en_jour_salairejour = profile_paie_employee.salaire_actuel / nbr_days_of_current_month

    @api.onchange("employee_id")
    def onchange_employee_nbr_jour(self):
        self.recuperer_salaire()

    @api.onchange("type_prelevemenet_en_jour_nbrjour","type_prelevemenet_en_jour_salairejour","type_prelevement")
    def calculer_montant_onchange(self):
        if self.type_prelevement == "en_jour" and self.is_credit != True:
            nbr_jour = self.type_prelevemenet_en_jour_nbrjour
            salaire_jr = self.type_prelevemenet_en_jour_salairejour
            self.montant_total_prime = nbr_jour * salaire_jr
            self.echeance = self.montant_total_prime

    def recuperer_id_periode(self,date_fait):
        query = """
                SELECT id from account_month_period
                WHERE '%s' between date_start and date_stop;
            """  % (date_fait)
        self.env.cr.execute(query)
        res = self.env.cr.fetchall()
        return res[0][0]
    
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