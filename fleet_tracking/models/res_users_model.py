# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"
    _descriptin = "create and maintain driver users from setting"

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    users_type = fields.Selection([('driver', 'Driver')], store=False,)
    driving_licence_nunmber = fields.Char(name="Driving licence number")
    birth_date = fields.Date('Birth Date')

    @api.model
    def create(self, vals):
        if vals['users_type'] == 'driver':
            vals['groups_id'] = [(6, 0, [self.env.ref('fleet_tracking.group_driver').id])]
        if vals['users_type'] == 'company':
            vals['groups_id'] = [(6, 0, [self.env.ref('fleet_tracking.group_manager').id])]
        else:
            vals['groups_id'] = [(6, 0, [self.env.ref('fleet_tracking.group_customer').id])]
            vals['email'] = vals['login']
            vals['password'] = '1234'

        return super(ResUsers, self).create(vals)
