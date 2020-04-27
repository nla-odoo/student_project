# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    res_pay = fields.Char(config_parameter='cricket_tournament.res_pay')


class ResUser(models.Model):
    _inherit = 'res.users'

    user_pay = fields.Char(config_parameter='cricket_tournament.res_pay')
