# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class profilepaiepersonnel(models.Model):
    _name = "hr.profile.paie.personnel"
    _description = "Profile de paie Personnel"
    _inherit = ['hr.profile.paie','mail.thread', 'mail.activity.mixin']

        
    @api.depends('contract_id.salaire_actuel','contract_id.wage','nbre_jour_worked_par_mois','definition_nbre_jour_worked_par_mois')
    def _compute_salaire_jour(self):
        self.salaire_jour = self.get_wage_per_day()

    @api.depends('contract_id.salaire_actuel','contract_id.wage','nbre_heure_worked_par_jour')
    def _compute_salaire_hour(self):
        self.salaire_heure = self.get_wage_per_hour()
    
    @api.depends('contract_id.salaire_actuel','contract_id.wage','nbre_heure_worked_par_demi_jour')
    def _compute_salaire_demi_jour(self):
        self.salaire_demi_jour = self.get_wage_per_half_day()

    contract_id = fields.Many2one("hr.contract", "Contrats",ondelete="cascade")

    salaire_mois = fields.Float("Salaire du mois")
    salaire_jour = fields.Float("Salaire du jour",compute="_compute_salaire_jour")
    salaire_demi_jour = fields.Float("Salaire du demi-jour",compute="_compute_salaire_demi_jour")
    salaire_heure = fields.Float("Salaire d'heure",compute="_compute_salaire_hour")

    @api.constrains('nbre_heure_worked_par_jour')
    def _check_nbre_heure_worked_par_jour(self):
        if self.nbre_heure_worked_par_jour <= 0:
            raise ValidationError("Les Heures et Jours travaillés doivent être supérieurs de la valeur 0.")

    
    @api.constrains('nbre_heure_worked_par_demi_jour')
    def _check_nbre_heure_worked_par_demi_jour(self):
        if self.nbre_heure_worked_par_demi_jour <= 0:
            raise ValidationError("Les Heures et Jours travaillés doivent être supérieurs de la valeur 0.")


    @api.constrains('nbre_jour_worked_par_mois')
    def _check_nbre_jour_worked_par_mois(self):
        if self.nbre_jour_worked_par_mois <= 0:
            raise ValidationError("Les Heures et Jours travaillés doivent être supérieurs de la valeur 0.")

    @api.model
    def create(self, vals):
        res = super(profilepaiepersonnel, self).create(vals)
        #res.salaire_jour = res.salaire_mois / res.nbre_jour_worked_par_mois
        #res.salaire_heure = res.salaire_jour / res.nbre_heure_worked_par_jour
        #res.salaire_demi_jour = res.salaire_heure * res.nbre_heure_worked_par_demi_jour
        return res


    def write(self, vals):
        return super(profilepaiepersonnel, self).write(vals)
    
    def get_wage_per_day(self,period=False):
        res = 0
        for record in self:    
            if record:    
                
                period_obj = self.env['account.month.period']
                contract_wage = record.get_contract_wage_after_raise()
                month_range = period.get_number_of_days_per_month() if period else period_obj.get_number_of_days_per_month(datetime.now()) 

                nbrjpm = record.nbre_jour_worked_par_mois if record.definition_nbre_jour_worked_par_mois == 'nbr_saisie' else month_range

                if record.contract_id and record.contract_id.type_salaire == 'j':
                    res = contract_wage
                elif record.contract_id and record.contract_id.type_salaire == 'm':
                    res = contract_wage / nbrjpm
                else:
                    res = contract_wage * record.nbre_heure_worked_par_jour

        return res
    
    def get_wage_per_half_day(self,period=False):
        res = 0
        for record in self: 
            res = record.get_wage_per_hour(period=period) * record.nbre_heure_worked_par_demi_jour
        return res
    
    def get_wage_per_hour(self,period=False):
        res = 0
        for record in self:
            if record.contract_id and record.contract_id.type_salaire != 'h':
                res = record.get_wage_per_day(period=period) / record.nbre_heure_worked_par_jour
            else:
                res = record.get_contract_wage_after_raise()
        return  res

    def get_contract_wage_after_raise(self):
        
        for record in self:
            raise_obj = self.env['hr.augmentation']
            period_obj = self.env['account.month.period']
            contract_start_period = period_obj.get_period_from_date(record.contract_id.date_start)
            contract_wage = record.contract_id.wage + raise_obj.get_sum_of_raises_by_period_id(employee_id = record.contract_id.employee_id,period_id = contract_start_period)

        return contract_wage