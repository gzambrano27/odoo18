# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request

class ModuleInfoController(http.Controller):

    @http.route('/api/v1/configs', type='http', auth='public', methods=['GET'], csrf=False)
    def list_configs(self, **kwargs):
        """Devuelve la lista de configuraciones disponibles."""
        configs = request.env['module.api.config'].sudo().search([])
        data = configs.read(['id', 'name', 'module_id', 'api_endpoint'])
        return request.make_response(
            json.dumps({'configs': data}, default=str),
            [('Content-Type', 'application/json')]
        )

    @http.route('/api/v1/configs/<int:config_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_config(self, config_id, **kwargs):
        """Devuelve los detalles de una configuración específica."""
        config = request.env['module.api.config'].sudo().browse(config_id)
        if not config.exists():
            return request.make_response(
                json.dumps({'error': 'Configuración no encontrada'}, default=str),
                [('Content-Type', 'application/json')], status=404
            )

        result = {
            'id': config.id,
            'name': config.name,
            'module': config.module_id.model,
            'access_token': config.access_token,
            'api_endpoint': config.api_endpoint,
            'fields': [
                {
                    'field_name': line.model_id.name,
                    'alias': line.name_alias,
                    'technical_name': line.model_id.name,
                }
                for line in config.field_ids
            ]
        }
        return request.make_response(
            json.dumps(result, default=str),
            [('Content-Type', 'application/json')]
        )

    @http.route('/api/v1/<string:module>/data', type='http', auth='public', methods=['GET'], csrf=False)
    def get_module_data(self, module, token=None, **kwargs):
        """
        Devuelve los registros configurados para un módulo determinado.
        Se busca primero la configuración que coincide con el módulo + token.
        """
        Config = request.env['module.api.config'].sudo()

        # ✅ Buscar la configuración que coincida con el módulo y token
        config = Config.search([
            ('module_id.model', '=', module),
            ('access_token', '=', token)
        ], limit=1)

        if not config:
            return request.make_response(
                json.dumps({'error': 'Token inválido o configuración no encontrada'}, default=str),
                [('Content-Type', 'application/json')], status=403
            )

        # Agrupar campos por modelo
        model_fields = {}
        for line in config.field_ids:
            model_name = line.model_id.model_id.model
            model_fields.setdefault(model_name, []).append(line.model_id.name)

        data = {}
        dominio_raw = kwargs.get('dominio') or config.dominio

        try:
            domain = json.loads(dominio_raw) if dominio_raw else []
            if not isinstance(domain, list):
                raise ValueError()
        except Exception:
            return request.make_response(
                json.dumps({'error': 'El dominio debe ser una lista JSON válida. Ejemplo: [["state", "=", "posted"]]'}, default=str),
                [('Content-Type', 'application/json')], status=400
            )

        for model_name, fields in model_fields.items():
            try:
                records = request.env[model_name].sudo().search_read(domain, fields=fields)
                data[model_name] = records
            except Exception as e:
                data[model_name] = {'error': str(e)}

        result = {
            'config': config.name,
            'module': module,
            'data_count': {m: len(r) if isinstance(r, list) else 0 for m, r in data.items()},
            'data': data,
        }

        return request.make_response(
            json.dumps(result, default=str),
            [('Content-Type', 'application/json')]
        )
