# -*- coding: utf-8 -*-
{
    'name': "Human Ressources Management",
    'summary': "The Human Ressources Management",
    'description': "Description Of Human Ressources Management",
    #'author': "My Company",
    #'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    "license": 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'hr'],

    # always loaded
    'data': [         
        'views/views.xml',
        'views/templates.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/employee_model/employee_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],

    'application': True ,
    'installable': True ,
    'auto_install': False,
    'sequence': 2,
    
}