# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class OwlController(http.Controller):
    @http.route('/owl_demo', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("OWL_DEMO.demo_template")

    @http.route('/owl_demo_complain', type='http', auth="public", csrf=False)
    def owl_complain(self, **post):
        return http.request.render("OWL_DEMO.demo_template_complain")

    @http.route('/owl_demo_feedback', type='http', auth="public", csrf=False)
    def owl_feedback(self, **post):
        return http.request.render("OWL_DEMO.demo_template_feedback")

    @http.route('/owl_demo_rating', type='http', auth="public", csrf=False)
    def owl_rating(self, **post):
        return http.request.render("OWL_DEMO.demo_template_rating")

    @http.route('/get_partner_data', type='json', auth="public", csrf=False)
    def get_partner(self, **post):
        return request.env['res.partner'].search([]).mapped('name')

    @http.route('/inquirey', type='http', auth="public", csrf=False)
    def get_leads(self, **post):
        partner = request.env.user.partner_id
        return http.request.env['crm.lead'].sudo().search_read([('partner_id', '=', partner.id)], ['name', 'description', 'partner_id', 'type'])
        return request.env['crm.lead'].sudo().search_read([], ['name', 'description', 'partner_id', 'type'])
        return request.env['crm.lead'].sudo().search_read([], ['name', 'description', 'partner_id', 'type']).mapped('partner_id')

    @http.route('/lead/form/', auth="public", type="http", csrf=False)
    def lead_form(self, **kw):
        print('\n\n\n\n\n\n\n\n', kw)
        request.env['crm.lead'].sudo().create([{
                    'description': kw.get('description'),
                    'name': kw.get('name'),
                    'user_id': False,
                    'partner_id': request.env.user.partner_id.id
                    }])
        return self.get_leads()
