# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class MailChannel(models.Model):
    _inherit = "mail.channel"

    livechat_operator_id = fields.Many2one('res.partner')
    channel_type = fields.Selection(selection_add=[('livechat', 'Livechat')])
