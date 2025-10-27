{
	'name': 'Excel Odoo Connector',
	'version': '2.0.0',
	'category': 'Extra Tools',
	'author': 'XFanis (adapted for Odoo 18 by GPS Group)',
	'license': 'LGPL-3',
	'depends': ['web'],
	'data': [
		'security/security.xml',
		'security/ir.model.access.csv',
		'views/odc_template.xml',
	],
	'assets': {
		'web.assets_backend': [
			'xf_excel_odoo_connector/static/src/js/odc_template_list_controller.js',
			'xf_excel_odoo_connector/static/src/xml/odc_template_button.xml',
		],
	},
	'installable': True,
	'application': True,
}
