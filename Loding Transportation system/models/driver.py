# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class drivers(models.Model):
    _name = 'drivers.drivers'
    _description = 'drivers.drivers'

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    name = fields.Char(string="Name")
    contactnumber = fields.Integer(string="Contact Number")
    email = fields.Char(string="Email")
    address = fields.Text(required=True, string="Address")
    date_of_birth = fields.Date(string="Date Of Date")
    licence = fields.Selection(store=True, selection=[('yes', 'yes'), ('no', 'no')], default="yes", string="Licence_Availability")
    licence_number = fields.Char(string="Licence Number")
    valid_date = fields.Date(string="Due Date")
    city = fields.Char(string="City")
    pincode = fields.Char(string="Pincode")
    state_id = fields.Many2one('res.country.state', string='State', domain=([('country_id.name', "in", ["India"])]), store=True)
    photo = fields.Binary(attachment=True, string="Image")
    available = fields.Selection([('available', 'Available'), ('not available', 'Not Available')], default='available')
