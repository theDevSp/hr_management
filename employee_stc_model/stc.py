# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import date
import calendar


class hr_stc(models.Model):
    _name = "hr.stc"
    _description = "STC"
    _inherit = ['mail.thread','mail.activity.mixin']

    READONLY_STATES = {
        'cancel': [('readonly', True)],
        'valide': [('readonly', True)],
        'done': [('readonly', True)]
    }

    READONLY_STATES_VALID_SALARY = {
        'cancel': [('readonly', True)],
        'done': [('readonly', True)]
    }

    def _count_by_year(self):
        for employee in self:
            query = """
                    select count(*) from hr_stc where job_id = %s and extract(year from date_start) = %s and id <= %s
                    """% (employee.job_id.id,fields.Date.from_string(employee.date_start).year,employee.id)
            self.env.cr.execute(query)
            result = self.env.cr.fetchall()
            employee.count_by_year = str(result[0][0])+'/'+str(fields.Date.from_string(employee.date_start).year)
        return

    name = fields.Char(u"Référence" ,readonly=True, default="######")
    employee_id = fields.Many2one("hr.employee",u"Employée",required=True,readonly=False, states=READONLY_STATES)
    job_id = fields.Many2one('hr.job',string="Titre du Poste",readonly=False, states=READONLY_STATES)
    cin = fields.Char(related='employee_id.cin',string='N° CIN' ,readonly=True)
    job = fields.Char(u'FONCTION', states=READONLY_STATES)
    date_debut = fields.Date(related='contract.date_start',string="Date de début" ,readonly=True)
    date_fin = fields.Date(related='contract.date_end',string="Date de fin" ,readonly=False, states=READONLY_STATES)
    chantier = fields.Many2one('fleet.vehicle.chantier',string="Dernier Chantier" , states=READONLY_STATES)
    chantier_id = fields.Many2one('fleet.vehicle.chantier',string="Dernier Chantier" , states=READONLY_STATES)
    vehicle = fields.Many2one('fleet.vehicle',string="Dernier Engin",readonly=False, states=READONLY_STATES)
    bank = fields.Many2one(related='employee_id.rib_number',string='N° RIB' ,readonly=True)
    date_start = fields.Date(u"Date du STC", default=datetime.today(),readonly=False, states=READONLY_STATES)
    modePay = fields.Selection([('mode1',u'Mise à disposition'),('mode2',u"Virement Postal"),('mode3',u"Virement Bancaire"),('mode4',u"Espèce")],u"Mode de paiement",readonly=False, states=READONLY_STATES)
    contract = fields.Many2one('hr.contract' ,string="Contrat", required=True, domain="[('employee_id', '=', employee_id)]",readonly=False, states=READONLY_STATES)

    motif = fields.Text(u"Motif",readonly=False, states=READONLY_STATES)
    motifs = fields.Char(u"Motif",readonly=False, states=READONLY_STATES)
    note = fields.Text(u"Observation",readonly=False, states=READONLY_STATES)
    notes = fields.Html('Notes')
    
    montant_total = fields.Float(u"Montant total",readonly=True)
    currency_id = fields.Many2one('res.currency', string = 'Symbole Monétaire')
    salaire = fields.Float(related="contract.salaire_actuel",string="Salaire de base" ,readonly=True)
    salaire_jour = fields.Float(string="Salaire de jour" ,readonly=True,compute="_compute_salaire_jr")
    type_salaire = fields.Selection(related="contract.type_salaire",readonly=True)
    
    nombre_dimanche_a_payer = fields.Selection([
            ('1',u'Tous les jours'),
            ('2',u"50 %"),
            ('3',u"25 %")
        ],u"Nbrs dimanches à calculer",default='1', states=READONLY_STATES,tracking=True)
    
    montant_dim = fields.Float(u"Montant des dimanches",readonly=True,compute="_compute_jr_dim")
    jr_dim = fields.Float(u"Nombre des dimanches", states=READONLY_STATES,tracking=True)

    prime = fields.Float(u"Prime", states=READONLY_STATES,tracking=True)
    licenciement = fields.Float(u"Licenciement", states=READONLY_STATES,tracking=True)
    dgi = fields.Float(u"Dommage et intérêts", states=READONLY_STATES,tracking=True)
    amande = fields.Float(u"Amende", states=READONLY_STATES,tracking=True)
    retenu = fields.Float(u"Prélèvement", states=READONLY_STATES,tracking=True)

    sum_salaire= fields.Float(u"Reste Salaire",readonly=True,compute="_get_sum_salaire")
    sum_prime= fields.Float(u"Reste Prime",readonly=True,compute="_get_sum_prime")
    sum_prelevement = fields.Float(u"Reste Prélevement",readonly=True,compute="_get_sum_prelevement")
    addition_lines = fields.One2many("addition.list", 'stc_id',string='Liste des primes', states=READONLY_STATES)
    deduction_lines = fields.One2many("deduction.list", 'stc_id',string='Liste des prélévement', states=READONLY_STATES)

    reste_salaire = fields.Float(u"Reste du salaire",readonly=True)
    valide_salaire = fields.Float(u"Montant Validé", states=READONLY_STATES_VALID_SALARY,tracking=True)
    payslip_lines = fields.One2many("hr.payslip.stc", 'stc_id',string='Fiche Paie', states=READONLY_STATES)

    jr_conge = fields.Float(u"Panier Congés", states=READONLY_STATES,tracking=True)
    jr_conge_m = fields.Float(u"Montant Congés",readonly=True,compute="_compute_jr_conge")

    jr_block = fields.Float(u"Jours Restants", states=READONLY_STATES,tracking=True)
    jr_block_m = fields.Float(u"Montant Restants",readonly=True)

    last_period_days = fields.Float(u"La dernière période (nbr Jours)" ,readonly=True)
    preavis_retenu = fields.Float(u"Préavis à retenir (Jours)", states=READONLY_STATES,tracking=True)
    preavis_ajouter = fields.Float(u"Préavis à ajouter (Jours)", states=READONLY_STATES,tracking=True)
    preavis_retenu_m = fields.Float(u"Montant",readonly=True,compute="_compute_preavis_retenu")
    preavis_ajouter_m = fields.Float(u"Montant",readonly=True,compute="_compute_preavis_ajouter")
    frais_depense = fields.Float(u"Frais de dépense", states=READONLY_STATES,tracking=True)
    frais_route = fields.Float(u"Frais de route", states=READONLY_STATES,tracking=True)
    cimr = fields.Float(u"Cotisation CIMR", states=READONLY_STATES,tracking=True)
    profile_paie  = fields.Many2one(related="employee_id.contract_id.pp_personnel_id_many2one",string='Profile de paie',readonly=True)
    employee_type = fields.Selection(related="contract.type_emp",store=True)
    
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
        self.contract.to_cancelled()
    
    def action_done(self):
        self.write({'state': 'done'})
        self.contract.to_expired()
    
    def action_valide(self):
        self.write({'state': 'valide'})
    
    def action_draft(self):
        self.write({'state': 'draft'})
        self.contract.to_running()
        self.write({
            'date_fin':False
        })

    @api.depends('contract')
    def _compute_salaire_jr(self):
        self.salaire_jour  = self._salaire_journalier()
    
    def _salaire_journalier(self):
        salaire_jour = 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        employee_profile = self.contract.pp_personnel_id_many2one.definition_nbre_jour_worked_par_mois
        if employee_profile == 'jr_mois' and self.contract.type_salaire == 'm':
            salaire_jour = self.contract.salaire_actuel / 30
        elif employee_profile == 'nbr_saisie' and self.contract.type_salaire == 'm':
            salaire_jour = self.contract.salaire_actuel / self.contract.pp_personnel_id_many2one.nbre_jour_worked_par_mois
        elif self.contract.type_salaire == 'h':
            salaire_jour = self.contract.salaire_actuel * self.contract.nbre_heure_worked_par_jour_related
        elif self.contract.type_salaire == 'j':
            salaire_jour = self.contract.salaire_actuel
        return salaire_jour

    @api.depends('contract','jr_block')
    def _compute_jr_block(self):
        self.jr_block_m = self.jr_block * self._salaire_journalier()

    @api.depends('contract','jr_conge')
    def _compute_jr_conge(self):
        self.jr_conge_m = self.jr_conge * self._salaire_journalier()

    @api.depends('contract','preavis_retenu')
    def _compute_preavis_retenu(self):
        self.preavis_retenu_m = self.preavis_retenu * self._salaire_journalier()

    @api.depends('contract','preavis_ajouter')
    def _compute_preavis_ajouter(self):
        self.preavis_ajouter_m = self.preavis_ajouter * self._salaire_journalier()
        
    @api.depends('jr_dim','nombre_dimanche_a_payer')
    def _compute_jr_dim(self):
        salaire_jour = self._salaire_journalier()
        res = 0
        
        if self.nombre_dimanche_a_payer == '1':
            res = salaire_jour * self.jr_dim
        elif self.nombre_dimanche_a_payer == '2':
            res = salaire_jour * (self.jr_dim / 2)
        elif self.nombre_dimanche_a_payer == '3':
            res = salaire_jour * (self.jr_dim / 4)
        
        self.montant_dim = res

    @api.depends('payslip_lines')
    def _get_sum_salaire(self):
        self.sum_salaire = sum(line.net_pay for line in self.payslip_lines if line.add)  if len(self.payslip_lines) > 0 else 0

    @api.depends('addition_lines')
    def _get_sum_prime(self):
        self.sum_prime = sum(line.montant_payer for line in self.addition_lines if line.add) if len(self.addition_lines) > 0 else 0

    @api.depends('deduction_lines')
    def _get_sum_prelevement(self):
        self.sum_prelevement = sum(line.montant_payer for line in self.deduction_lines if line.add) if len(self.deduction_lines) > 0 else 0


    @api.model
    def create(self,vals):
        contract = self.env['hr.contract'].browse(vals['contract'])
        code_type = 'S' if contract.type_emp == 's' else 'O'
        
        if not contract.pp_personnel_id_many2one:
            raise ValidationError(
                    "Erreur, Cet employé doit avoir un profil de paie."
                )
        
        query = """
                select count(*) from hr_stc where extract(year from date_start) = %s 
                """% (datetime.today().year)
        self.env.cr.execute(query)
        result = self.env.cr.fetchall()

        vals['name'] = 'STC'+str(result[0][0]+1).zfill(5)+'-'+code_type+'/'+str(datetime.today().month)+'/'+str(datetime.today().year)


        return super(hr_stc,self).create(vals)



    def write(self,vals):
        date = fields.Date.from_string(vals['date_start']) if vals.get('date_start') else fields.Date.from_string(self.date_start)
        allocation_object = self.env['hr.allocations']
        current_period = self.env['account.month.period'].get_period_from_date(self.date_start)

        if vals.get('employee_type') or vals.get('date_start') or vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(vals['employee_id'])
            code_type = 'S' if employee.type_emp == 's' else 'O'
            
            query = """
                select count(*) from hr_stc where extract(year from date_start) = %s and id <= %s
                """% (date.year,self.id)
            self.env.cr.execute(query)
            result = self.env.cr.fetchall()
            
            new_code = 'STC'+str(result[0][0]).zfill(5)+'-'+code_type+'/'+str(date.month)+'/'+str(date.year)
            self.name = new_code



        if 'state' in vals and vals.get('state') == 'done':
            
            # panier bonus
            conge = self.get_valide_panier(self.employee_id,self.date_debut,self.date_fin,self.date_start) 
            # panier dimanche
            conge_dimanche = self.get_valide_panier(self.employee_id,self.date_debut,self.date_fin,self.date_start,True)

            for addition in self.addition_lines:        
                addition.prime_id.write({
                    'state':'cloture_paye'
                })
                for line in addition.prime_id.paiement_prime_ids.filtered(lambda ln: ln.state == 'non_paye'):  
                    line.write({
                        'state':'annule', 
                        'observations':'Régelement de payement STC N° %s'%(self.name),
                        'stc_id' : self.id
                    })

                reglement_line = {
                    'prime_id' : addition.prime_id.id,
                    'period_id':current_period.id,
                    'montant_a_payer' : addition.montant_payer,
                    'observations' : addition.note or '' + ' '+ 'Régelement de payement STC N° %s'%(self.name),
                    'stc_id' : self.id
                }
                self.env['hr.paiement.ligne'].create(reglement_line).write({
                    'state':'paye'
                })
            
            for deduction in self.deduction_lines:        
                deduction.prelevement_id.write({
                    'state':'cloture_paye'
                })
                for line in deduction.prelevement_id.paiement_prelevement_ids.filtered(lambda ln: ln.state == 'non_paye'):  
                    line.write({
                        'state':'annule', 
                        'observations':'Régelement de payement STC N° %s'%(self.name),
                        'stc_id' : self.id
                    })
                reglement_line = {
                    'prelevement_id' : deduction.prelevement_id.id,
                    'period_id':current_period.id,
                    'montant_a_payer' : deduction.montant_payer,
                    'observations' : deduction.note or '' + ' '+ 'Régelement de payement STC N° %s'%(self.name),
                    'stc_id' : self.id
                    }
                self.env['hr.paiement.prelevement'].create(reglement_line).write({
                    'state':'paye'
                })

            for payslip in self.payslip_lines:
                payslip.payslip_id.to_done()
                payslip.payslip_id.write({
                    'notes':'Régelement de payement STC N° %s'%(self.name),
                    'stc_id':self.id
                    })
            """
            if self.jr_conge != 0:
                data_bonus = {
                    'employee_id' : self.employee_id.id,
                    'name' : u'Solde de tous compte',
                    'nbr_jour' : -conge,
                    'categorie': "stc",
                    
                    }
                bonus = allocation_object.create(data_bonus)
                bonus.write({'state':'validee'})
            self.employee_id.write({'state_employee_wtf':'stc'})
            """
        if 'state' in vals and (vals.get('state') == 'draft' or vals.get('state') == 'cancel'):

            for addition in self.addition_lines:        
                addition.prime_id.write({
                    'state':'validee'
                })
                for line in addition.prime_id.paiement_prime_ids.filtered(lambda ln: ln.state == 'annule'):  
                    line.write({
                        'state':'non_paye', 
                        'observations':'',
                        'stc_id' : False
                    })
                addition.prime_id.paiement_prime_ids[len(addition.prime_id.paiement_prime_ids) - 1].write({
                        'state':'non_paye'
                    })
                addition.prime_id.paiement_prime_ids[len(addition.prime_id.paiement_prime_ids) - 1].unlink()
            
            for deduction in self.deduction_lines:        
                deduction.prelevement_id.write({
                    'state':'validee'
                })
                for line in deduction.prelevement_id.paiement_prelevement_ids.filtered(lambda ln: ln.state == 'annule'):  
                    line.write({
                        'state':'non_paye', 
                        'observations':'',
                        'stc_id' : False
                    })
                deduction.prelevement_id.paiement_prelevement_ids[len(deduction.prelevement_id.paiement_prelevement_ids) - 1].write({
                        'state':'non_paye'
                    })
                deduction.prelevement_id.paiement_prelevement_ids[len(deduction.prelevement_id.paiement_prelevement_ids) - 1].unlink()

            for payslip in self.payslip_lines:
                payslip.payslip_id.unblock()
                payslip.payslip_id.write({
                    'stc_id':False
                    })
            """
            for attribution_id in self.env['hr.allocations'].search([('stc_id','=',self.id)]):
                attribution_id.write({'state':'refusee'})
                attribution_id.write({'state':'draft'})
                attribution_id.unlink()
            """
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

    
    
    def get_employee_additions(self):
        additions = self.env['hr.prime'].search([('employee_id','=',self.employee_id.id),('reste_a_paye','>',0),('state','=','validee')])
        addition_lines = [(5,0,0)]
        for line in additions:
            if line.type_prime.type_payement != "z" and line.type_prime.type_addition == "indiv":
                vals = {
                    "prime_id": line.id,
                    "montant_payer":line.reste_a_paye
                    }
                addition_lines.append((0,0,vals))
        self.addition_lines = addition_lines

    
    def get_employee_deductions(self):
        deductions = self.env['hr.prelevement'].search([('employee_id','=',self.employee_id.id),('reste_a_paye','>',0),('state','=','validee')])
        deduction_lines = [(5,0,0)]
        for line in deductions:
            vals ={
                "prelevement_id": line.id,
                "montant_payer":line.reste_a_paye
                }
            deduction_lines.append((0,0,vals))
        self.deduction_lines = deduction_lines
    
    
    def get_employee_payslip(self):
        payslips = self.env['hr.payslip'].search([('employee_id','=',self.employee_id.id),('state','in',('cal','done','approuved')),('type_fiche','=','stc')],order="id desc")
        payslip_lines = [(5,0,0)]
        for line in payslips:
            if not line.stc_id:
                vals = {
                    'payslip_id':line.id
                    }
                payslip_lines.append((0,0,vals))
        self.payslip_lines = payslip_lines
        

    def compute_stc(self):

        res_add = self.jr_conge_m + self.jr_block_m + self.montant_dim + self.frais_depense + self.frais_route + self.preavis_ajouter_m + self.prime + self.licenciement + self.dgi + self.reste_salaire
        res_add += self.sum_salaire + self.sum_prime
        res_retenu = self.preavis_retenu_m + self.amande + self.retenu + self.cimr + self.sum_prelevement

        self.montant_total = res_add - res_retenu
        self.valide_salaire = self.montant_total


    @api.onchange('employee_id')
    def get_reste_on_changed_employee(self):
        for rec in self:
            if rec.employee_id:
                rec.reset()
    
    @api.onchange('contract')
    def get_reste_on_changed_contract(self):
        for rec in self:
            if rec.contract:
                rec.reset_contract()


    def reset(self):
        for rec in self:
            if rec.employee_id:
                rec.contract = rec.employee_id.contract_id
                rec.job_id = rec.contract.job_id
                rec.jr_conge = rec.get_valide_panier(rec.employee_id,rec.date_debut,rec.date_fin,rec.date_start)
                rec.jr_dim = rec.get_valide_panier(rec.employee_id,rec.date_debut,rec.date_fin,rec.date_start,True)
                rec.chantier = rec.employee_id.chantier_id
                rec.get_employee_additions()
                rec.get_employee_deductions()
                rec.get_employee_payslip()
                rec.last_period_days = rec.get_last_period_days()
    
    def reset_contract(self):
        for rec in self:
            rec.job_id = rec.contract.job_id
            rec.jr_conge = rec.get_valide_panier(rec.employee_id,rec.date_debut,rec.date_fin,rec.date_start)
            rec.jr_dim = rec.get_valide_panier(rec.employee_id,rec.date_debut,rec.date_fin,rec.date_start,True)
            rec.chantier = rec.employee_id.chantier_id
            rec.get_employee_additions()
            rec.get_employee_deductions()
            rec.get_employee_payslip()
            rec.last_period_days = rec.get_last_period_days()
    
    def get_valide_panier(self,employee_id,date_debut,date_fin,date,is_dimanche=False):
        allocation_object = self.env['hr.allocations']
        current_period = self.env['account.month.period'].get_period_from_date(date) if not date_fin else self.env['account.month.period'].get_period_from_date(date_fin)
        contract_start_period = self.env['account.month.period'].get_period_from_date(date_debut)
        return allocation_object.get_sum_allocation(employee_id,current_period,contract_start_period,is_dimanche)

    @api.onchange("employee_id")
    def _verification_profil(self):
        for rec in self:
            profile = rec.employee_id.pp_personnel_id_many2one
            if not profile and rec.employee_id:
                raise ValidationError(
                        "Erreur, Cet employé doit avoir un profil de paie."
                    )
            rec.contract=False

