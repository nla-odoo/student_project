# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class inquirey(models.Model):
    _name = 'inquirey.inquirey.demo'
    _description = 'inquirey.inquirey'
    _rec_name = "id"

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    source_add = fields.Char(required=True, string="Source Address")
    desti_add = fields.Char(string="Destination Address", required=True)
    distance = fields.Integer(string="Distance(km)")
    duration = fields.Integer(string="Duration(hr)")
    weight = fields.Integer(string="Weight(KG)")
    product_name = fields.Char(string="Product Name")
    price = fields.Float(string="Price")
    date = fields.Date(string="Date")

   