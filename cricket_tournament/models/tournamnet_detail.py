# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime

from odoo import api, fields, models


class TournamentDetail(models.Model):
    _name = "tournament.detail"
    _inherit = ['mail.thread']
    _description = "Tournament Detail"

    name = fields.Char(string="Tournament Name", required=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    place = fields.Char(string="Tournament Place")
    tournamenttype = fields.Selection([('latherballtournament', 'Leather Ball Tournaments'), ('tennisballtournament', 'Tennis Ball Tournaments'), ('underarmstournament', 'Underarms Tournaments'), ('tapeballtournament', 'Tape Ball Tournaments')], string="Tournament Type")
    team = fields.Integer(string="Participate Team")
    starting_date = fields.Date(string="Tournament Starting Date")
    ending_date = fields.Date(string="Tournament Ending Date")
    status_days = fields.Integer("", compute="_compute_status", compute_sudo=True)
    shedule = fields.One2many("match.detail", "match_id", string="Shedule")
    status = fields.Selection([('ongoing', 'Ongoing'), ('upcoming', 'Upcoming'), ('past', 'Past')], compute="_compute_status", store=True)

    # @api.depends('starting_date', 'ending_date')
    # def _compute_status(self):
    #     for record in self:
    #         record.status_days = (record.ending_date - record.starting_date).days
    #         start_date_diff = (datetime.date.today() - record.starting_date).days
    #         end_date_diff = (record.ending_date - datetime.date.today()).days
    #         if start_date_diff >= 0 and end_date_diff <= 0:
    #             record.status = "past"
    #         elif start_date_diff >= 0 and end_date_diff >= 0:
    #             record.status = "ongoing"
    #         elif start_date_diff < 0 and end_date_diff >= 0:
    #             record.status = "upcoming"
