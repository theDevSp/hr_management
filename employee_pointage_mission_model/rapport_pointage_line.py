from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError
from datetime import datetime
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
        'cancel': [('readonly', True)]
    }

    READONLY_STATES_MG = {
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


    def _get_content(self):
        self.ensure_one()
        content = []
        if self.modification_data :
            data = json.loads(self.modification_data)
            for fname in data:
                old_value = fname['old']['hours']
                new_value = fname['new']['hours']
                date = fname['new']['date']
                name = fname['new']['user_name']
                content.append((old_value, new_value, date, name))
        return content


    def _render_html(self):
        thead = ''
        for head in (('Ancienne valeur'), ('Nouvelle valeur'), ('Date de Modification'), ('Modifié Par')):
            thead += '<th>%s</th>' % head
        thead = '<thead><tr class="oe_list_header_columns">%s</tr></thead>' % thead
        tbody = ''
        for line in self._get_content():
            row = ''
            for item in line:
                row += '<td>%s</td>' % item
            tbody += '<tr>%s</tr>' % row
        tbody = '<tbody>%s</tbody>' % tbody
        self.modification_data_html = '<table class="oe_list_content">%s%s</table>' % (thead, tbody)


    def _get_modification_count(self):
        self.modification_count = max(len(self._get_content())-1,0)


    def _get_engin_resume(self):
        if (len(self.vehicle_ids) > 1):
            self.vehicle_ids_resume = self.vehicle_ids[len(self.vehicle_ids)-1].name.code+' +'+str(len(self.vehicle_ids)-1)
        elif(len(self.vehicle_ids) == 1):
            self.vehicle_ids_resume = self.vehicle_ids[len(self.vehicle_ids)-1].name.code


    def _get_chantier_domain(self):
        pointeur = self.env['res.users'].has_group("hr_management.group_pointeur")
        res = []
        query = ""
        if pointeur:
            query = """
                    select chantier_id from hr_responsable_chantier where user_id = %s;
                """   % (self.env.user.id)
        else:
            query = """
                    select id from fleet_vehicle_chantier where lower(name) not like '%gasoil%' and lower(name) not ilike '%citern%' ;
                """ 
        self.env.cr.execute(query)
        for result in self.env.cr.fetchall():
            res.append(result[0])
        return [('id', 'in',res)]  


    def _get_engin_domain(self):
        pointeur = self.env['res.users'].has_group("hr_management.group_pointeur")
        res = []
        query = ""
        if pointeur:
            query = """
                    select distinct(vehicle_id) from fleet_vehicle_chantier_affectation where
                     chantier_id in (select chantier_id from hr_responsable_chantier where user_id = %s)
                """   % (self.env.user.id)
        else:
            query = """
                    select distinct(vehicle_id) from fleet_vehicle_chantier_affectation fvca inner join fleet_vehicle fv on fv.id = fvca.vehicle_id where fv.active = true;
                """  
        self.env.cr.execute(query)
        for result in self.env.cr.fetchall():
            res.append(result[0]) 
        return [('id', 'in',res)]  
    
    employee_id = fields.Many2one("hr.employee",u"Employée", states=READONLY_STATES_RL, ondelete='cascade')
    name = fields.Char('Jour',readonly=True)
    chantier_id = fields.Many2one("fleet.vehicle.chantier",u"Chantier", states=READONLY_STATES_RL,domain=_get_chantier_domain,tracking=True)
    # vehicle_id = fields.Many2one("fleet.vehicle",u"Code engin", states=READONLY_STATES_RL,domain=_get_engin_domain,tracking=True)
    emplacement_chantier_id = fields.Many2one("fleet.vehicle.chantier.emplacement","Dernière Équipe", states=READONLY_STATES_RL,tracking=True)
    h_travailler = fields.Selection(hours_table_pointeur,u"Total Heures",default='0.0', states=READONLY_STATES_RL,tracking=True)
    h_travailler_v = fields.Selection(hours_table,string="Total Heures Validees",default='0.0', states=READONLY_STATES_MG,tracking=True)
    h_bonus = fields.Selection([('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')],u"Bonus",default='0', states=READONLY_STATES_RL,tracking=True)
    h_sup = fields.Selection(hours_table_pointeur,"Heures Supplémentaires >> 9",default='0.0', states=READONLY_STATES_MG,tracking=True)
    j_travaille = fields.Selection([('0', '0'), ('0.5', '0.5'), ('1', '1')],u"Jours Travaillés",default='0', states=READONLY_STATES_RL,tracking=True)
    j_travaille_v = fields.Selection([('0', '0'), ('0.5', '0.5'), ('1', '1'), ('1.5', '1.5'),('2','2')],u"Jours Travaillés Validés",default='0', states=READONLY_STATES_MG,tracking=True)
    day = fields.Date('Date Jour',readonly=True) 
    day_type = fields.Selection([('1',u'Jour Ouvrable'),('2',u"Dimanche"),('3',u"Jour Ferié"),('4',u"Congé"),('5',u"Absence Non Autorisée"),('6',u"Abondement de Poste"),('7',u"STC"),('8',u'Accident du Travail'),('9',u'Transfert')],u"État Jour",default='1',required=True,tracking=True)
    details = fields.Text("Travaux Détaillés", states=READONLY_STATES_RL)
    note = fields.Char("Observation", states=READONLY_STATES_MG)
    modification_count = fields.Integer("Modifier",readonly=True,compute='_get_modification_count')
    modification_data = fields.Text('Data', readonly=True)
    modification_data_html = fields.Html('HTML Data', readonly=True, compute='_render_html')
    vehicle_ids = fields.One2many("hr.rapport.pointage.line.engin",'rapport_line',string="Engins")
    vehicle_ids_resume = fields.Char('Code Engin',readonly=True,compute="_get_engin_resume")
    state = fields.Selection([('draft',u'Brouillon'),('working',u'Traitement En Cours'),('valide',u"Validé"),('compute',u"Calculé"),('done',u"Clôturé"),('cancel','Annulé')],u"Etat Ligne Pointage",default='draft',readonly=True,tracking=True)
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
        view = self.env.ref('hr_management.view_engin_list_view') if pointeur else self.env.ref('hr_management.view_engin_list_view_manager')
        
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
        query_transfert = """
                    select hrt.chantier_id_destiation,fvc.simplified_name
                    from hr_employee_transfert hrt
                    left join fleet_vehicle_chantier fvc
                    on fvc.id = hrt.chantier_id_destiation
                    where hrt.date_transfert = '%s' and hrt.state = 'done' and hrt.employee_id = %s
                """  % (res.day,res.employee_id.id)
        self.env.cr.execute(query_transfert)
        query_res_transfert = self.env.cr.dictfetchall()
        
        if len(query_res_transfert) > 0:
            res.write({
                'day_type':'9',
                'details':'Transfert vers '+query_res_transfert[0]['simplified_name'].decode('utf-8'),
                'chantier_id':query_res_transfert[0]['chantier_id_destiation']
            })
        
        query_holiday = """
                    select * from hr_holidays where
                    employee_id = %s and
                    date_start <= '%s' and date_end >= '%s' and state = 'validate'
                    
                """   % (res.employee_id.id,res.day,res.day)

        self.env.cr.execute(query_holiday)
        query_res_holiday = self.env.cr.dictfetchall()
        if len(query_res_holiday) > 0:
            placement = self.env['hr.employee'].browse(query_res_holiday[0]['employee_remplacant_id'])
            remplacant = (' - Remplacer par : ' + placement.name + ' - ' + placement.identification_id).decode('utf-8') if placement else ''
            res.write({
                'day_type':'4',
                'details':(dict(self.env['hr.holidays'].browse(query_res_holiday[0]['id']).fields_get(allfields=['motif'])['motif']['selection'])[self.env['hr.holidays'].browse(query_res_holiday[0]['id']).motif] + remplacant),
                'chantier_id':query_res_holiday[0]['chantier_id'],
                'emplacement_chantier_id':res.rapport_id.emplacement_chantier_id.id,
            })

        return res
    

    def get_normal_heur(self,date,chantier_id):
        query = """
                    select heure_normal from historique_heur_normal_chantier where
                    chantier_id = %s and day <= '%s' order by id desc limit 1     
                """   % (chantier_id.id,date)
        self.env.cr.execute(query)
        query_res = self.env.cr.fetchall()
        return query_res[0][0] if query_res else 9


    def write(self,vals):
        pointeur = self.env['res.users'].has_group("hr_management.group_pointeur")
        period_month = fields.Date.from_string(self.rapport_id.period_id.date_start).month
        period_year = fields.Date.from_string(self.rapport_id.period_id.date_start).year

        quinzaine1_first_day = str(period_year)+'-'+str(period_month)+'-01'
        quinzaine1_day_ref = str(period_year)+'-'+str(period_month)+'-18'
        quinzaine2_day_ref = str(period_year)+'-'+str(period_month + 1)+'-03' if period_month != 12 else str(period_year +1)+'-01-03'

        quinzaine1_delimite = str(period_year)+'-'+str(period_month)+'-15'
        quinzaine2_delimite = str(period_year)+'-'+str(period_month)+'-'+str(calendar.monthrange(period_year, period_month)[1])
        
        if 'state' not in vals and 'day_type' not in vals:
            if (self.rapport_id.chantier_id.periodicite == '2' or self.rapport_id.employee_id.type_emp == 's'):
                if pointeur and not self.grant_modification and not self.rapport_id.chantier_id.grant_modification and fields.Date.from_string(self.day) <= fields.Date.from_string(quinzaine2_delimite) and fields.Date.from_string(datetime.today().strftime("%Y-%m-%d")) >= fields.Date.from_string(quinzaine2_day_ref):
                    raise ValidationError(
                        "Erreur, Vous n'étes plus autorisé à modifier ce jour."
                    )
            else:
                if pointeur and not self.grant_modification and not self.rapport_id.chantier_id.grant_modification and fields.Date.from_string(self.day) <= fields.Date.from_string(quinzaine1_delimite) and fields.Date.from_string(self.day) >= fields.Date.from_string(quinzaine1_first_day) and fields.Date.from_string(datetime.today().strftime("%Y-%m-%d"))  >= fields.Date.from_string(quinzaine1_day_ref):
                    raise ValidationError(
                        "Erreur, Vous n'étes plus autorisé à modifier ce jour."
                    )  
                if pointeur and not self.grant_modification and not self.rapport_id.chantier_id.grant_modification and fields.Date.from_string(self.day) <= fields.Date.from_string(quinzaine2_delimite) and fields.Date.from_string(self.day) > fields.Date.from_string(quinzaine1_delimite) and fields.Date.from_string(datetime.today().strftime("%Y-%m-%d"))  >= fields.Date.from_string(quinzaine2_day_ref):
                    raise ValidationError(
                        "Erreur, Vous n'étes plus autorisé à modifier ce jour."
                    )

        if pointeur and self.state != 'draft' and 'state' not in vals and 'day_type' not in vals:
            raise ValidationError(
                        "Erreur, Vous n'étes plus autorisé à modifier ce jour."
                    ) 

        old = self.h_travailler
        new = 0
        user_name = self.env.user.name
        date = datetime.today().strftime("%d-%m-%Y, %H:%M:%S")
        old_data = []
        
        if self.modification_data:
            old_data = json.loads(self.modification_data)

        if vals.get('day_type'):
            if self.day_type in ('2','3') or (vals['day_type'] ==  '2' and 'Dim' not in self.name):
                vals.pop('day_type')

        if vals.get('day_type'):
            if vals['day_type'] in ('5','6','7','8'):
                self.rapport_id.write({
                    'etat':vals['day_type']
                })
                vals['details'] = dict(self.fields_get(allfields=['day_type'])['day_type']['selection'])[vals['day_type']]
            if vals['day_type'] == '1':
                self.rapport_id.write({
                    'etat':False
                })
        
        if 'h_travailler' in vals and not pointeur and self._uid != SUPERUSER_ID:
            vals.pop('h_travailler') 
        if 'h_bonus' in vals and not pointeur and self._uid != SUPERUSER_ID:
            vals.pop('h_bonus') 
        if 'h_sup' in vals and not pointeur and self._uid != SUPERUSER_ID:
            vals.pop('h_sup') 
        if 'chantier_id' in vals and not pointeur and self._uid != SUPERUSER_ID:
            vals.pop('chantier_id')
        if 'emplacement_chantier_id' in vals and not pointeur and self._uid != SUPERUSER_ID:
            vals.pop('emplacement_chantier_id')

        if 'state' not in vals and 'day_type' not in vals:
            if not self.chantier_id and not vals.get('chantier_id') and self._uid != SUPERUSER_ID:
                raise ValidationError(
                        "Erreur, Vous devez spécifier un Chantier."
                    )
            if not self.emplacement_chantier_id and not vals.get('emplacement_chantier_id')  and self._uid != SUPERUSER_ID:
                raise ValidationError(
                        "Erreur, Vous devez spécifier un Emplacement sur Chantier."
                    )
            if not self.details and not vals.get('details')  and self.employee_id.type_emp == 's' and self._uid != SUPERUSER_ID:
                raise ValidationError(
                        "Erreur, Vous devez spécifier les détails des travaux."
                    )

        res = super(hr_rapport_pointage_line,self).write(vals) 

        demi_jour = 6 if self.employee_id.type_emp == 'o' else 4.5

        chantier_id_heure_normal = self.get_normal_heur(self.day,self.chantier_id) if self.chantier_id else 0

        if not self.employee_id.job_id and self._uid != SUPERUSER_ID:
            raise ValidationError("Erreur, Veuillez ajouter un titre du poste pour Mr/Mme %s".decode('utf-8') % (self.employee_id.name))
        
        condition1 = float(self.h_travailler) > max(chantier_id_heure_normal,9)
        condition2 = not self.details and pointeur
        condition3 = self.employee_id.type_emp == 'o'
        condition4 = 'gardien' not in self.employee_id.job_id.name.lower() if self._uid != SUPERUSER_ID else True
        condition5 = float(self.h_travailler) > 0
        condition6 = self.day_type == '2'

        if (condition1 and condition2 and condition3 and condition4) or (condition5 and condition6 and condition2):
            raise ValidationError("Erreur, Veuillez justifier les heures supplémentaires pour la journée %s".decode('utf-8') % (self.name))
            
        if vals.get('h_travailler'):
            new = self.h_travailler
            old_data.append({"new":{"hours":new,"date":date,"user_name":user_name},"old":{"hours":old}})
            json_data = json.dumps(old_data)
            self.modification_data = json_data

            self.h_travailler_v = self.h_travailler
            
            self.h_sup = str(max(float(self.h_travailler) - 9.0,0.0))

            if float(self.h_travailler) > 0 and float(self.h_travailler) <= demi_jour:
                self.j_travaille = '0.5'
            elif float(self.h_travailler) > demi_jour and float(self.h_travailler)<= 24:
                self.j_travaille = '1'
            else :
                self.j_travaille = '0'

        if vals.get('h_travailler_v'):    
            if float(self.h_travailler_v) > 0 and float(self.h_travailler_v) <= demi_jour:
                self.j_travaille_v = '0.5'
            elif float(self.h_travailler_v) > demi_jour  and float(self.h_travailler_v) <= 24:
                self.j_travaille_v = '1'
            else :
                self.j_travaille_v = '0'
                
        last_line = self.env['hr.rapport.pointage.line'].search([('chantier_id','!=',False),('rapport_id','=',self.rapport_id.id)],order="id desc",limit=1)

        if self.id == last_line.id and (pointeur or self._uid == SUPERUSER_ID):
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
        # self.vehicle_id = self.rapport_id.employee_id.vehicle_id
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