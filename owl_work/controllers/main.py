# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http


class OwlController(http.Controller):

    @http.route('/owl_work', type='http', auth='public', csrf=False, website=True)
    def owl_work(self, **post):
        return http.request.render("owl_work.btn_template")

    @http.route('/get_livechat_mail_channel_vals', type='json', auth='public', csrf=False, website=True)
    def get_livechat_mail_channel_vals(self):
        # partner to add to the mail.channel
        operator_partner_id = http.request.env.ref("base.user_admin").id
        channel_partner_to_add = [(4, operator_partner_id)]
        visitor_user = False
        # if user_id:
        #     visitor_user = http.request.env['res.users'].browse(user_id)
        #     if visitor_user and visitor_user.active:  # valid session user (not public)
        #         channel_partner_to_add.append((4, visitor_user.partner_id.id))
        mail_channel_vals = {
            'channel_partner_ids': channel_partner_to_add,
            'livechat_active': True,
            'livechat_operator_id': operator_partner_id,
            'livechat_channel_id':  1,
            'anonymous_name': 3,
            'country_id': 2,
            'channel_type': 'livechat',
            'name': 'sd',
            'public': 'private',
            'email_send': False,
        }

        mail_channel = http.request.env["mail.channel"].with_context(mail_create_nosubscribe=False).sudo().create(mail_channel_vals)
        print('mail_channel', mail_channel)
        mail_channel._broadcast([operator_partner_id])
        return mail_channel.sudo().channel_info()[0]

    @http.route('/open_channel', type='json', auth='public', csrf=False, website=True)
    def open_channel(self, channel_id):
        print(channel_id)
