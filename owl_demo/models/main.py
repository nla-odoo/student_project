from odoo import fields, models


class MailChannel(models.Model):
    _inherit = "res.user"

    name = fields.Many2one('product.template')
    fess = fields.Integer('Color Index')
