# -*- coding: utf-8 -*-
# Part of Wicoders Solutions. See LICENSE file for full copyright and licensing details

from odoo import _, api, fields, models, _
from openai import OpenAI
import logging

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.model
    def get_view(self, view_id=None, view_type='form', **options):
        res = super().get_view(view_id, view_type, **options)

        api_key = self.env['ir.config_parameter'].sudo().get_param("wc_chatgpt_integration.api_key")

        if not api_key:
            from lxml import etree
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='model_type']"):
                node.set('readonly', '1')
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

    def get_model_list(self, use_saved=True):
        try:
            if use_saved:
                api_key = self.env['ir.config_parameter'].sudo().get_param(
                    'wc_chatgpt_integration.api_key'
                )
            else:
                api_key = self.api_key
            if api_key:
                client = OpenAI(api_key=api_key)
                models = client.models.list()
                a = []
                for x in models.data:
                    a.append((x.id, x.id))
                self.is_valid_api_key = True
                return a
            else:
                return []
        except Exception as e:
            self.is_valid_api_key = False
            _logger.exception("Error fetching AI model list: %s", e)
            return []

    api_key = fields.Char('OpenAI API Key', config_parameter='wc_chatgpt_integration.api_key')
    model_type = fields.Selection(get_model_list, config_parameter='wc_chatgpt_integration.model_type',
                                  string="AI Model")
    is_valid_api_key = fields.Boolean('Is Valid API key', config_parameter='wc_chatgpt_integration.is_valid_api_key',
                                      default=False)

    is_enable = fields.Boolean('Is Enable?',config_parameter='wc_chatgpt_integration.is_enable')


    @api.onchange('api_key')
    def _onchange_api_key(self):
        models = self.get_model_list(use_saved=False)
        if not models:
            self.model_type = False