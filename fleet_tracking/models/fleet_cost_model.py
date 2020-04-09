# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class TypeOfMaintenance(models.Model):
    _name = "fleet.maintenance.type"
    _description = "type of maintenance"

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    name = fields.Char('Name')


class FleetCost(models.Model):
    _name = "fleet.cost"
    _description = "manage expence on vehicle"

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    date = fields.Date('Service Date', required=True, default=fields.Date.today)
    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", ondelete="restrict", string="Vehicle", required=True)
    required_user_ids = fields.Many2many(comodel_name="res.users", compute="_compute_users")
    responcible_driver_id = fields.Many2one(comodel_name="res.users", ondelete="restrict", string='Driver Id', domain="[('id', 'in', required_user_ids)]")
    maintenance_type_id = fields.Many2one(comodel_name="fleet.maintenance.type", ondelete="restrict", string='Maintenance Type', required=True)
    cost = fields.Float('Cost', required=True)
    note = fields.Text('Note')

    @api.depends("responcible_driver_id")
    def _compute_users(self):
        self.required_user_ids = self.env['res.users'].search([]).filtered(lambda self: self.has_group('fleet_tracking.group_driver')).mapped('id')
