# -*- coding: utf-8 -*-
{
    'name': "Human Ressources Management",
    'summary': "The Human Ressources Management",
    'description': "Description Of Human Ressources Management",
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    'depends': [
        'base', 'mail', 'hr', 'stock', 'hr_contract', 'construction_site_management', 'muk_web_theme', 'account_fiscal_year_period', 'base_fontawesome'
        ],

    'data': [         
        
        'security/groups.xml',
        'security/ir.model.access.csv',
        'wizard/wizard_blacklist_view.xml',

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
        'views/employee_prime_rembourssement_model/paiement_prime_view.xml',
        #'views/employee_prelevement_model/prelevement_view.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/profile_paie_view.xml',

        'reports/report_demande_recrutement.xml',
        
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
        'views/employee_prime_rembourssement_model/paiement_prime_menu.xml',
        #'views/employee_prelevement_model/prelevement_menu.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/profile_paie_menu.xml',
    ],

    'demo': [
    ],

    'assets': {
        'web.assets_qweb': [
            
        ],
        'web.assets_backend': [

            

        ],
        
    },

    'application': True ,
    'installable': True ,
    'auto_install': False,
    'sequence': 2,

}
