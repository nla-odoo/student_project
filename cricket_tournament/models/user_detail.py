# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class UserDetail(models.Model):
    _name = "user.detail"
    _description = "User Detail"

    name = fields.Char(string="Player Name", required=True)
    user_type = fields.Selection([('player', 'Player'), ('umpire', 'Umpire')])
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    image = fields.Binary(string="Player Image")
    address = fields.Text(string="Player Address")
    age = fields.Integer(string="Player Age")
    role = fields.Selection([('batsman', 'Batsman'), ('bowler', 'Bowler'), ('allrounder', 'Allrounder'), ('keeparbatsman', 'Keeparbatsman')], string="Player Role")
    batting_style = fields.Char(string="Batting Style")
    bowling_style = fields.Char(string="Bowling Style")
    user_id = fields.Many2one('team.detail', string="user", ondelete="restrict")
