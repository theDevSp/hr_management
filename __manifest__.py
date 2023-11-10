# -*- coding: utf-8 -*-
{
    'name': "Human Ressources Management",
    'summary': "The Human Ressources Management",
    'description': "Description Of Human Ressources Management",
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    'depends': [
        'base', 
        'mail', 
        'hr',  
        'hr_contract', 
        'construction_site_management', 
        'muk_web_theme', 
        'account_fiscal_year_period', 
        'base_fontawesome', 
        'reports_templates', 
        'fleet_gmao_management',
        'configuration_module'
        ],

    'data': [         
        'security/groups.xml',
        'security/rules.xml',
        'security/ir.model.access.csv',
        'wizard/wizard_blacklist_view.xml',
        'wizard/wizard_reporter_dates_view.xml',
        'wizard/wizard_confirmer_annuler_reporter_date.xml',

        'views/employee_model/employee_view.xml',
        'views/config/config_view.xml',
        'views/employee_model/directeur_view.xml',
        'views/employee_blacklist_model/blacklist_view.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/recruit_view.xml',
        'views/sequences/sequence_hr_management.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/job_view.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/contrats/contrat_histo_view.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/contrats/contrat_view.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/contrats/type_contrat_view.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/augmentation_view.xml',
        'views/employee_prime_rembourssement_model/prime_type_view.xml',
        'views/employee_prime_rembourssement_model/prime_view.xml',
        'views/employee_prime_rembourssement_model/paiement_ligne_view.xml',
        'views/employee_prelevement_model/prelevement_view.xml',
        'views/employee_prelevement_model/paiement_prelevement_view.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/profile_paie_view.xml',
        'views/employee_credit_model/credit_view.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/fixation_view.xml',
        'views/employee_holidays_model/holidays_view.xml',
        'views/employee_holidays_model/jour_ferie_view.xml',
        'views/employee_holidays_model/allocations_view.xml',
        'views/employee_stc_model/stc_view.xml',
        'views/employee_rib_model/rib_view.xml',
        'views/employee_payroll_model/fiche_paie_view.xml',
        'views/employee_payroll_model/jr_travaille_par_chantier_view.xml',
        'views/employee_pointage_mission_model/pointage_view.xml',
        # 'views/employee_pointage_mission_model/rapport_pointage_view.xml',
        'views/employee_pointage_mission_model/rapport_pointage_admin_view.xml',
        'views/employee_pointage_mission_model/transfert_view.xml',
        'views/employee_pointage_mission_model/wizards/add_new_employee_wizard.xml',
        'views/employee_pointage_mission_model/wizards/create_single_emplyee_repport.xml',
        'views/employee_pointage_mission_model/wizards/create_mass_repport.xml',
        'employee_holidays_model/validation_wizard/wizard_view.xml',
        'employee_holidays_model/mass_creation_holidays/wizard_view.xml',

        'reports/responsable_template.xml',
        'reports/employee_template.xml',
        'reports/report_demande_recrutement.xml',
        'reports/report_fiche_employee.xml',
        'reports/template_employee.xml',
        'reports/report_augmentation.xml',
        'reports/report_emprunt.xml',
        'reports/report_prime.xml',
        'reports/report_fixation.xml',
        'reports/report_holidays.xml',
        'reports/report_commande.xml',
        'reports/report_stc.xml',

        'views/employee_model/employee_menu.xml',
        'views/config/config_menu.xml',
        'views/config/responsable_menu.xml',
        'views/employee_model/directeur_menu.xml',
        'views/employee_blacklist_model/blacklist_menu.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/recruit_menu.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/job_menu.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/contrats/contrat_histo_menu.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/contrats/contrat_menu.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/contrats/type_contrat_menu.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/augmentation_menu.xml',
        'views/employee_prime_rembourssement_model/prime_type_menu.xml',
        'views/employee_prime_rembourssement_model/prime_menu.xml',
        'views/employee_prime_rembourssement_model/paiement_ligne_menu.xml',
        'views/employee_prelevement_model/prelevement_menu.xml',
        'views/employee_prelevement_model/paiement_prelevement_menu.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/profile_paie_menu.xml',
        'views/employee_credit_model/credit_menu.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/fixation_menu.xml',
        'views/employee_holidays_model/holidays_menu.xml',
        'views/employee_holidays_model/jour_ferie_menu.xml',
        'views/employee_holidays_model/allocations_menu.xml',
        'views/employee_stc_model/stc_menu.xml',
        'views/employee_rib_model/rib_menu.xml',
        'views/employee_payroll_model/fiche_paie_menu.xml',
        'views/employee_payroll_model/jr_travaille_par_chantier_menu.xml',
        'views/employee_pointage_mission_model/pointage_menu.xml',
        'views/declaration/declaration_menu.xml',
        'views/declaration/declaration_views.xml',

        'views/recap_pdf/recap_pdf_view.xml',
        'views/recap_pdf/recap_pdf_menu.xml',
        'views/recap_pdf/recap_line_pdf_view.xml',
        
        'views/dashboards/dashboards_menu.xml',

        'views/owl_views/report_pointage_views_inherit.xml',
        'views/owl_views/conges/conges_views_inherit.xml',
        'views/owl_views/stc/stc_views_inherit.xml',
        'views/owl_views/transfert/transfert_views_inherit.xml',
        'views/owl_views/fiche_de_paie/fiche_de_paie_views_inherit.xml',
        'views/owl_views/fixation/fixation_salaire_views_inherit.xml',
        'views/owl_views/employe/employe_views_inherit.xml',
        'views/owl_views/recap/recap_views_inherit.xml'
        

],

    'demo': [
    ],

    'assets': {
        'web.assets_qweb': [
            
        ],
        'web.assets_backend': [
            'hr_management/static/src/js/*.js',
            'hr_management/static/src/js/**/*.js',
            'hr_management/static/src/xml/*.xml',
            'hr_management/static/src/xml/**/*.xml',
            'hr_management/static/src/css/*.scss',
            'hr_management/static/src/css/**/*.scss'
        ],
        'web.report_assets_pdf': [
            'hr_management/static/src/report_css/*.scss',  
        ],
        'web.assets_common': [
            'hr_management/static/src/**/*.scss',  

        ],
        
    },

    'application': True ,
    'installable': True ,
    'auto_install': False,
    'sequence': 2,

}
