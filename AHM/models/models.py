# from datetime import time
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class Health(models.Model):
    _name = 'ahm.health'
    _description = "AHM Health"
    _rec_name = "duration"

    company_id = fields.Many2one('res.company', string="Clinic Name", required=True, default=lambda self: self.env.company)
    app_id = fields.Many2one(comodel_name="ahm.appointment", ondelete="cascade")
    starting_date = fields.Date(string="Starting Date")
    ending_date = fields.Date(string="Ending Date")
    duration = fields.Integer(compute="_compute_duration", store=True)
    graph_field = fields.Float(default=10)

    @api.depends('starting_date', 'ending_date')
    def _compute_duration(self):
        for i in self:
            if i.ending_date and i.starting_date:
                delta = i.ending_date - i.starting_date
                i.duration = delta.days
            else:
                i.duration = 0


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    new_field = fields.Char(config_parameter='ahm.new_field')
