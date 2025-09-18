# -*- coding: utf-8 -*-
# Part of Wicoders Solutions. See LICENSE file for full copyright and licensing details

from markupsafe import Markup
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.mail.tools.discuss import Store
from odoo.exceptions import AccessDenied, UserError, ValidationError
from openai import OpenAI, APIError
import json


class Channel(models.Model):
    _inherit = 'discuss.channel'

    is_chatgpt = fields.Boolean(string='Is Chatgpt')

    @api.model
    @api.returns('self', lambda channels: Store(channels).get_result())
    def channel_create_chatgpt(self, name, group_id):
        """ Create a channel and add the current partner, broadcast it (to make the user directly
            listen to it when polling)
            :param name : the name of the channel to create
            :param group_id : the group allowed to join the channel.
            :return dict : channel header
        """
        # create the channel
        vals = {
            'channel_type': 'channel',
            'name': name,
            'is_chatgpt': True,
        }
        new_channel = self.create(vals)
        group = self.env['res.groups'].search([('id', '=', group_id)]) if group_id else None
        new_channel.group_public_id = group.id if group else None
        notification = Markup('<div class="o_mail_notification">%s</div>') % _("created this channel.")
        new_channel.message_post(body=notification, message_type="notification", subtype_xmlid="mail.mt_comment")
        self.env.user._bus_send_store(new_channel)
        return new_channel

    @api.model
    @api.returns('self', lambda channels: Store(channels).get_result())
    def channel_get_chatgpt(self, partners_to,channel,force_open):
        if channel[0].get('id'):
            channel = self.env['discuss.channel'].sudo().browse(channel[0].get('id'))
            channel._broadcast(partners_to)
            return channel


    def check_api_key_and_model(self):
        ICP = self.env['ir.config_parameter'].sudo()
        is_valid_api_key = ICP.get_param('wc_chatgpt_integration.is_valid_api_key')
        is_enable = ICP.get_param('wc_chatgpt_integration.is_enable')
        vals_dict = {}
        if is_valid_api_key:
            vals_dict.update({'is_valid_api_key':True})

        if is_enable:
            vals_dict.update({'is_enable': True})

        return vals_dict



    def _notify_thread(self, message, msg_vals=False, **kwargs):
        rdata = super(Channel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)
        prompt = msg_vals.get('body')

        user_chatgpt = self.env.ref("wc_chatgpt_integration.chatgpt_user")
        partner_chatgpt = self.env.ref("wc_chatgpt_integration.chatgpt_partner")
        author_id = msg_vals.get('author_id')
        chatgpt_name = str(partner_chatgpt.name or '')
        if not prompt:
            return rdata
        try:
            if author_id != partner_chatgpt.id and chatgpt_name in msg_vals.get('record_name', ''):
                res = self._get_chatgpt_response(prompt=prompt)
                self.with_user(user_chatgpt).sudo().message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
            return rdata
        except Exception as e:
            raise UserError(_(e))

        return rdata

    def _get_chatgpt_response(self, prompt):
        ICP = self.env['ir.config_parameter'].sudo()
        api_key = ICP.get_param('wc_chatgpt_integration.api_key')
        gpt_model_id = ICP.get_param('wc_chatgpt_integration.model_type')
        client = OpenAI(api_key=api_key)
        try:
            completion = client.chat.completions.create(
                model=gpt_model_id,
                store=True,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ])
            content = completion.choices[0].message.content
        except APIError as e:
            try:
                error_json = e.response.json()
                content = error_json.get("error", {}).get("message", "Unknown error")
                return content
            except Exception:
                content = 'Something Went Wrong!'
                return content

        return content
