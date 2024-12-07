# -*- coding: utf-8 -*-
{
    'name': "Identity Card Reader : Belgium",

    'summary': """
        Create partners from Belgian identity card on Windows 
        """,

    'description': """
        Create Odoo partners (res.partners) from Belgian identity card and card reader on Windows clients.
        The middleware is using a specific BSD licence that can be found in MIDDLEWARE_LICENSE.txt
    """,

    'author': "Cyberwave",
    'website': "https://www.cyberwave.be",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '18.0.1.0.0',
    
    'price': 1000,
    'currency': 'EUR',
    'support': 'jerome.dewandre.mail@gmail.com',

    # any module necessary for this one to work correctly
    'depends': ['base','bus'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/res_users.xml',
        'views/templates.xml',
        'wizard/card_reader.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'OPL',
    'assets': {
        'web.assets_backend': [
            'be_id_reader/static/src/xml/eidConnector.xml',
            'be_id_reader/static/src/**/*',
        ],
    },
    'installable': True,
    'application': True,
    'images': ['static/description/main_screenshot.png'],
}
