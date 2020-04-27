# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PrizeCaremony(models.Model):
    _name = "prize.caremony"
    _description = "Prize Caremony"

    name = fields.Char(string="Prize Name")
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    receiver_name_id = fields.Many2one("user.detail", string="Receiver Name")
    giver_name = fields.Char(string="Prize Giver Name")
    amount = fields.Integer(string="Prize Amount", copy=False)
