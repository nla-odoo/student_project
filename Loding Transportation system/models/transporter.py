# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class transporter(models.Model):
    _name = 'transporter.transporter'
    _description = 'transporter.transporter'
    _rec_name = "name"

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    name = fields.Char(required=True, string="Name", copy=False, help="Enter Your Name")
    email = fields.Char(required=True, string="Email")
    contactnumber = fields.Integer(string="Contact Number")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    address = fields.Text(string="Address")
    city = fields.Char(string="City")
    pincode = fields.Integer(string="Pincode")
    state_id = fields.Many2one('res.country.state', string='State', domain=([('country_id.name', "in", ["India"])]))
    photo = fields.Binary(attachment=True, string="Image")
