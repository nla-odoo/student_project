# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class FuleType(models.Model):
    _name = "fleet.vehicle.fule.type"
    _description = "type of fule"

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    name = fields.Char('Fule Type')


class vehicle(models.Model):
    _name = "fleet.vehicle"
    _description = "vehicle detail"
    _rec_name = "license_plate"

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    model_id = fields.Many2one(comodel_name='fleet.vehicle.car.model', string='Model',
                               tracking=True, required=True, help='Model of the vehicle')
    license_plate = fields.Char(name="license plate")
    no_of_seats = fields.Integer(name="Seats Number")
    no_of_doors = fields.Integer(name="Doors Number")
    color = fields.Char(name="Color", size=15)
    model_year = fields.Char(name="Model Year")
    description = fields.Text(name="Description")
    fule_type = fields.Many2one(comodel_name="fleet.vehicle.fule.type", ondelete="restrict", string="Fule Type")
    contract_id = fields.Many2one(comodel_name="fleet.vehicle.trip.booking")
    image_128 = fields.Image(related='model_id.image_128', readonly=False, store=True)

    def name_get(self):
        name = []
        for vehicle in self:
            name.append((vehicle.id, str(vehicle.model_id.brand_id.name)+"-"+str(vehicle.model_id.name)+"/"+str(vehicle.license_plate)+"-"+str(vehicle.color)))
        return(name)
