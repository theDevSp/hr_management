from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError,UserError

class mass_holiday_creation_wizard(models.TransientModel):       

    _name = "mass.holiday.creation.wizard"
    
    def _get_chantier_domain(self):
        pointeur = self.env['res.users'].has_group("hr_management.group_pointeur")
        
        res = []
        if pointeur :
            for user_chantier in self.env.user.chantier_responsable_ids:
                res.append(user_chantier.id)
        else:
            for chantier in self.env['fleet.vehicle.chantier'].search([('type_chantier','in',('Chantier','Depot','Poste'))]):
                res.append(chantier.id)
        
        return [('id', 'in',res)]
    
    chantier_id = fields.Many2one('fleet.vehicle.chantier',domain=_get_chantier_domain,string="Chantier",required=True) 
    motif = fields.Selection([
        ('arret_mawlid','Arrét Aid Al Maoulid'),
        ('arret_fitr','Arrét Aid Al Fitr'),
        ('arret','Arrét Aid Al Adha'),
        ],"Motif", required=True
    )
    date_start = fields.Date('Date de début')
    date_end = fields.Date('Date de fin')
    duree_jours = fields.Float("Durée jour", readonly=True)
    excluded_employee_ids = fields.One2many('excluded.employee', 'main_list_id', string='excluded_employee')

    @api.onchange("date_start","date_end")
    def onchange_dates(self):
        date_difference = self.env['hr.holidays'].get_duree(self.date_start,self.date_end)
        self.duree_jours = date_difference

    def create_holiday(self):

        excluded_list = []

        for ex_employee in self.excluded_employee_ids:
            excluded_list.append(ex_employee.employee_id.id)

        list_employee = self.env['hr.employee'].search([("chantier_id","=",self.chantier_id.id),("id","not in",excluded_list)])

        data_list = []

        for employee in list_employee:
            data_list.append({
                'employee_id':employee.id,
                'chantier_id':self.chantier_id.id,
                'motif':self.motif,
                'state':'confirm',
                'date_start':self.date_start,
                'date_end':self.date_end,
                'duree_jours':self.env['hr.holidays'].get_duree(self.date_start,self.date_end)
            })
        print(data_list)
        print(excluded_list)
        return

class excluded_employee(models.TransientModel):
    _name = 'excluded.employee'
    
    main_list_id = fields.Many2one('mass.holiday.creation.wizard', string='main_list')
    employee_id = fields.Many2one('hr.employee', string='employee')
    cin = fields.Char(related='employee_id.cin',readonly=True)
    job_id = fields.Many2one(related='employee_id.job_id',readonly=True)
    type_emp = fields.Selection(related='employee_id.type_emp', string='type_emp',readonly=True)
    emplacement_chantier_id = fields.Many2one(related='employee_id.emplacement_chantier_id', string='Equipe',readonly=True)
    vehicle_id = fields.Many2one(related='employee_id.vehicle_id', string='Code Engin',readonly=True)
    