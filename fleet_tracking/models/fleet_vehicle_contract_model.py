# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import uuid

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class VehicleContract(models.Model):
    _name = "fleet.vehicle.contract.booking"
    _description = "service tpye of the vehicle"
    _rec_name = "customer_id"

    start_date = fields.Date('Start Date', required=True, default=fields.Date.today)
    end_date = fields.Date('End Date', required=True, default=fields.Date.today)
    duration = fields.Char('Duration', compute="_compute_duration", default=0)
    available_vehicle_ids = fields.Many2many(comodel_name="fleet.vehicle", compute="_compute_available_vehicles")
    vehicle_ids = fields.Many2many(comodel_name="fleet.vehicle", domain="[('id', 'in',available_vehicle_ids)]", string='Vehicle', required=True)
    instruction = fields.Text(name="Other Instruction")
    state = fields.Selection(selection=[('draft', 'Draft'), ('confirm', 'Confirm'), ('cancelled', 'Cancelled'), ('running', 'Running'), ('closed', 'Closed'), ('renew', 'ReNew')], default='draft')
    count_trips = fields.Integer(compute="_count_trips")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    required_user_ids = fields.Many2many(comodel_name="res.users", compute="_compute_users")
    customer_id = fields.Many2one(string="Customer Name", comodel_name="res.users", domain="[('id', 'in', required_user_ids)]", context=lambda self: {'default_groups_id': [(6, 0, [self.ref('fleet_tracking.group_customer').id])]})
    model_id = fields.Many2one('fleet.vehicle.car.model', 'Model')
    image_128 = fields.Image(related='model_id.image_128', readonly=False)
    cancelled_reason_id = fields.Many2one(comodel_name="fleet.cancelled.reason", string="Cancelled Reason")
    cancelled_date = fields.Date('Cancelled Date', default=None)
    closed_reason_id = fields.Many2one(comodel_name="fleet.cancelled.reason", string="Closed Reason")
    closed_date = fields.Date('Closed Date', default=None)
    renew_ids = fields.One2many(comodel_name="fleet.contract.renew", inverse_name='contract_id', string="ReNew", stored=False)
    order_id = fields.Char("Order Id", default=str(uuid.uuid4()))
    acquirer_ref = fields.Char("Acquirer Ref")
    payment_status = fields.Char("Payment Status")
    payment_date = fields.Char("Payment Date")

    @api.depends("start_date", "end_date")
    def _compute_duration(self):
        for record in self:
            record.duration = (record.end_date - record.start_date).days + 1

    @api.depends("start_date", "end_date")
    def _compute_available_vehicles(self):
        booking_ids = self.env['fleet.vehicle.contract.booking'].search(['&', ('state', '!=', 'cancelled'), '|', '&', ('start_date', '<=', self.start_date), ('end_date', '>=', self.start_date),
                                                                         '&', ('start_date', '<=', self.end_date), ('end_date', '>=', self.end_date)])

        booking_renew_ids = self.env['fleet.contract.renew'].search(['&', ('state', '!=', 'cancelled'), '|', '&', ('start_date', '<=', self.start_date), ('end_date', '>=', self.start_date),
                                                                     '&', ('start_date', '<=', self.end_date), ('end_date', '>=', self.end_date)])

        vehicle_ids = booking_ids.filtered(lambda con: con.state in ['confirm', 'running']).mapped('vehicle_ids.id')
        vehicle_ids += booking_renew_ids.filtered(lambda con: con.state in ['confirm', 'running']).mapped('vehicle_ids.id')

        self.available_vehicle_ids = self.env['fleet.vehicle'].search([('id', 'not in', vehicle_ids)])

    def open_trip_view(self):
        if self.count_trips > 0:
            if self.state in ['confirm', 'running']:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Assignation Logs',
                    'view_type': 'list',
                    'view_mode': 'list,form',
                    'res_model': 'fleet.vehicle.contract.trip',
                    'domain': [('contract_id', '=', self.id)],
                    'context': {'default_contract_id': self.id}
                }
            if self.state in ['closed', 'renew']:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Assignation Logs',
                    'view_type': 'list',
                    'view_mode': 'list',
                    'res_model': 'fleet.vehicle.contract.trip',
                    'domain': [('contract_id', '=', self.id)],
                }
        else:
            if self.state in ['confirm', 'running']:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'New Trip',
                    'view_mode': 'form',
                    'res_model': 'fleet.vehicle.contract.trip',
                    'context': {'default_contract_id': self.id}
                }

    def _count_trips(self):
        self.count_trips = self.env['fleet.vehicle.contract.trip'].search_count([('contract_id', '=', self.id)])

    def action_renew_contract(self, **args):
        return {
            'type': 'ir.actions.act_window',
            'name': 'ReNew Contract',
            'view_mode': 'form',
            'res_model': 'fleet.contract.renew',
            'target': 'new',
            'context': {'default_contract_id': self.id,
                        'default_instruction': self.instruction,
                        }
        }

    def action_draft(self):
        return self.write({'state': 'draft'})

    def action_confirm(self):
        return self.write({'state': 'confirm'})

    def action_running(self):
        return self.write({'state': 'running'})

    @api.depends("customer_id")
    def _compute_users(self):
        self.required_user_ids = self.env['res.users'].search([]).filtered(lambda self: self.has_group('fleet_tracking.group_customer')).mapped('id')

    @api.constrains('start_date', 'end_date')
    def _check_validity_of_date(self):
        if self.end_date < self.start_date:
            raise ValidationError("Contract end date must be greter than start date")


class ContractRenew(VehicleContract):
    _name = "fleet.contract.renew"
    _description = "detail of renew contract"
    _inherit = 'fleet.vehicle.contract.booking'


    contract_id = fields.Many2one(comodel_name="fleet.vehicle.contract.booking", string="Contract Id")
    renew_date = fields.Date('Renew Date', default=fields.Date.today)
    state = fields.Selection(selection=[('draft', 'Draft'), ('confirm', 'Confirm'), ('cancelled', 'Cancelled'), ('running', 'Running'), ('closed', 'Closed')], default='draft')

    @api.model
    def create(self, vals):
        self.env["fleet.vehicle.contract.booking"].browse([vals['contract_id']]).filtered(lambda contract: contract.state == 'closed').write({'state': 'renew'})
        return super(ContractRenew, self).create(vals)


class ContractTrip(models.Model):
    _name = "fleet.vehicle.contract.trip"
    _description = "trip detail related to contract"
    _rec_name = "contract_id"

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    date = fields.Date('Date', required=True, default=fields.Date.today)
    contract_id = fields.Many2one(comodel_name="fleet.vehicle.contract.booking", string="Contract Id", domain="[('state','not in',['cancelled','draft'])]")
    required_vehicle_ids = fields.Many2many(comodel_name="fleet.vehicle", compute="_compute_required_vehicle_ids")
    vehicle_ids = fields.Many2many(comodel_name="fleet.vehicle", string="Vehicle Ids", domain="[('id', 'in', required_vehicle_ids)]")
    required_user_ids = fields.Many2many(comodel_name="res.users", compute="_compute_users")
    driver_id = fields.Many2one(comodel_name="res.users", ondelete="restrict", string='Driver Id', domain="[('id', 'in', required_user_ids)]")
    no_of_person_in_trip = fields.Integer(name="No of Person")
    address_ids = fields.Many2many(comodel_name='fleet.trip.address', string="Address")
    renew_id = fields.Many2one(comodel_name='fleet.contract.renew', string="Renew ID")

    @api.depends("driver_id")
    def _compute_users(self):
        self.required_user_ids = self.env['res.users'].search([]).filtered(lambda self: self.has_group('fleet_tracking.group_driver')).mapped('id')

    @api.depends("contract_id")
    def _compute_required_vehicle_ids(self):
        # vehicle_ids = self.env['fleet.vehicle.contract.booking'].filtered(['id', '=', self.contract_id]).mapped('vehicle_ids.id')
        # print(vehicle_ids, "============================", self.contract_id.vehicle_ids.ids)
        self.required_vehicle_ids = self.contract_id.vehicle_ids.ids


class State(models.Model):
    _name = "fleet.state"
    _description = "list of state"

    name = fields.Char(name="State Name")


class Address(models.Model):
    _name = "fleet.trip.address"
    _description = "address included in trip"

    _rec_name = "street1"
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    street1 = fields.Char(name="Street1")
    street2 = fields.Char(name="Street2")
    city = fields.Char(name="City")
    state_id = fields.Many2one(comodel_name="fleet.state", string="State")
    pincode = fields.Char(name="Pincode")
    notes = fields.Text(name="Notes")


class CancelledReason(models.Model):
    _name = "fleet.cancelled.reason"
    _description = "contract calcel & closed reason"

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    name = fields.Char(name="Reason", required=True)
    reason_type = fields.Boolean("Reason Type")
