# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import uuid
from odoo import fields, models, api


class order(models.Model):
    _name = "order.order"
    _description = "order table"

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    inquiryid = fields.Many2one('inquirey.inquirey.demo', string="inquiryid", required=True)
    source_add = fields.Char(required=True, string="Source Address")
    desti_add = fields.Char(string="Destination Address", required=True)
    distance = fields.Integer(string="Distance(km)")
    duration = fields.Float(string="Duration(hr)", store=True)
    weight = fields.Integer(string="Weight(KG)")
    driver_id = fields.Many2one('drivers.drivers', string="Driver Name", required=True)
    vehicle_type = fields.Many2one('vehicles.vehicles', string="Vehicle Type", required=True)
    vehicle_capacity = fields.Integer(related='vehicle_type.vehicle_capacity', store=True, string="Vehicle Capacity")
    vehicle_speed = fields.Integer(related='vehicle_type.vehicle_speed', string="Vehicle Speed(kmph)", store=True)
    vehicle_weight = fields.Integer(related='vehicle_type.vehicle_weight', string="Vehicle weight(KG)", store=True)
    date = fields.Date(string="Date")
    state = fields.Selection([('onprogress', 'OnProgress'), ('done', 'Done')], required=True, default='onprogress')
    payment_state = fields.Selection([('pending', 'Pending'), ('done', 'Done'), ('fail', 'Fail')], store=True, default="pending")
    amount = fields.Integer(string="Amount", store=True)

    def _default_order_reference(self):
        return str(uuid.uuid4())
    order_ref = fields.Char(default=_default_order_reference, store=True)
    acquirer_ref = fields.Char()
    payment_date = fields.Date(string="Payment Date")

    @api.onchange('distance', 'amount')
    def calculateamount(self):
        self.amount = self.distance * 12

    @api.onchange('inquiryid', 'order_status')
    def getorder(self):
        orderid = self.env.context.get('current_id')
        self.inquiryid = orderid
        self.order_status = 'confirm'
        rec = self.env['inquirey.inquirey.demo'].search([])
        for i in rec:
            if i.id == orderid:
                self.source_add = i.source_add
                self.desti_add = i.desti_add
                self.distance = i.distance
                self.duration = i.duration
                self.weight = i.weight
                self.vehicle_type = i.vehicle_type
                self.date = i.date
                self.driver_id = i.driver_id
                self.vehicle_type = i.vehicle_type

    @api.model
    def create(self, vals):
        self.env['drivers.drivers'].sudo().browse([vals.get('driver_id')]).write({'available': 'not available'})
        self.env['vehicles.vehicles'].sudo().browse([vals.get('vehicle_type')]).write({'available': 'not available'})
        return super(order, self).create(vals)

    def button_onprogress(self):
        self.env['drivers.drivers'].sudo().search([])
        self.env['vehicles.vehicles'].sudo().search([])
        for driver in self:
            if driver.id == self.driver_id.id:
                driver.available = "not available"

        for vehicle in self:
            if vehicle.id == self.vehicle_type.id:
                vehicle.available = "not available"

    def button_done(self):
        rec = self.env['drivers.drivers'].sudo().search([])
        res = self.env['vehicles.vehicles'].sudo().search([])
        for i in rec:
            if i.id == self.driver_id.id:
                i.available = "available"
        for j in res:
            if j.id == self.vehicle_type.id:
                j.available = "available"
        self.write({'state': 'done'})
