from odoo import models, fields
from odoo.exceptions import ValidationError

class hr_rapport_pointage_line_engin(models.Model):
    _name="hr.rapport.pointage.line.engin"
    _description = "List Engin par Ligne de Rapport de Pointage"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_engin_domain(self):
        pointeur = self.env['res.users'].has_group("hr_management.group_pointeur")
        date_ref = self.env.context.get('date_ref')
        res = []
        query = ""
        if date_ref:
            if pointeur:
                query = """
                        select distinct(vehicle_id) from fleet_vehicle_chantier_affectation where
                        chantier_id in (select chantier_id from chantier_responsable_relation where user_id = %s)
                        and date_start <= '%s' and (date_end >= '%s' or date_end is null)
                    """  % (self.env.user.id,str(date_ref),str(date_ref))
            else:
                query = """
                        select distinct(vehicle_id) from fleet_vehicle_chantier_affectation fvca inner join fleet_vehicle fv on fv.id = fvca.vehicle_id where fv.active = true;
                    """  
            self.env.cr.execute(query)
            for result in self.env.cr.fetchall():
                res.append(result[0])
        
        return [('id', 'in',res)]  
    

    time_table = []

    for i in range(25):
        time_table.append((str('%02d' % i)+':00:00',str('%02d' % i)+':00:00'))
        time_table.append((str('%02d' % i)+':15:00',str('%02d' % i)+':15:00'))
        time_table.append((str('%02d' % i)+':30:00',str('%02d' % i)+':30:00'))
        time_table.append((str('%02d' % i)+':45:00',str('%02d' % i)+':45:00'))

    name = fields.Many2one("fleet.vehicle",u"Code engin",domain=_get_engin_domain,required=True)
    rapport_line = fields.Many2one("hr.rapport.pointage.line",string="Lignes Rapport Pointage")
    time_start = fields.Selection(time_table,string="Heure Début",required=True,tracking=True)
    time_end = fields.Selection(time_table,string="Heure Fin",required=True,tracking=True)
    color = fields.Integer('color')
