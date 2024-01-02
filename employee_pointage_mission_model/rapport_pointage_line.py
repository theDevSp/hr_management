from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError
from datetime import datetime,date
import numpy as np
import json
import calendar

class hr_rapport_pointage_line(models.Model):    
    _name="hr.rapport.pointage.line"
    _description = "Ligne de Rapport de Pointage"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    READONLY_STATES_RL = {
        'valide': [('readonly', True)],
        'compute': [('readonly', True)],
        'done': [('readonly', True)],
        'working': [('readonly', True)],
        'cancel': [('readonly', True)]
    }

    READONLY_STATES_MG = {
        'draft': [('readonly', True)],
        'valide': [('readonly', True)],
        'compute': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)]
    }

    hours_table = []

    for i in np.arange(0.0,40.5,0.5):
        hours_table.append((str(i),str(i)))
    
    hours_table_pointeur = []

    for i in np.arange(0.0,24.5,0.5):
        hours_table_pointeur.append((str(i),str(i)))

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
    
    employee_id = fields.Many2one("hr.employee",u"Employée", states=READONLY_STATES_RL, ondelete='cascade')
    name = fields.Char('Jour',readonly=True)
    chantier_id = fields.Many2one("fleet.vehicle.chantier",u"Chantier", states=READONLY_STATES_RL,domain=_get_chantier_domain,tracking=True)
    vehicle_id = fields.Many2one("fleet.vehicle",u"Code engin", states=READONLY_STATES_RL,tracking=True)
    emplacement_chantier_id = fields.Many2one("fleet.vehicle.chantier.emplacement","Dernière Équipe", states=READONLY_STATES_RL,tracking=True)
    h_travailler = fields.Selection(hours_table_pointeur,u"Total Heures",default='0.0', states=READONLY_STATES_RL,tracking=True)
    h_travailler_v = fields.Selection(hours_table,string="Total Heures Validees",default='0.0', states=READONLY_STATES_MG,tracking=True)
    h_bonus = fields.Selection([('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')],u"Bonus",default='0', states=READONLY_STATES_RL,tracking=True)
    h_sup = fields.Selection(hours_table_pointeur,"Heures Supplémentaires >> 9",default='0.0', readonly=True)
    j_travaille = fields.Selection([('0', '0'), ('0.5', '0.5'), ('1', '1')],u"Jours Travaillés",default='0', states=READONLY_STATES_RL,tracking=True)
    j_travaille_v = fields.Selection([('0', '0'), ('0.5', '0.5'), ('1', '1'), ('1.5', '1.5'),('2','2')],u"Jours Travaillés Validés",default='0', states=READONLY_STATES_MG,tracking=True)
    day = fields.Date('Date Jour',readonly=True)
    h_sup_cal = fields.Float(string="Total Heures Supplementaire", default=0.0)
    day_type = fields.Selection([
                ('1',u'Jour Ouvrable'),
                ('2',u"Dimanche"),
                ('3',u"Jour Ferié"),
                ('4',u"Congé"),
                ('5',u"Absence Non Autorisée"),
                ('6',u"Abondement de Poste"),
                ('7',u"STC"),
                ('8',u'Accident du Travail'),
                ('9',u'Transfert'),
                ('10',u'Déplacement'),
                ('11',u'Autorisation'),
                ],u"État Jour",required=True,tracking=True)
    
    details = fields.Text("Travaux Détaillés", states=READONLY_STATES_RL)
    note = fields.Char("Observation", states=READONLY_STATES_MG)
    vehicle_ids = fields.One2many("hr.rapport.pointage.line.engin",'rapport_line',string="Engins")
    state = fields.Selection([

                ('draft',u'Brouillon'),
                ('working',u'Traitement En Cours'),
                ('valide',u"Validé"),
                ('compute',u"Calculé"),
                ('done',u"Clôturé"),
                ('cancel','Annulé')],u"Etat Ligne Pointage",default='draft',readonly=True,tracking=True)
    
    grant_modification = fields.Boolean('Autoriser la  modification')

    rapport_id = fields.Many2one("hr.rapport.pointage",u"Rapport Pointage", ondelete='cascade')

    
    def update_wizard_ref_view(self):
        admin = self.env['res.users'].has_group("hr_management.group_admin_paie")
        view = self.env.ref('hr_management.view_mmodification_history_wizard') if not admin else self.env.ref('hr_management.rapport_pointage_line_admin_form')
        target = 'new' if not admin else 'current'
        return {
            'name': 'Historiques des Modifications',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.rapport.pointage.line',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': target,
            'res_id':self.id
        }
    

    def update_engin_list(self):
        pointeur = self.env['res.users'].has_group("hr_management.group_pointeur")
        view = self.env.ref('hr_management.view_engin_list_view') #if pointeur else self.env.ref('hr_management.view_engin_list_view_manager')
        
        return {
            'name': 'Historiques des Engins',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.rapport.pointage.line',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id':self.id,
            'context':{
                'date_ref':self.day,
            }
        }
    

    def save_engin_list(self):
        if (len(self.vehicle_ids)):
            self.write({
                'vehicle_id':self.vehicle_ids[len(self.vehicle_ids)-1].name.id
                })
            self.rapport_id.write({
                'vehicle_id':self.vehicle_ids[len(self.vehicle_ids)-1].name.id
                })
        return True


    def file_upload_view(self):
        view = self.env.ref(
            'hr_management.viewfile_upload_wizard')
        
        return {
            'name': 'Pièce jointe',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.rapport.pointage.line',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id':self.id
        }


    @api.model
    def create(self,vals):
        res = super(hr_rapport_pointage_line,self).create(vals)

        return res
    

    def get_normal_heur(self,date,chantier_id):
        query = """
                    select heure_normal from historique_heure_normal_chantier where
                    chantier_id = %s and day <= '%s' order by day desc limit 1     
                """   % (chantier_id.id,date)
        self.env.cr.execute(query)
        query_res = self.env.cr.fetchall()
        return query_res[0][0] if query_res else chantier_id.heure_normal


    def write(self,vals):
        
        pointeur = self.env['res.users'].has_group("hr_management.group_pointeur")
        period_month = self.rapport_id.period_id.date_start.month
        period_year = self.rapport_id.period_id.date_start.year

        quinzaine1_first_day = datetime.strptime(str(period_year)+'-'+str(period_month)+'-01', "%Y-%m-%d")
        quinzaine1_day_ref = datetime.strptime(str(period_year)+'-'+str(period_month)+'-18', "%Y-%m-%d")
        quinzaine2_day_ref = datetime.strptime(str(period_year)+'-'+str(period_month + 1)+'-03', "%Y-%m-%d")  if period_month != 12 else datetime.strptime(str(period_year +1)+'-01-03', "%Y-%m-%d")

        quinzaine1_delimite = datetime.strptime(str(period_year)+'-'+str(period_month)+'-15', "%Y-%m-%d")
        quinzaine2_delimite = datetime.strptime(str(period_year)+'-'+str(period_month)+'-'+str(calendar.monthrange(period_year, period_month)[1]), "%Y-%m-%d")

        if 'state' not in vals and 'day_type' not in vals:
            if (self.rapport_id.chantier_id.periodicite == '2' or self.rapport_id.employee_id.type_emp != 'o'):
                if pointeur and not self.grant_modification and not self.rapport_id.chantier_id.grant_modification and datetime.strptime(str(self.day), "%Y-%m-%d") <= quinzaine2_delimite and datetime.now() >= quinzaine2_day_ref:
                    raise ValidationError(
                        "Erreur, Vous n'étes plus autorisé à modifier ce jour."
                    )
            else:
                if pointeur and not self.grant_modification and not self.rapport_id.chantier_id.grant_modification and datetime.strptime(str(self.day), "%Y-%m-%d") <= quinzaine1_delimite and datetime.strptime(str(self.day), "%Y-%m-%d") >= quinzaine1_first_day and datetime.now()  >= quinzaine1_day_ref:
                    raise ValidationError(
                        "Erreur, Vous n'étes plus autorisé à modifier ce jour."
                    )  
                if pointeur and not self.grant_modification and not self.rapport_id.chantier_id.grant_modification and datetime.strptime(str(self.day), "%Y-%m-%d") <= quinzaine2_delimite and datetime.strptime(str(self.day), "%Y-%m-%d") > quinzaine1_delimite and datetime.now()  >= quinzaine2_day_ref:
                    raise ValidationError(
                        "Erreur, Vous n'étes plus autorisé à modifier ce jour."
                    )

        if pointeur and self.state != 'draft' and 'state' not in vals and 'day_type' not in vals:
            raise ValidationError(
                        "Erreur, Vous n'étes plus autorisé à modifier ce jour."
                    ) 

        key_list = ['h_travailler','h_bonus','h_sup','chantier_id','emplacement_chantier_id']   
        for key in key_list:    
            if key in vals and not pointeur and self._uid != SUPERUSER_ID and not self.env.user._is_admin():
                vals.pop(key)

        if 'state' not in vals and 'day_type' not in vals:
            if not self.chantier_id and not vals.get('chantier_id') and pointeur:
                raise ValidationError(
                        "Erreur, Vous devez spécifier un Chantier."
                    )
            if not self.emplacement_chantier_id and not vals.get('emplacement_chantier_id')  and pointeur:
                raise ValidationError(
                        "Erreur, Vous devez spécifier un Emplacement sur Chantier."
                    )
            if not self.details and not vals.get('details')  and self.employee_id.type_emp != 'o' and pointeur:
                raise ValidationError(
                        "Erreur, Vous devez spécifier les détails des travaux."
                    )

        res = super(hr_rapport_pointage_line,self).write(vals) 


        chantier_id_heure_normal = self.get_normal_heur(self.day,self.chantier_id) if self.chantier_id else 0
        
        condition1 = float(self.h_travailler) > max(chantier_id_heure_normal,9)
        condition2 = not self.details and pointeur
        condition3 = self.employee_id.type_emp == 'o'
        condition4 = self.employee_id.contract_id.profile_paie_id.justification
        condition5 = float(self.h_travailler) > 0
        condition6 = self.day_type == '2'

        if (condition1 and condition2 and condition3 and condition4) or (condition5 and condition6 and condition2):
            raise ValidationError("Erreur, Veuillez justifier les heures supplémentaires pour la journée %s" % (self.name))
            
        if vals.get('h_travailler'):

            if self.employee_id.job_id.name.lower() != 'gardien':
                self.h_sup_cal = float(self.h_travailler) - max(chantier_id_heure_normal,9) if self.day_type == '1' else float(self.h_travailler)
            else :
                self.h_sup_cal = 0
            
            self.h_travailler_v = self.h_travailler
            self.h_sup = str(max(float(self.h_travailler) - 9.0,0.0))
            self.j_travaille = self.employee_id.contract_id.get_hours_per_day(self.h_travailler)

        if vals.get('h_travailler_v'):  
            self.j_travaille_v = self.employee_id.contract_id.get_hours_per_day(self.h_travailler_v)
                
        last_line = self.env['hr.rapport.pointage.line'].search([('chantier_id','!=',False),('rapport_id','=',self.rapport_id.id)],order="id desc",limit=1)

        if self.id == last_line.id and (pointeur or self._uid == SUPERUSER_ID or self.env.user._is_admin()):
            if self.vehicle_id:
                self.rapport_id.write({'vehicle_id':self.vehicle_id.id})
            if self.emplacement_chantier_id:
                self.rapport_id.write({'emplacement_chantier_id':self.emplacement_chantier_id.id})  
            if self.chantier_id:
                self.rapport_id.write({'chantier_id':self.chantier_id.id})      
        return res    
    

    @api.onchange("h_travailler")
    def onchange_h_travailler(self):
        self.chantier_id = self.rapport_id.employee_id.chantier_id
        self.vehicle_id = self.rapport_id.employee_id.vehicle_id
        self.emplacement_chantier_id = self.rapport_id.employee_id.emplacement_chantier_id

    
    @api.onchange("day_type")
    def onchange_day_type(self):
        if not self.chantier_id:
            self.chantier_id = self.rapport_id.employee_id.chantier_id


    def action_validation(self):
        self.write({'state': 'valide'})
    
    def action_draft(self):
        self.write({'state': 'draft'})
    
    def action_cancel(self):
        self.write({'state': 'cancel'})
    
    def action_done(self):
        self.write({'state': 'done'})
        
    def action_working(self):
        self.write({'state': 'working'})
