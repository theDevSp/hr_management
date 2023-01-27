# -*- coding: utf-8 -*-
{
    'name': "Human Ressources Management",
    'summary': "The Human Ressources Management",
    'description': "Description Of Human Ressources Management",
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    'depends': [
        'base', 'mail', 'hr', 'stock', 'hr_contract', 'construction_site_management', 'muk_web_theme'
        ],

    'data': [         
        'views/views.xml',
        'views/templates.xml',
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
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/contrats/contrat_actif_view.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/contrats/type_contrat_view.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/contrats/contrat_new_view.xml',
        
        'reports/report_demande_recrutement.xml',
        'reports/paper_format/paper_format.xml',
        'reports/report/report.xml',
        
        'views/employee_model/employee_menu.xml',
        'views/config/config_menu.xml',
        'views/config/responsable_menu.xml',
        'views/employee_model/directeur_menu.xml',
        'views/employee_blacklist_model/blacklist_menu.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/recruit_menu.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/job_menu.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/contrats/contrat_histo_menu.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/contrats/contrat_actif_menu.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/contrats/type_contrat_menu.xml',
        'views/employee_contract_job_recruit_augmentation_fixation_profile_model/contrats/contrat_new_menu.xml',
    ],

    'demo': [
    ],

    'application': True ,
    'installable': True ,
    'auto_install': False,
    'sequence': 2,

    'assets': {
    },
}
