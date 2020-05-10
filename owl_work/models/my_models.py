# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class MyModel(models.Model):
    _name = "my.model"

    def get_livechat_mail_channel_vals(self):
        # partner to add to the mail.channel
        operator_partner_id = request.env.ref("base.user_admin").id
        channel_partner_to_add = [(4, operator_partner_id)]
        visitor_user = False
        if user_id:
            visitor_user = self.env['res.users'].browse(user_id)
            if visitor_user and visitor_user.active:  # valid session user (not public)
                channel_partner_to_add.append((4, visitor_user.partner_id.id))
        return {
            'channel_partner_ids': channel_partner_to_add,
            # 'livechat_active': True,
            # 'livechat_operator_id': operator_partner_id,
            # 'livechat_channel_id': self.id,
            # 'anonymous_name': False if user_id else anonymous_name,
            # 'country_id': country_id,
            # 'channel_type': 'livechat',
            # 'name': ' '.join([visitor_user.display_name if visitor_user else anonymous_name, operator.livechat_username if operator.livechat_username else operator.name]),
            # 'public': 'private',
            # 'email_send': False,
        }
