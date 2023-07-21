# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class HrManagement(http.Controller):
    @http.route('/hr_management/get_line_paiement/<int:employee_id>/<int:period_id>', type='json', auth='user')
    def get_prime_list(self,employee_id,period_id):
        prime = http.request.env['hr.prime']
        res = []
        
        for line in prime.search([
                    ('state','!=','draft'),
                    '|',
                        '&',
                        ('employee_id','=',employee_id),
                        ('first_period_id','<=',period_id),
                        '&',
                        ('employee_id','=',False),
                        ('first_period_id','<=',period_id)
                        ]).paiement_prime_ids.filtered(lambda ln: ln.period_id.id == period_id):
            res.append({
                'period': line.period_id.code,
                'nbr_days': 0,
                'amount':line.montant_a_payer,
                'state':dict(line.fields_get(allfields=['state'])['state']['selection'])[line.state],
                'note':line.observations,
                'prime':{
                    'label':line.prime_id.type_prime.name,
                    'add_rate':line.prime_id.type_prime.type_addition,
                    'pay_rate':line.prime_id.type_prime.type_payement,
                    'condition':line.prime_id.type_prime.payement_condition,
                    'j_m':line.prime_id.type_prime.j_m,
                    'date_start':line.prime_id.date_start,
                    'date_end':line.prime_id.date_end
                },
                'payement_id':line.id,
                'prime_id':line.prime_id.id
            })
        return {
            'result':res
        }
    
    @http.route('/hr_management/get_line_prelevement/<int:employee_id>/<int:period_id>', type='json', auth='user')
    def reset_prime_table(self,employee_id,period_id):
        prelevement = http.request.env['hr.prelevement']
        res = []
        
        for line in prelevement.search([
                    ('state','!=','draft'),
                    '|',
                        '&',
                        ('employee_id','=',employee_id),
                        ('first_period_id','<=',period_id),
                        '&',
                        ('employee_id','=',False),
                        ('first_period_id','<=',period_id)
                        ]).paiement_prelevement_ids.filtered(lambda ln: ln.period_id.id == period_id):
            
            res.append({
                'period': line.period_id.code,
                'amount':line.montant_a_payer,
                'state':dict(line.fields_get(allfields=['state'])['state']['selection'])[line.state],
                'note':line.observations,
                'label':line.prelevement_id.objet_emprunt if line.prelevement_id.is_credit else dict(line.prelevement_id.fields_get(allfields=['type_prelevement'])['type_prelevement']['selection'])[line.prelevement_id.type_prelevement],
                'payement_id':line.id,
                'is_creadit':line.prelevement_id.is_credit,
                'prelevement_id':line.prelevement_id.id
            })
        return {
            'result':res
        }
    
"""   
    @http.route('/hr_management/get_per_day_line_paiement/<int:period_id>', type='json', auth='user')
    def get_prime_per_day_list(self,period_id):
        cr = request.cr
        query = 
                    SELECT id
                    FROM hr_prime
                    WHERE type_prime in (select id from hr_prime_type where type_payement = 'j' and type_addition = 'perio')
                    AND state = 'validee' ANd first_period_id <= %s
                %(period_id)
        cr.execute(query)
        for line in prime.search([
                    ('state','=','validee'),
                    '|',
                        '&',
                        ('employee_id','=',employee_id),
                        ('first_period_id','<=',period_id),
                        ('first_period_id','<=',period_id)
                        ]).paiement_prime_ids.filtered(lambda ln: ln.period_id.id == period_id):
            res.append({
                'period': line.period_id.code,
                'amount':line.montant_a_payer,
                'state':line.state,
                'note':line.observations,
                'prime':{
                    'label':line.prime_id.type_prime.name,
                    'add_rate':line.prime_id.type_prime.type_addition,
                    'pay_rate':line.prime_id.type_prime.type_payement,
                    'condition':line.prime_id.type_prime.payement_condition,
                    'j_m':line.prime_id.type_prime.j_m
                },
                'id':line.id
                
            })
        return {
            'result':res
        }
"""

#     @http.route('/hr_management/hr_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_management/hr_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_management.listing', {
#             'root': '/hr_management/hr_management',
#             'objects': http.request.env['hr_management.hr_management'].search([]),
#         })

#     @http.route('/hr_management/hr_management/objects/<model("hr_management.hr_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_management.object', {
#             'object': obj
#         })
