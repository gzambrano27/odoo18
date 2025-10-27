# -*- coding: utf-8 -*-
{
    'name': 'Module Info API',
    'version': '18.0',
    'author': 'Gps Sistemas',
    'category': 'Tools',
    'summary': 'API to fetch configured module data',
    'description': 'Configure which module and fields to expose via REST API.',
    'depends': ['base','mail'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/module_api_config_views.xml',
    ],
    'images': [
        'static/description/logo.png',
        'static/description/icon.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
