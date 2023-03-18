from odoo import fields, models, api
from odoo.exceptions import ValidationError

class recruit(models.Model):
    _name = "hr.recrutement"
    _description = "Recrutement"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    READONLY_STATES = {
        'draft': [('readonly', False)],
        'validee': [('readonly', True)],
        'encours': [('readonly', True)],
        'acceptee': [('readonly', True)],
        'refusee': [('readonly', True)],
        'annulee': [('readonly', True)],
        'terminee': [('readonly', True)]
    }

    READONLY_STATES_NBR_EFF_ACCEPTE = {
        'draft': [('readonly', True)],  
        'validee': [('readonly', False)],
        'encours': [('readonly', False)],
        'acceptee': [('readonly', False)],
        'refusee': [('readonly', False)],
        'annulee': [('readonly', False)],
        'terminee': [('readonly', False)]
    }

    name = fields.Char('Référence', readonly=True, required=True, copy=False, default='New')
    chantier_id  = fields.Many2one("fleet.vehicle.chantier",u"Chantier", states = READONLY_STATES, required=True)
    responsable_id = fields.Many2one("hr.responsable.chantier","Responsable", states = READONLY_STATES)
    title_poste = fields.Many2one("hr.job","Titre du poste", states = READONLY_STATES)
    observation = fields.Text("Observation", states = READONLY_STATES)
    nbr_effectif_demande = fields.Integer("Nombre d'effectif demandé", states = READONLY_STATES)
   
    nbr_effectif_accepte = fields.Integer("Nombre d'effectif accepté", states = READONLY_STATES_NBR_EFF_ACCEPTE)
    compute_readonly_eff_accepte = fields.Boolean(string="check field", compute='get_user')

    state  = fields.Selection([
        ("draft","Brouillon"),
        ("validee","Validée"),
        ("encours","En cours de traitement"),
        ("acceptee","Acceptée"),
        ("refusee","Refusée"),
        ("annulee","Annulée"),
        ("terminee","Terminée")
        ],"Status", 
        default="draft",
    )

    motif_recrut = fields.Selection([
        ("remplacement","Remplacement d'un salarié sortant"),
        ("raison_chantier","Pour des besoins de chantier"),
        ("autre_raison","Autres motifs"),
        ],"Motif de recrutement",
        states = READONLY_STATES,
    )
    motif_raison_nom_prenom = fields.Char("Nom et prénom",states = READONLY_STATES)
    motif_raison_fonction = fields.Char("Fonction",states = READONLY_STATES)
    motif_raison_code_machine = fields.Char("Code Machine",states = READONLY_STATES)
    motif_raison = fields.Text("Plus de détails",states = READONLY_STATES)
    equipe_id = fields.Many2one("fleet.vehicle.chantier.emplacement",u"Équipe")
    
    _sql_constraints = [
		('name_uniq', 'UNIQUE(name)', 'Cette référence est déjà utilisée.'),
	]

    @api.onchange("nbr_effectif_demande")
    def onchange_nbr_effectif_demande(self):
        self.nbr_effectif_accepte = self.nbr_effectif_demande


    @api.depends('compute_readonly_eff_accepte')
    def get_user(self):
        self.compute_readonly_eff_accepte = self.user_has_groups('hr_management.group_pointeur')


    @api.constrains('nbr_effectif_demande')
    def _check_nbr_effectif_demande(self):
        if self.nbr_effectif_demande <= 0:
            raise ValidationError("Le nombre d'effectif doit être supérieur de la valeur 0.")

    @api.constrains('nbr_effectif_accepte')
    def _check_nbr_effectif_accepte(self):
        if self.nbr_effectif_accepte < 0:
            raise ValidationError("Le nombre d'effectif doit être supérieur ou égal à la valeur 0.")

    @api.model
    def create(self, vals):
        identifiant_chantier = self.env['fleet.vehicle.chantier'].browse(vals.get('chantier_id')).id
        reference_demande = self.recuperer_reference(identifiant_chantier)
        code_chantier = self.env['fleet.vehicle.chantier'].browse(vals.get('chantier_id')).code
        vals['name'] = str(code_chantier) + '/RECRUT' + str(reference_demande)
        return super(recruit, self).create(vals)

    def write(self, vals):
        if(vals.get("chantier_id")):
            identifiant_chantier = self.env['fleet.vehicle.chantier'].browse(vals.get('chantier_id')).id
            reference_demande = self.recuperer_reference(identifiant_chantier)
            code_chantier = self.env['fleet.vehicle.chantier'].browse(vals.get('chantier_id')).code
            vals['name'] = str(code_chantier) + '/RECRUT' + str(reference_demande)
        return super(recruit, self).write(vals)

    def recuperer_reference(self,identifiant_chantier):
        query = """
                SELECT name FROM hr_recrutement
                WHERE chantier_id = %s
                ORDER BY name DESC
                LIMIT 1;
            """ % (identifiant_chantier)
        self.env.cr.execute(query)
        res = self.env.cr.fetchall()
        if len(res) > 0:
            chaine = res[0][0]
            debut_word = chaine.find('RECRUT')
            debut_chiffre = debut_word + 6
            chiffre = int(chaine[debut_chiffre:])
            reference_demande = chiffre + 1
        else:
            reference_demande = 1
        return reference_demande

    def calculer_nbr_existant(self):
        for rec in self:
            query = """
                    SELECT COUNT(*)
                    FROM hr_employee
                    WHERE chantier_id = %s AND job_id = %s
                """ % (rec.chantier_id.id, rec.title_poste.id)
            rec.env.cr.execute(query)
            res = rec.env.cr.fetchall()
            if len(res) > 0 :
                return res[0][0]
        return 0


    def to_draft(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft', 'encours', 'acceptee', 'refusee', 'terminee'} :
                self.state = 'draft'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        elif self.user_has_groups('hr_management.group_pointeur'):
            if self.state in {'validee'} :
                self.state = 'draft'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Seulement les administrateurs, les agents de paie et les pointeurs qui peuvent changer le status.")


    def to_validee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'validee', 'encours', 'acceptee', 'refusee', 'annulee', 'terminee'} :
                self.state = 'validee'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        elif self.user_has_groups('hr_management.group_pointeur'):
            if self.state in {'draft'} :
                self.state = 'validee'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Seulement les administrateurs, les agents de paie et les pointeurs qui peuvent changer le status.")


    def to_encours(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft', 'encours', 'acceptee', 'refusee', 'annulee', 'terminee'} :
                self.state = 'encours'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Seulement les administrateurs, les agents de paie qui peuvent changer ce status.")
        

    def to_acceptee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft', 'validee', 'acceptee', 'refusee', 'annulee', 'terminee'} :
                self.state = 'acceptee'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Seulement les administrateurs, les agents de paie qui peuvent changer ce status.")
        
    
    def to_refusee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft', 'validee', 'acceptee', 'refusee', 'annulee', 'terminee'} :
                self.state = 'refusee'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Seulement les administrateurs, les agents de paie qui peuvent changer ce status.")
        
    
    def to_annulee(self):
        if self.user_has_groups('hr_management.group_admin_paie'):
            self.state = 'annulee'
        elif self.user_has_groups('hr_management.group_agent_paie') and self.state in {'validee', 'encours', 'acceptee'} :
            self.state = 'annulee'
        elif self.user_has_groups('hr_management.group_pointeur') and self.state in {'draft', 'validee'} :
            self.state = 'annulee'
        else:
            raise ValidationError("Erreur, Cette action n'est pas autorisée.")

    def to_terminee(self):
        if self.user_has_groups('hr_management.group_admin_paie') or self.user_has_groups('hr_management.group_agent_paie') :
            if self.state not in {'draft', 'validee', 'encours', 'refusee', 'annulee', 'terminee'} :
                self.state = 'terminee'
            else:
                raise ValidationError("Erreur, Cette action n'est pas autorisée.")
        else:
            raise ValidationError("Erreur, Seulement les administrateurs, les agents de paie qui peuvent changer ce status.")  
        


    #@api.multi
    def action_pointeur_user(self,employee_type,etat):

        pointeur = self.env['res.users'].has_group("hr_management.group_pointeur")
        view = self.env.ref('hr_management.recrutement_tree_pointeur') if pointeur else self.env.ref('hr_management.recrutement_tree')
        form = self.env.ref('hr_management.recrutement_form_pointeur') if pointeur else self.env.ref('hr_management.recrutement_view_form')
        res=[]
        where = ''
        #if etat:
        #    where += 'etat = '+str(etat)
        #else:
        #    where +='(etat = 5 or etat is null or etat = 9)'
        
        #dest = 'Salariés' if type_emp == 's' else 'Ouvriers'

        query = ""

        if pointeur:
            query = """
                    select id from hr_rapport_pointage where chantier_id in (select chantier_id from chantier_responsable_relation where user_id = %s) and %s;
                """   % (self.env.user.id,where)
        else:
            query = """
                    select id from hr_rapport_pointage where %s;
                """   % (where)
        self.env.cr.execute(query)
        for result in self.env.cr.fetchall():
            res.append(result[0])
        
        context = {
                "search_default_group_by_public_market_id":1,
                "search_default_group_by_period_id":1,
                "search_default_group_by_emplacement_chantier_id":1
            }
        #if employee_type == 'employee2':
        #    context['search_default_group_by_quinzaine'] = 1
        
        return {
            'name':'Demandes de recrutement',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form,search',
            'res_model': self._name,
            'views': [(view.id, 'tree'),(form.id, 'form')],
            #'view_id': view.id,
            'target': 'current',
            'domain':[('id','in',res)],
            'context':context
        }
    
    @api.onchange("motif_recrut")
    def onchange_motif_recrut_vider_champs(self):
        self.motif_raison_nom_prenom = ""
        self.motif_raison_fonction = ""
        self.motif_raison_code_machine = ""
        self.motif_raison = ""

