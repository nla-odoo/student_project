from odoo import models, fields


class example(models.TransientModel):
    _inherit = 'res.config.settings'

    merchant_id = fields.Char(config_parameter="MID")
    merchant_key = fields.Char(config_parameter="MERCHANT_KEY")
