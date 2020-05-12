# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class OwlController(http.Controller):

    @http.route('/owl_demo', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("loading_transportation_system.demo_template")

    @http.route('/get_partner_data', type='json', auth="public", csrf=False)
    def get_partner(self, **post):
        return request.env['res.partner'].search([]).mapped('name')

    @http.route('/inquirey', type='json', auth="public", csrf=False)
    def get_leads(self, **post):
        partner = request.env.user.partner_id
        inquiries = http.request.env['crm.lead'].sudo().search([('partner_id', '=', partner.id)])
        print("\n\n\n\n\n\n", inquiries)
        return request.env['crm.lead'].sudo().search_read([], ['name', 'description', 'partner_id', 'type'])
        # return request.env['crm.lead'].sudo().search_read([], ['name', 'description', 'partner_id', 'type']).mapped('partner_id')

    @http.route('/lead/form/', auth="public", type="json", csrf=False)
    def lead_form(self, **kw):
        print('\n\n\n\n\n\n\n\n', kw)
        var = request.env['crm.lead'].sudo().create([{
                    'description': kw.get('description'),
                    'name': kw.get('name'),
                    'user_id': False
                    }])
        return {'var': var}
