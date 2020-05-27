from odoo import fields, models


class AddFeedback(models.Model):
    _inherit = "res.users"

    name = fields.name()
    mobile = fields.Integer()
    feedback = fields.Integer()
