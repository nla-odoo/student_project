# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class TossDetail(models.Model):
    _name = "toss.detail"
    _description = "Toss Detail"

    tournamentname = fields.Many2one('tournament.detail', string="Tournamnet Name")
    match = fields.One2many("match.detail", "match_id", related="tournamentname.shedule", string="Match", stored=True)
    name = fields.Many2one('match.detail', string="Match Name", domain="[('id','in',match)]")
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    team = fields.Many2many(comodel_name="team.detail", compute="_compute_team", string="Team", stored=False)
    tosswinnername = fields.Many2one('team.detail', string="Toss Winner Team", domain="[('id','in', team)]")
    decide = fields.Selection([('batting', 'Batting'), ('bowling', 'Bowling')])
    description = fields.Text()
    state = fields.Selection([('firstinning', 'First Inning'), ('secondinning', 'Second Inning'), ('done', 'Done')])

    @api.depends('name')
    def _compute_team(self):
        match = self.env['match.detail'].search([('id', '=', self.name.id)])
        l = [match.team1name_id.id, match.team2name_id.id]
        self.team = self.env['team.detail'].search([('id', 'in', l)])

    def button_firstinning(self):
        self.write({'state': 'firstinning'})
        match = self.env['match.detail'].search([('id', '=', self.name.id)])
        match.write({
            'status': "live"
            })
        return{
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'score.board',
            'target': 'current',
            'res_id': False,
            'type': 'ir.actions.act_window',
            'context': {'current_id': self.id}
        }

    def button_secondinning(self):
        self.write({'state': 'secondinning'})
        match = self.env['match.detail'].search([('id', '=', self.name.id)])
        match.write({
            'status': "live"
            })
        return{
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'score.board',
            'target': 'current',
            'res_id': False,
            'type': 'ir.actions.act_window',
            'context': {'current_id': self.id}
        }

    def button_done(self):
        self.write({'state': 'done'})
        match = self.env['match.detail'].search([('id', '=', self.name.id)])
        match.write({
            'status': "past"
            })
        return True
