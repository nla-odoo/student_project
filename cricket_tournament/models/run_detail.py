# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class RunDetail(models.Model):
    _name = 'run.detail'
    _description = 'Run Detail'

    scoreboard_id = fields.Many2one('score.board')
    toss_id = fields.Many2one('toss.detail')
    batting_id = fields.Many2one('score.board')
    run = fields.Integer(string="run")
    over = fields.Float(string="Over", digits=(12, 1))
    totalrun = fields.Integer(compute="_compute_totalrun", store=True)
