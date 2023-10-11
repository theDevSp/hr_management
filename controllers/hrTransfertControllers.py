from odoo import http
from odoo.exceptions import UserError
from odoo.http import request, Controller, route


class transfertController(http.Controller):

    @http.route('/hr_management/get_transfert/<int:id>', type='json', auth='user')
    def get_transfert_by_id(self, id):
        transfert = request.env['hr.employee.transfert'].search([('id', '=', id)])
        data = transfert[0]
        
        try:  
            return {
                'code':200,
                'msg':'succes',
                'transfert_num': data.name,
                'transfert_employe_name': data.employee_id.name.upper(),
                'transfert_employe_cin': data.employee_id.cin.upper().strip(),
                'transfert_employe_fonction': data.employee_id.job.upper(),
                'transfert_chantier_depart': data.chantier_id_source.code+" - "+data.chantier_id_source.simplified_name.upper(),
                'transfert_chantier_dest': data.chantier_id_destiation.code+" - "+data.chantier_id_destiation.simplified_name.upper(),
                'transfert_date_depart':data.date_transfert,
            }
        except:
            return {
                'code':504,
                'msg':'error'
            }