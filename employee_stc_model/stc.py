# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import date
import calendar
from lxml import etree


class hr_stc(models.Model):
    _name = "hr.stc"
    _description = "STC"
    _inherit = ['mail.thread','mail.activity.mixin']

    READONLY_STATES = {
        'cancel': [('readonly', True)],
        'valide': [('readonly', True)],
        'done': [('readonly', True)]
    }

    def _count_by_year(self):
        query = """
                select count(*) from hr_stc where job_id = %s and extract(year from date_start) = %s and id <= %s
                """% (self.job_id.id,fields.Date.from_string(self.date_start).year,self.id)
        self.env.cr.execute(query)
        result = self.env.cr.fetchall()
        self.count_by_year = str(result[0][0])+'/'+str(fields.Date.from_string(self.date_start).year)
        return

    name = fields.Char(u"Référence" ,readonly=True, default="New")
    employee_id = fields.Many2one("hr.employee",u"Employée",required=True)
    job_id = fields.Many2one('hr.job',string="Titre du Poste")
    cin = fields.Char(related='employee_id.cin',string='N° CIN' ,readonly=True)
    job = fields.Char(u'FONCTION', states=READONLY_STATES)
    date_debut = fields.Date(related='contract.date_start',string="Date de début" , states=READONLY_STATES)
    date_fin = fields.Date(related='contract.date_end',string="Date de fin", states=READONLY_STATES)
    chantier = fields.Many2one('fleet.vehicle.chantier',string="Dernier Chantier" , states=READONLY_STATES)
    #vehicle = fields.Many2one('fleet.vehicle',string="Dernier Engin", states=READONLY_STATES)
    bank = fields.Char(related='employee_id.bank_account',string='N° RIB' ,readonly=True)
    date_start = fields.Date(u"Date du STC", default=datetime.today(), states=READONLY_STATES)
    modePay = fields.Selection([('mode1',u'Mise à disposition'),('mode2',u"Virement Postal"),('mode3',u"Virement Bancaire"),('mode4',u"Espèce")],u"Mode de paiement", states=READONLY_STATES)
    contract = fields.Many2one('hr.contract',string="Contrat" ,readonly=True)
    employee_type = fields.Selection(related='employee_id.type_emp',string="Type d'employé")

    motif = fields.Text(u"Motif", states=READONLY_STATES)
    note = fields.Text(u"Observation", states=READONLY_STATES)
    
    montant_total = fields.Float(u"Montant total (DH)",readonly=True)
    currency_id = fields.Many2one('res.currency', string = 'Symbole Monétaire')
    salaire = fields.Monetary(related="contract.wage",string="Salaire de base" ,currency_field = 'currency_id',readonly=True)
    
    nombre_dimanche_a_payer = fields.Selection([
            ('1',u'Tous les jours'),
            ('2',u"50 %"),
            ('3',u"25 %")
        ],u"Nbrs dimanches à calculer",default=1, states=READONLY_STATES,track_visibility='onchange')
    
    montant_dim = fields.Float(u"Montant des dimanches",readonly=True)
    jr_dim = fields.Float(u"Nombre des dimanches", states=READONLY_STATES,track_visibility='onchange')

    prime = fields.Float(u"Prime (DH)", states=READONLY_STATES,track_visibility='onchange')
    licenciement = fields.Float(u"Licenciement (DH)", states=READONLY_STATES,track_visibility='onchange')
    dgi = fields.Float(u"Dommage et intérêts (DH)", states=READONLY_STATES,track_visibility='onchange')
    amande = fields.Float(u"Amende (DH)", states=READONLY_STATES,track_visibility='onchange')
    retenu = fields.Float(u"Prélèvement (DH)", states=READONLY_STATES,track_visibility='onchange')

    emprunt = fields.Float(u"Reste Emprunts (DH)",readonly=True)
    emprunt_lines = fields.One2many("loan.list", 'stc_id',string='Liste des emprunts', states=READONLY_STATES)

    reste_salaire = fields.Float(u"Reste du salaire (DH)",readonly=True)
    valide_salaire = fields.Float(u"Montant Validé (DH)", states=READONLY_STATES,track_visibility='onchange')
    payslip_lines = fields.One2many("hr.payslip.stc", 'stc_id',string='Fiche Paie', states=READONLY_STATES)

    jr_conge = fields.Float(u"Panier Congés", states=READONLY_STATES,track_visibility='onchange')
    jr_conge_m = fields.Float(u"Montant Congés",readonly=True)

    jr_block = fields.Float(u"Jours Restants", states=READONLY_STATES,track_visibility='onchange')
    jr_block_m = fields.Float(u"Montant Restants",readonly=True)

    last_period_days = fields.Float(u"La dernière période (nbr Jours)" ,readonly=True)
    preavis_retenu = fields.Float(u"Préavis à retenir (Jours)", states=READONLY_STATES,track_visibility='onchange')
    preavis_ajouter = fields.Float(u"Préavis à ajouter (Jours)", states=READONLY_STATES,track_visibility='onchange')
    preavis_retenu_m = fields.Float(u"Montant (DH)",readonly=True)
    preavis_ajouter_m = fields.Float(u"Montant (DH)",readonly=True)
    frais_depense = fields.Float(u"Frais de dépense (DH)", states=READONLY_STATES,track_visibility='onchange')
    frais_route = fields.Float(u"Frais de route (DH)", states=READONLY_STATES,track_visibility='onchange')
    cimr = fields.Float(u"Cotisation CIMR (DH)", states=READONLY_STATES,track_visibility='onchange')
    #profile_paie = fields.Many2one(related='contract.function.function_id',string="Profile Paie",readonly=True)
    profile_paie  = fields.Many2one(related="employee_id.contract_id.pp_personnel_id_many2one",string='Profile de paie',readonly=True)
    
    count_by_year = fields.Char(compute="_count_by_year")

    state = fields.Selection([
        ('draft',u'Broullion'),
        ('valide',u"Validé"),
        ('done',u"Términé"),
        ('cancel',u"Annulé")
    ],u"Statut",default='draft')

    ordre = fields.Selection([
        ('order1',u'M.Abdenabi'),
        ('order2',u"M.Abderrahim"),
        ('order3',u"M.Khalid")
    ],u"Par Ordre de", states=READONLY_STATES)

    def action_cancel(self):
        self.write({'state': 'cancel'})
    
    def action_done(self):
        self.write({'state': 'done'})
    
    def action_valide(self):
        self.write({'state': 'valide'})
    
    def action_draft(self):
        self.write({'state': 'draft'})
    
    def _salaire_journalier(self,contract):
        salaire_jour = 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        employee_profile = contract.pp_personnel_id_many2one.definition_nbre_jour_worked_par_mois
        if employee_profile == 'jr_mois':
            salaire_jour = contract.wage / 30
        elif employee_profile == 'nbr_saisie':
            salaire_jour = contract.wage / contract.pp_personnel_id_many2one.nbre_jour_worked_par_mois
        return salaire_jour

    @api.onchange('jr_conge')
    def _compute_jr_conge(self):
        self.jr_conge_m = self.jr_conge * self._salaire_journalier(self.contract)

    @api.onchange('jr_block')
    def _compute_jr_conge(self):
        self.jr_block_m = self.jr_block * self._salaire_journalier(self.contract)

    @api.onchange('preavis_retenu')
    def _compute_preavis_retenu(self):
        self.preavis_retenu_m = self.preavis_retenu * self._salaire_journalier(self.contract)

    @api.onchange('preavis_ajouter')
    def _compute_preavis_ajouter(self):
        self.preavis_ajouter_m = self.preavis_ajouter * self._salaire_journalier(self.contract)
    
    @api.onchange('jr_dim','nombre_dimanche_a_payer')
    def _compute_jr_dim(self):
        employee_profile = self.contract.pp_personnel_id_many2one.definition_nbre_jour_worked_par_mois
        salaire_jour = 0
        res = 0
        if employee_profile == 'jr_mois':
            salaire_jour = self.contract.wage / 30
        elif employee_profile == 'nbr_saisie':
            salaire_jour = self.contract.wage / self.contract.pp_personnel_id_many2one.nbre_jour_worked_par_mois
        
        if self.nombre_dimanche_a_payer == '1':
            res = salaire_jour * self.jr_dim
        elif self.nombre_dimanche_a_payer == '2':
            res = salaire_jour * (self.jr_dim / 2)
        elif self.nombre_dimanche_a_payer == '3':
            res = salaire_jour * (self.jr_dim / 4)
        
        self.montant_dim = res


    @api.model
    def create(self,vals):
        contract = self.env['hr.contract'].browse(vals['contract'])
        code_type = 'S' if vals['employee_type'] == 's' else 'O'
        query = """
                select count(*) from hr_stc where extract(year from date_start) = %s 
                """% (datetime.today().year)
        self.env.cr.execute(query)
        result = self.env.cr.fetchall()

        vals['name'] = 'STC'+str(result[0][0]+1).zfill(5)+'-'+code_type+'/'+str(datetime.today().month)+'/'+str(datetime.today().year)
        
        if vals.get('jr_block'):
            vals['jr_block_m'] = vals['jr_block'] * self._salaire_journalier(contract)
        if vals.get('jr_conge'):
            vals['jr_conge_m'] = vals['jr_conge'] * self._salaire_journalier(contract)
        if vals.get('preavis_retenu'):
            vals['preavis_retenu_m'] = vals['preavis_retenu'] * self._salaire_journalier(contract)
        if vals.get('preavis_ajouter'):
            vals['preavis_ajouter_m'] = vals['preavis_ajouter'] * self._salaire_journalier(contract)

        if vals.get('nombre_dimanche_a_payer'):
            if vals['nombre_dimanche_a_payer'] == '1':
                vals['montant_dim'] = self._salaire_journalier(contract) * vals['jr_dim']
            if vals['nombre_dimanche_a_payer'] == '2':
                vals['montant_dim'] = self._salaire_journalier(contract) * (vals['jr_dim'] / 2)
            if vals['nombre_dimanche_a_payer'] == '3':
                vals['montant_dim'] = self._salaire_journalier(contract) * (vals['jr_dim'] / 4)

        return super(hr_stc,self).create(vals)
    
        
    def _get_legal_bonus(self,employee_id,date_start):
        query = """
                    select sum(affich_bonus_jour) - sum(affich_jour_conge) from hr_payslip where employee_id = %s and date >= '%s';
                """   % (employee_id,date_start)
        self.env.cr.execute(query)
        return self.env.cr.fetchall()[0][0]

    def write(self,vals):
        date = fields.Date.from_string(vals['date_start']) if vals.get('date_start') else fields.Date.from_string(self.date_start)
        if vals.get('employee_type') or vals.get('date_start'):
            code_type = 'S' if vals['employee_type'] == 's' else 'O'
            
            query = """
                select count(*) from hr_stc where extract(year from date_start) = %s and id <= %s
                """% (date.year,self.id)
            self.env.cr.execute(query)
            result = self.env.cr.fetchall()

            self.name = 'STC'+str(result[0][0]).zfill(5)+'-'+code_type+'/'+str(date.month)+'/'+str(date.year)

        if vals.get('jr_conge'):
            vals['jr_conge_m'] = vals['jr_conge'] * self._salaire_journalier(self.contract)
        
        if vals.get('jr_block'):
            vals['jr_block_m'] = vals['jr_block'] * self._salaire_journalier(self.contract)

        if vals.get('preavis_retenu'):    
            vals['preavis_retenu_m'] = vals['preavis_retenu'] * self._salaire_journalier(self.contract)

        if vals.get('preavis_ajouter'):    
            vals['preavis_ajouter_m'] = vals['preavis_ajouter'] * self._salaire_journalier(self.contract)

        if vals.get('nombre_dimanche_a_payer'):
            if vals['nombre_dimanche_a_payer'] == '1':
                vals['montant_dim'] = self._salaire_journalier(self.contract) * self.jr_dim
            if vals['nombre_dimanche_a_payer'] == '2':
                vals['montant_dim'] = self._salaire_journalier(self.contract) * (self.jr_dim / 2)
            if vals['nombre_dimanche_a_payer'] == '3':
                vals['montant_dim'] = self._salaire_journalier(self.contract) * (self.jr_dim / 4)

        if vals.get('jr_dim'):
            if self.nombre_dimanche_a_payer == '1':
                vals['montant_dim'] = self._salaire_journalier(self.contract) * vals['jr_dim']
            if self.nombre_dimanche_a_payer == '2':
                vals['montant_dim'] = self._salaire_journalier(self.contract) * (vals['jr_dim'] / 2)
            if self.nombre_dimanche_a_payer == '3':
                vals['montant_dim'] = self._salaire_journalier(self.contract) * (vals['jr_dim'] / 4)    

        if 'state' in vals and vals.get('state') == 'done':
            last_day = str(calendar.monthrange(date.today().year, date.today().month)[1]) 
            # status = self.env.ref("hr_payroll_ma.holidays_status_conge0")
            date_stop = fields.Date.from_string(str(date.today().year)+'-'+str(date.today().month)+'-'+last_day)
            date_start = fields.Date.from_string(str(date.today().year)+'-'+str(date.today().month)+'-01')
            period_id = self.env["account.month.period"].search([('date_stop','<=',date_stop),('date_start','>=',date_start)],limit=1)   
            last_contrat = self.env['hr.contract'].search([('id','>',self.contract.id),('employee_id','=',self.employee_id.id)],order="id",limit=1)
            conge = self.employee_id.panier_conge
            if last_contrat:
                if not last_contrat.date_start:
                    raise ValidationError(
                        "Erreur, Contrat %s doit avoir une date de début."%(last_contrat.date_start)
                    )
                else:
                    conge -= self._get_legal_bonus(self.employee_id.id,last_contrat.date_start)
            
            for emprunt in self.emprunt_lines:        
                emprunt_line_data = {
                    'prelevement_id' : emprunt.emprunt_id.id,
                    'period_id':period_id.id,
                    'montant_a_payer' : emprunt.montant_payer,
                    'observations' : emprunt.note,
                    'stc_id' : self.id
                    }
                self.env['hr.paiement.prelevement'].create(emprunt_line_data)

            for payslip in self.payslip_lines:
                payslip.payslip_id.write({'stc_id':self.id})

            if self.jr_conge != 0:
                data_bonus = {
                    # 'holiday_status_id' :status.id ,
                    'employee_id' : self.employee_id.id,
                    'name' : u'Solde de tous compte',
                    'nbr_jour' : -conge,
                    'categorie': "stc",
                    'stc_id' : self.id
                    }
                bonus = self.env['hr.allocations'].create(data_bonus)
                bonus.write({'state':'validee'})
            self.employee_id.write({'state_employee_wtf':'stc'})

        if 'state' in vals and (vals.get('state') == 'draft' or vals.get('state') == 'cancel'):
            emprunt_echeance = self.env['hr.paiement.prelevement'].search([('stc_id','=',self.id)])
            for line in emprunt_echeance:
                line.unlink()
            
            for payslip in self.payslip_lines:
                payslip.payslip_id.write({'stc_id':False})

            for attribution_id in self.env['hr.allocations'].search([('stc_id','=',self.id)]):
                attribution_id.write({'state':'refusee'})
                attribution_id.write({'state':'draft'})
                attribution_id.unlink()

            self.employee_id.write({'state_employee_wtf':'active'})
            
        return super(hr_stc,self).write(vals)


    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(
                    "Erreur, Vous ne pouvez pas supprimer un STC validé."
                )
        return super(hr_stc,self).unlink()
    

    @api.model
    def get_nbr_dim(self):
        slip_ids = self.env['hr.payslip'].search([('employee_id','=',self.employee_id.id)])
        nb_dimch = self.env['jh.travaille.par.chantier']
        nb = 0
        for i in slip_ids:
            nb = sum([line.nb_dim for line in nb_dimch.search([('slip_id','=',i.id)])])
        return nb 
    
    @api.model
    def get_last_period_days(self):
        slip_ids = self.env['hr.payslip'].search([('employee_id','=',self.employee_id.id)],order='id desc',limit=1)
        if slip_ids:
            return slip_ids.nbr_jour_travaille

    
    @api.model
    def get_emp_bal(self):
        emprunts = self.env['hr.prelevement'].search([('employee_id','=',self.employee_id.id),('reste_a_paye','>',0),('state','=','validee')])
        res = []
        for line in emprunts:
            res.append(
                {"emprunt_id": line.id,
                 "add": True,
                 "montant_payer": line.reste_a_paye
                })
        print (res)
        return self.env["loan.list"].sudo().create(res)
    
    
    @api.model
    def get_emp_payslip(self):
        payslips = self.env['hr.payslip'].search([('employee_id','=',self.employee_id.id),('state','!=','draft'),('type_fiche','=','stc')],order="id desc")
        res = []
        for line in payslips:
            if not line.stc_id:
                res.append({'payslip_id':line.id})
        self.update({'payslip_lines': res})
        return True

    def compute_stc(self):
        res_add = res_retenu = res_emprunt = res_payslip = 0

        for line in self.emprunt_lines:
            if line.add:
                res_emprunt += line.montant_payer
            
        self.emprunt = res_emprunt

        for line in self.payslip_lines:
            res_payslip += line.net_pay
        
        self.reste_salaire = res_payslip

        res_add = self.jr_conge_m + self.jr_block_m + self.montant_dim + self.frais_depense + self.frais_route + self.preavis_ajouter_m + self.prime + self.licenciement + self.dgi + self.reste_salaire
        res_retenu = self.preavis_retenu_m + self.amande + self.retenu + self.emprunt + self.cimr

        self.montant_total = res_add - res_retenu
       
       

    @api.onchange('employee_id')
    def get_reste(self):
        if self.employee_id:
            self.jr_conge = self.employee_id.panier_conge
            self.jr_dim = self.employee_id.panier_dimanches
            self.chantier = self.employee_id.chantier_id
            # self.vehicle = self.employee_id.vehicle_id
            self.employee_type = self.employee_id.type_emp
            self.get_emp_bal()
            self.get_emp_payslip()
            self.last_period_days = self.get_last_period_days()

            contract_ids = self.env['hr.contract'].search([('employee_id','=',self.employee_id.id)]).ids

            return {'domain': {
                'contract': [('id','in',contract_ids)]
            }}
       