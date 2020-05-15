# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class TotalCharges(models.Model):
    _name = 'ahm.total.charges'
    _description = "AHM Total Charges"

    app_id = fields.Many2one(comodel_name="ahm.appointment", ondelete="cascade")
    company_id = fields.Many2one('res.company',  default=lambda self: self.env.company)
    medicine_charges = fields.Integer(string="Medicine Charges", required=True)
    total_bill = fields.Float(compute="_compute_total")
    visiting_charges = fields.Integer("Visiting Charges", default=450)
    date = fields.Date(string="Date")

    @api.depends('medicine_charges', 'visiting_charges')
    def _compute_total(self):
        for ahm in self:
            ahm.total_bill = ahm.medicine_charges + ahm.visiting_charges


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sandbox_merchant_id = fields.Char(config_parameter='sandbox_merchant_id')
    website_url = fields.Char(config_parameter='website_url')
    sandbox_merchant_key = fields.Char(config_parameter='sandbox_merchant_key')
    industry_type = fields.Char(config_parameter='industry_type')
