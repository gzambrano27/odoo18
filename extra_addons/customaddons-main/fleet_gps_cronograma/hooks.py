from odoo import api, fields, SUPERUSER_ID
from datetime import datetime, timedelta


def post_init_hook(cr, registry):
	"""Crea o actualiza el cron automáticamente al instalar el módulo (compatible con Odoo 18)."""
	env = api.Environment(cr, SUPERUSER_ID, {})

	# Buscar el modelo fleet.cronograma
	model = env['ir.model'].search([('model', '=', 'fleet.cronograma')], limit=1)
	if not model:
		return

	# Buscar si ya existe el cron
	cron = env['ir.cron'].search([
		('model_id', '=', model.id),
		('code', '=', 'model.send_pending_finalization_email()'),
	], limit=1)

	# Definir próxima ejecución: hoy o mañana a las 03:00 (hora servidor)
	now = fields.Datetime.now()
	nextcall_dt = now.replace(hour=3, minute=0, second=0, microsecond=0)
	if nextcall_dt < now:
		nextcall_dt += timedelta(days=1)

	vals = {
		'name': 'Enviar resumen de finalizaciones pendientes',
		'model_id': model.id,
		'state': 'code',
		'code': 'model.send_pending_finalization_email()',
		'interval_number': 1,
		'interval_type': 'days',
		'nextcall': nextcall_dt.strftime('%Y-%m-%d %H:%M:%S'),
		'active': True,
		'user_id': env.ref('base.user_root').id,
		# Odoo 18 ya no usa numbercall ni max_number_of_calls
		# Se ejecutará indefinidamente mientras esté activo
	}

	if cron:
		cron.write(vals)
	else:
		env['ir.cron'].create(vals)
