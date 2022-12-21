# -*- coding: utf-8 -*-
{
    'name': "Human Ressources Management",
    'summary': "The Human Ressources Management",
    'description': "Description Of Human Ressources Management",
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    'depends': [
        'base', 'mail', 'hr', 'stock', 'hr_contract', 'construction_site_management'
        ],

    'data': [         
        'views/views.xml',
        'views/templates.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/employee_model/employee_view.xml',
        'views/employee_model/employee_menu.xml',
    ],

    'demo': [
    ],

    'application': True ,
    'installable': True ,
    'auto_install': False,
    'sequence': 2,

    'assets': {
        'web.assets_backend': [
            'hr_management/static/src/css/style.css',
        ],
    },
}
