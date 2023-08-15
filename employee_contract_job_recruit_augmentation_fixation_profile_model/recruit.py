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

    def _get_engin_domain(self):
        
        res = []

        query = """
                select distinct(vehicle_id) from fleet_vehicle_chantier_affectation fvca inner join fleet_vehicle fv on fv.id = fvca.vehicle_id where fv.active = true;
            """  
        self.env.cr.execute(query)
        for result in self.env.cr.fetchall():
            res.append(result[0])
                
        return [('id', 'in',res)]

    name = fields.Char('Référence', readonly=True, copy=False)
    chantier_id  = fields.Many2one("fleet.vehicle.chantier",u"Chantier",domain=_get_chantier_domain, states = READONLY_STATES, required=True)
    responsable_id = fields.Many2one("hr.responsable.chantier","Responsable", states = READONLY_STATES, required=True)
    title_poste = fields.Many2one("hr.job","Titre du poste", states = READONLY_STATES, required=True)
    observation = fields.Text("Observation", states = READONLY_STATES)
    nbr_effectif_demande = fields.Integer("Nombre demandé", states = READONLY_STATES, required=True)
    nbr_effectif_accepte = fields.Integer("Nombre accepté", states = READONLY_STATES_NBR_EFF_ACCEPTE)
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
    motif_raison_code_machine = fields.Many2one("fleet.vehicle",u'Code Engin',domain=_get_engin_domain,states = READONLY_STATES)
    motif_raison = fields.Text("Plus de détails",states = READONLY_STATES)
    equipe_id = fields.Many2one("fleet.vehicle.chantier.emplacement",u"Équipe",states = READONLY_STATES)
    
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
            raise ValidationError("Erreur, Seulement les administrateurs, les agents de paie et les pointeurs qui peuvent changer le statut.")


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
            raise ValidationError("Erreur, Seulement les administrateurs, les agents de paie et les pointeurs qui peuvent changer le statut.")


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
        
        
    @api.onchange("motif_recrut")
    def onchange_motif_recrut_vider_champs(self):
        self.motif_raison_nom_prenom = ""
        self.motif_raison_fonction = ""
        self.motif_raison_code_machine = ""
        self.motif_raison = ""

