# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class job_hr(models.Model):
    _description = "Job Model"
    _inherit = ['hr.job']

    nbr_effectif_recrutes = fields.Integer(compute='_compute_nbr_effectif_recrutes', store = False, string="Nombre d'effectif acceptés",readonly=True,
        help="Le Nombre d'Effectif Acceptés.")
    nbr_employees_active_for_this_job = fields.Integer(compute='_compute_nbr_employees_active_for_this_job', store = False, string="Nombre des employés actifs occupant ce poste",readonly=True,
        help='Nombre Des Employés Actifs Occupant Ce Poste')
    nbr_effectif_prevu_where_state_encours = fields.Integer(compute='_compute_nbr_effectif_prevu_where_state_encours', store = False, string="Nombre d'effectif prévu",readonly=True,
        help="Le Nombre d'Effectif Prévu.")

    nbr_total_demandes_of_this_job = fields.Integer(compute='_compute_nbr_total_demandes_of_this_job', store = False, string="Nombre total des demandes de ce poste.",readonly=True,
        help="Le nombre total des demandes de ce poste.")

    nbr_demandes_draft = fields.Integer(compute='_compute_counts_nbr_demandes_selon_state', store = False, string="En Brouillon",readonly=True,
        help='Le nombre des demandes de recrutement en brouillon.')
    nbr_demandes_validee = fields.Integer(compute='_compute_counts_nbr_demandes_selon_state', store = False, string='Validées',readonly=True,
        help='Le nombre des demandes de recrutement validées.')
    nbr_demandes_en_cours = fields.Integer(compute='_compute_counts_nbr_demandes_selon_state', store = False, string='En Cours',readonly=True,
        help='Le nombre des demandes de recrutement en cours.')
    nbr_demandes_acceptee = fields.Integer(compute='_compute_counts_nbr_demandes_selon_state', store = False, string='Acceptées',readonly=True,
        help='Le nombre des demandes de recrutement acceptées.')
    nbr_demandes_refusee = fields.Integer(compute='_compute_counts_nbr_demandes_selon_state', store = False, string='Refusées',readonly=True,
        help='Le nombre des demandes de recrutement refusées.')
    nbr_demandes_annulee = fields.Integer(compute='_compute_counts_nbr_demandes_selon_state', store = False, string='Annulées',readonly=True,
        help='Le nombre des demandes de recrutement annulées.')
    nbr_demandes_terminee = fields.Integer(compute='_compute_counts_nbr_demandes_selon_state', store = False, string='Terminées',readonly=True,
        help='Le nombre des demandes de recrutement terminées.')

    employees_not_in_blacklist = fields.Many2many('hr.employee', string='Liste des employés occupant ce poste', compute="_employees_not_in_blacklist")


    def _compute_nbr_effectif_recrutes(self):
        for rec in self :
            query = """
                SELECT SUM(nbr_effectif_accepte)
                FROM hr_recrutement
                WHERE state='acceptee' and title_poste=%s
                ;
            """ % (rec.id)
            rec.env.cr.execute(query)
            res = rec.env.cr.fetchall()
            if len(res) > 0:
                rec.nbr_effectif_recrutes = res[0][0]
            else :
                rec.nbr_effectif_recrutes = 0

    def _compute_nbr_employees_active_for_this_job(self):
        for rec in self :
            query = """
                SELECT count(*) 
                FROM hr_job j, hr_employee emp 
                WHERE emp.job_id= j.id
                and black_list = false
                and emp.job_id=%s
                ;
            """ % (rec.id)
            rec.env.cr.execute(query)
            res = rec.env.cr.fetchall()
            if len(res) > 0:
                rec.nbr_employees_active_for_this_job = res[0][0]
            else :
                rec.nbr_employees_active_for_this_job = 0

    def _compute_nbr_effectif_prevu_where_state_encours(self):
        for rec in self :
            query = """
                SELECT SUM(nbr_effectif_accepte)
                FROM hr_recrutement
                WHERE state='encours'
                and title_poste=%s
                ;
            """ % (rec.id)
            rec.env.cr.execute(query)
            res = rec.env.cr.fetchall()
            if len(res) > 0:
                rec.nbr_effectif_prevu_where_state_encours = res[0][0]
            else :
                rec.nbr_effectif_prevu_where_state_encours = 0

    def _compute_nbr_total_demandes_of_this_job(self):
        for rec in self :
            query = """
                SELECT count(*)
                FROM hr_recrutement
                WHERE title_poste=%s
                ;
            """ % (rec.id)
            rec.env.cr.execute(query)
            res = rec.env.cr.fetchall()
            if len(res) > 0:
                rec.nbr_total_demandes_of_this_job = res[0][0]
            else :
                rec.nbr_total_demandes_of_this_job = 0

    def _compute_counts_nbr_demandes_selon_state(self):
        query = """
                    select 
                    count(1) filter (where state='draft') as d_draft,
                    count(1) filter (where state='validee') as d_validee,
                    count(1) filter (where state='encours') as d_encours,
                    count(1) filter (where state='acceptee') as d_acceptee,
                    count(1) filter (where state='refusee') as d_refusee,
                    count(1) filter (where state='annulee') as d_annulee,
                    count(1) filter (where state='terminee') as d_terminee
                    from hr_recrutement where title_poste = %s;
                """ % (self.id)

        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()[0]
            
        self.nbr_demandes_draft = res['d_draft']
        self.nbr_demandes_validee = res['d_validee']
        self.nbr_demandes_en_cours = res['d_encours']
        self.nbr_demandes_acceptee = res['d_acceptee']
        self.nbr_demandes_refusee = res['d_refusee']
        self.nbr_demandes_annulee = res['d_annulee']
        self.nbr_demandes_terminee = res['d_terminee']


    @api.depends('employee_ids')
    def _employees_not_in_blacklist(self):
        for rec in self:
            self.employees_not_in_blacklist = self.employee_ids.filtered(lambda l: l.black_list == False)