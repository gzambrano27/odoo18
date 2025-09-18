# -*- coding: utf-8 -*-
# Part of Wicoders Solutions. See LICENSE file for full copyright and licensing details

{
    'name': 'ChatGPT Integration in Odoo Discuss',
    'version': '18.0.1.1.0',
    'license': 'AGPL-3',
    'summary': 'ChatGPT Integration in Odoo Discuss',
    'description': 'Enhance your team communication in Odoo by integrating ChatGPT directly into the Discuss app.With this module, users can interact with ChatGPT inside their chat channels or private messages, making collaboration smarter and faster.',
    'author': 'Wicoders Solutions',
    'website': 'https://wicoders.com/',
    'depends': ['base', 'base_setup', 'mail'],
    'data': [
        'data/user_partner_data.xml',
        'views/res_config_settings_views.xml',
    ],
    'external_dependencies': {'python': ['openai']},
    'assets': {
        'web.assets_backend': [
            'wc_chatgpt_integration/static/src/js/action_container.js',
        ],
    },

    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
