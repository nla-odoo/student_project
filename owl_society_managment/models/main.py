from odoo import fields, models
import uuid


class ResUser(models.Model):
    _inherit = "res.users"

    member_type = fields.Selection([
        ('treasurer', 'Treasurer'),
        ('member', 'Member'),
        ('secretary', 'Secretary'),
    ])


class SaleOrder(models.Model):
    _inherit = "account.payment"

    def default_order_reference(self):
        return str(uuid.uuid4())

    order_reference = fields.Char(default=default_order_reference, store=True)
