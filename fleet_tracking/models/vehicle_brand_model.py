# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class CarModel(models.Model):
    _name = "fleet.vehicle.car.model"
    _table = 'fleet_vehicle_custom_table'
    _description = "vehicle models detail"

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    name = fields.Char(name="Model", required=True, help="Ex. Mustang SVT Cobra R.", string="Model Name")
    brand_id = fields.Many2one(comodel_name='fleet.vehicle.brand', String='Manufacturer', required=True, help='Manufacturer of the vehicle')
    image_128 = fields.Image(related='brand_id.image_128', readonly=False, store=True)

    def name_get(self):
        name = []
        for model in self:
            name.append((model.id, str(model.brand_id.name)+"-"+str(model.name)))
        return name


class VehicleBrand(models.Model):
    _name = "fleet.vehicle.brand"
    _description = "brand detail of the vehicle"

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    name = fields.Char(name="Name", required=True)
    active = fields.Boolean(default=True)
    image_128 = fields.Image('image_128', max_width=128, max_height=128)
