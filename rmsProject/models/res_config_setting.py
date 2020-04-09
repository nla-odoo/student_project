from odoo import models, fields


class ConfigSettiing(models.TransientModel):
    _inherit = 'res.config.settings'

    sandbox_merchant_id = fields.Char(config_parameter='rms.sandbox_merchant_id')
    sandbox_merchant_key = fields.Char(config_parameter='rms.sandbox_merchant_key')

