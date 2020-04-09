# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class odometer(models.Model):
    _name = 'fleet.odometer'
    _description = "odometer entry"
    _rec_name = "vehicle_id"

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", ondelete="restrict", string="Vehicle")
    date = fields.Date('Date', required=True, default=fields.Date.today)
    required_user_ids = fields.Many2many(comodel_name="res.users", compute="_compute_users")
    driver_id = fields.Many2one(comodel_name="res.users", ondelete="restrict", string="Driver", domain="[('id', 'in', required_user_ids)]")
    odometer_reading = fields.Float('Odometer Reading')
    reading_unit = fields.Char('Unit', default="Km")

    @api.depends("driver_id")
    def _compute_users(self):
        self.required_user_ids = self.env['res.users'].search([]).filtered(lambda self: self.has_group('fleet_tracking.group_driver')).mapped('id')
