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


    nbr_demandes_recrutement_acceptees = fields.Integer(compute='_compute_count_nbr_demandes_recrutement_acceptees', store = False, string='Total des demandes acceptées',readonly=True,
        help='Le nombre des demandes de recrutement acceptées.')
    nbr_demandes_en_cours = fields.Integer(compute='_compute_nbr_demandes_en_cours', store = False, string='Total des demandes en cours',readonly=True,
        help='Le nombre des demandes de recrutement En cours.')

    #employeee_ids = fields.One2many('hr.employee', 'job_id', string='Employees', groups='base.group_user', domain="[('name','=','Employee 3')]")


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





    def _compute_count_nbr_demandes_recrutement_acceptees(self):
        for rec in self :
            query = """
                SELECT count(state)
                FROM hr_recrutement
                WHERE state = 'acceptee'
                ;
            """
            rec.env.cr.execute(query)
            res = rec.env.cr.fetchall()
            if len(res) > 0:
                rec.nbr_demandes_recrutement_acceptees = len(res)
            else :
                rec.nbr_demandes_recrutement_acceptees = 0

    