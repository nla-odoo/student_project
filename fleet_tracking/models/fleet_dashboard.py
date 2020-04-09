# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
from collections import Counter

from odoo import api, fields, models, _


class FleetDashboard(models.Model):
    _name = "fleet.dashboard"
    _description = "overview of module"

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    name = fields.Boolean(name="Name", default=True)
    kanban_dashboard_graph = fields.Text(compute='_kanban_dashboard_graph')
    partner_id = fields.Many2one('res.partner', string='Customer', tracking=10, index=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, TIN, Email or Internal Reference.")

    @api.depends("name")
    def _kanban_dashboard_graph(self):
        for journal in self:
            journal.kanban_dashboard_graph = json.dumps(journal.get_bar_graph_datas())

    def get_bar_graph_datas(self):
        data = []
        data.append({'label': _('month'), 'value': 0.0, 'type': 'past'})
        contract_env = self.env['fleet.vehicle.contract.booking'].search([])
        list_of_date = [date.start_date.strftime("%m") for date in contract_env]
        data_values = Counter(list_of_date)

        for key in data_values:
            data.append({'label': key, 'value': data_values[key], 'type': 'past'})

        return [{'values': data, 'title': "Monthly Contract", 'key': "graph_key", 'is_sample_data': True}]
