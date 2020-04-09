# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class vehicles(models.Model):
    _name = 'vehicles.vehicles'
    _description = 'vehicles.vehicles'
    _rec_name = 'vehicle_type'

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    vehicle_type = fields.Integer(string="Vehicle Type(Wheeler)")
    vehicle_capacity = fields.Integer(string="Vehicle Capacity(KG)")
    vehicle_speed = fields.Integer(string="Vehicle Speed(kmph)")
    vehicle_weight = fields.Integer(string="Vehicle Weight(KG)")
    vehicle_length = fields.Integer(string="Vehicle Length(mtr)")
    vehicle_Engine = fields.Char(string="Vehicle Engine")
    vehicle_image = fields.Binary(string="Vehicle Image")
    available = fields.Selection([('available', 'Available'), ('not available', 'Not Available')], default='available')
