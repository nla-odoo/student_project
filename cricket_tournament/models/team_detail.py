# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class TeamDetail(models.Model):
    _name = "team.detail"
    _description = "Team Detail"

    name = fields.Char(string="Team Name", required=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    playername_ids = fields.One2many("user.detail", "user_id", string="Player Name")
    captainname_id = fields.Many2one("user.detail", string="Captain Name")
    vicecaptainname_id = fields.Many2one("user.detail", string="Vice Captain Name")
    wicketkeeparname_id = fields.Many2one("user.detail", string="Wicket Keepar Name")
