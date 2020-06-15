from odoo import fields, models


class ResUser(models.Model):
    _inherit = "res.users"

    contact_no = fields.Integer(string='Contact No.')
    address = fields.Text(string='Address')
    is_customer = fields.Integer(string='Customer')


class ResPartner(models.Model):
    _inherit = "res.partner"

    mobile = fields.Integer(string='Contact No.')
    address = fields.Text(string='Address')