# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'res.partner']
    _description = 'Customer Detail'

    order_ids = fields.One2many('order.detail', 'customer_id', string="order IDs")
