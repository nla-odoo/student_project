# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import uuid

from odoo import fields, models


class order(models.Model):
    _inherit = "sale.order"
    _descriptin = "order details"

    order_id = fields.Char("Order Id", default=str(uuid.uuid4()))


class OrderLine(models.Model):
    _inherit = "sale.order.line"
    _descriptin = "order details"

    sale_order_id = fields.Char("Order Id", default=str(uuid.uuid4()))
