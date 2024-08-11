# -*- coding: utf-8 -*-
{
    'name': "be_id_reader",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Cyberwave",
    'website': "https://www.cyberwave.be",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

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
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'be_id_reader/static/src/xml/eidConnector.xml',
            'be_id_reader/static/src/**/*',
        ],
    },
    'installable': True,
    'application': True,
}
