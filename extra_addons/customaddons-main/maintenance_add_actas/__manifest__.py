{
    'name': 'Maintenance Add Actas',
    'version': '1.0',
    'summary': 'Extensión del módulo de mantenimiento para agregar actas',
    'author': 'Guillermo Zambrano',
    'depends': ['maintenance','portal','hr'],
    'data': [
        'data/data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/report.xml',                   # 👈 primero reportes
        'report/report_equipment_entrega.xml',
        'report/report_equipment_recepcion.xml',
        'views/maintenance_equipment_view.xml',
        'views/maintenance_actas_views.xml',   # 👈 ahora ya existen los reportes
        'views/menu_item_views.xml',
        'views/hr_employee.xml',
    ],
    'installable': True,
    'application': False,
}
