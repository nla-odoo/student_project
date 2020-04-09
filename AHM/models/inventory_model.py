# from datetime import datetime
from odoo import models, fields, api


class Medicine(models.Model):
    _name = 'ahm.medicine'
    _decription = "AHM Medicine"

    med_name = fields.Char(string="Medicine Name", required=True)
    med_type = fields.Selection(string="Medicine Type", selection=[('injection', 'Injection'), ('tablet', 'Tablet'), ('capsule', 'Capsule'), ('syrup', 'Syrup')], default='capsule')
    med_company = fields.Char(string="Medicine Company", required=True)
    price = fields.Integer(string="Price", required=True)
    manu_date = fields.Date(string="Manufactering Date")
    exp_date = fields.Date(string="Expiry Date")
    active = fields.Boolean(string="Active", default=True)


class Bill(models.Model):
    _name = 'ahm.bill'
    _decription = "AHM Bill"

    name = fields.Char(string="Name", required=True)
    comp = fields.Char(string="Company", required=True)
    price = fields.Float(string="Price", required=True)
    quantity = fields.Integer(string="Quantity", required=True)

    @api.model
    def create(self, vals):
        return super(Bill, self).create(vals)

    def write(self, vals):
        self.env['ahm.bill'].browse([1, 2])._context
        return super(Bill, self).write(vals)

    def copy(self, default=None):
        return super(Bill, self).copy()

    def unlink(self, default=None):
        return super(Bill, self).unlink()


class DoctorEquipment(models.Model):
    _name = 'ahm.doctor.equipment'
    _description = "AHM Doctor Equipment"

    name = fields.Char(string="Equipment Name")
    price = fields.Integer(string="Price")
    quantity = fields.Integer(string="Quantity")
