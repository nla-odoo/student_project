# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http, tools
from odoo.http import request


class OwlController(http.Controller):

    @http.route('/owl_work', type='http', auth='public', csrf=False, website=True)
    def owl_work(self, **post):
        return http.request.render("owl_work.btn_template")

    @http.route('/get_livechat_mail_channel_vals', type='json', auth='public', csrf=False, website=True)
    def get_livechat_mail_channel_vals(self):
        operator_partner_id = http.request.env.ref("base.user_admin").sudo().partner_id
        channel_partner_to_add = [(4, operator_partner_id.id)]

        mail_channel_vals = {
            'channel_partner_ids': channel_partner_to_add,
            # 'livechat_active': True,
            'livechat_operator_id': operator_partner_id.id,
            # 'livechat_channel_id':  1,
            # 'anonymous_name': 3,
            # 'country_id': 2,
            'channel_type': 'livechat',
            'name': '%s - %s' % (operator_partner_id.name, 'Visitor'),
            'public': 'private',
            'email_send': False,
        }

        mail_channel = http.request.env["mail.channel"].with_context(mail_create_nosubscribe=False).sudo().create(mail_channel_vals)
        print('mail_channel***************************', mail_channel)
        print(">>>>>>>>>>>>>>>", mail_channel.channel_info()[0])
        return mail_channel.channel_info()[0]

    @http.route('/mail/send_message', type="json", auth="public", cors="*")
    def send_message(self, uuid, message_content, **kwargs):
        mail_channel = request.env["mail.channel"].sudo().search([('uuid', '=', uuid)], limit=1)
        if not mail_channel:
            return False

        # find the author from the user session
        author_id = False
        email_from = 'Visitor'
        # post a message without adding followers to the channel. email_from=False avoid to get author from email data
        body = tools.plaintext2html(message_content)
        message = mail_channel.with_context(mail_create_nosubscribe=True).message_post(author_id=author_id, email_from=email_from, body=body, message_type='comment', subtype_xmlid='mail.mt_comment')
        return message and message.id

    @http.route('/mail/recive_message', type="json", auth="public", cors="*")
    def recive_message(self, uuid, message_content, **kwargs):
        mail_channel = request.env["mail.channel"].sudo().search([('uuid', '=', uuid)], limit=1)
        if not mail_channel:
            return False

        # find the author from the user session
        author_id = False
        email_from = 'Visitor'
        # post a message without adding followers to the channel. email_from=False avoid to get author from email data
        body = tools.plaintext2html(message_content)
        message = mail_channel.with_context(mail_create_nosubscribe=True).message_post(author_id=author_id, email_from=email_from, body=body, message_type='comment', subtype_xmlid='mail.mt_comment')
        return message and message.id
