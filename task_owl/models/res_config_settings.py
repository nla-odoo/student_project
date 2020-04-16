# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'system parameters'

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    sandbox_merchant_id = fields.Char(config_parameter='sandbox_merchant_id')
    website_url = fields.Char(config_parameter='website_url')
    sandbox_merchant_key = fields.Char(config_parameter='sandbox_merchant_key')
    industry_type = fields.Char(config_parameter='industry_type')
