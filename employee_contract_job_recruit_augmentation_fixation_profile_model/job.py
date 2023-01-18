# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class job_hr(models.Model):
    _description = "Job Model"
    _inherit = ['hr.job']

    nbr_demandes_recrutement_acceptees = fields.Integer(compute='_compute_count_nbr_demandes_recrutement_acceptees',string='Total des Demandes Acceptées', store=True, readonly=True,
        help='Le nombre des demandes de recrutement acceptées.')
    nbr_employees_active_for_this_job = fields.Integer(compute='_compute_employees',string="Nombre Des Employés Occupant Ce Poste", store=True, readonly=True,
        help='Nombre Des Employés Actifs Occupant Ce Poste')
    nbr_demandes_en_cours = fields.Integer(compute='_compute_employees', string='Total des Demandes En cours', store=True, readonly=True,
        help='Le nombre des demandes de recrutement En cours.')


    #@api.depends('vehicules_autorises_ids')
    def _compute_count_nbr_demandes_recrutement_acceptees(self):
        for rec in self :
            query = """
                SELECT state
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


