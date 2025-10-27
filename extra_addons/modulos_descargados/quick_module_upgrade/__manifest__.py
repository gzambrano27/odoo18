# -*- coding: utf-8 -*-

{
    'name': 'Quick Module Upgrade Install',
    'version': '18.0.0.0',
    'summary': 'Easy and Quickly Update your module,update module,upgrade module,easily upgrade module,module to upgrade,update,upgrade,Easy and Quickly install your module,install module,install module,easily install module,module to install,install,install',
    'license': 'LGPL-3',
    'support': 'info@reliution.com',
    'author': 'Reliution',
    'category': 'hidden',
    'description': "Easy and Quickly Update your module,update module,upgrade module,easily upgrade module,module to upgrade,update,upgrade,Easy and Quickly install your module,install module,install module,easily install module,module to install,install,install"

                   "",
    'website': 'https://www.reliution.com/',
    'images': ["static/description/banner.gif"],
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/quick_models_upgrade_popup_view.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
