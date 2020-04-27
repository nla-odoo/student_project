# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
import uuid

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MatchDetail(models.Model):
    _name = "match.detail"
    _description = "Match Detail"

    def _default_order_reference(self):
        return str(uuid.uuid4())

    tournamentname = fields.Many2one('tournament.detail', string="Tournamnet Name")
    name = fields.Char(string="Match Name", required=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    team1name_id = fields.Many2one("team.detail", string="Team1Name")
    team2name_id = fields.Many2one("team.detail", string="Team2Name")
    matchover = fields.Integer(string="Match Over")
    matchdatetime = fields.Datetime(string="Match_Date_Time")
    umpirename = fields.Char(string="Umpire Name")
    matchvenue = fields.Text(string="Match Venue")
    match_id = fields.Many2one("tournament.detail", string="match", ondelete="restrict")
    status = fields.Selection([('live', 'Live'), ('upcoming', 'Upcoming'), ('past', 'Past')], default="upcoming")
    amount = fields.Integer()
    order_id = fields.Char(default=_default_order_reference, store=True)
    acquirer_ref = fields.Char()
    transaction_date = fields.Date("Transaction Date", default=datetime.date.today())
    payment_status = fields.Selection([('done', 'Done'), ('pending', 'Pending'), ('fail', 'Fail')])

    def button_payment(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': '/demo/{}'.format(self.id),
        }

    @api.constrains('matchover')
    def _validate_matchover(self):
        if self.matchover < 10:
            raise ValidationError('enter 10 or greter then 10 over match')

    @api.onchange('matchover')
    def onchange_amount(self):
        if self.matchover >= 10 and self.matchover <= 20:
            self.amount = 500
        elif self.matchover >= 21 and self.matchover <= 50:
            self.amount = 700
        elif self.matchover > 50:
            self.amount = 1000
