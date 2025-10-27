# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

{
    'name': 'Mensajes de Dialogo',
    'category': 'Technical Settings',
    'license': 'LGPL-3',
    'version': '18.0',
    'author': "Lajonner Crespin & Dalemberg Crespin",
    'summary': 'Nos permite invocar mensajes de dialogo',
    'description': """
    
Permite mostrar

* Mensajes de Advertencia
* Mensajes con archivos de resultado

       """,
    'website': None,
    'depends': ['base'],
    'data': [
           "wizard/message_wizard.xml",
           "wizard/file_wizard.xml",
           "security/ir.model.access.csv",
           ],
    'demo': [

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'qweb': [
    
    ],
}