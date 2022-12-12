# -*- coding: utf-8 -*-
# from odoo import http


# class HrManagement(http.Controller):
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
