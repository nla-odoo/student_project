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
        return request.env['crm.lead'].sudo().search_read([], ['name', 'description', 'partner_id'])

    # @http.route(['/inquirey/'], auth='public')
    # def Inquirey(self, **kw):
    #     partner = request.env.user.partner_id
    #     return http.request.render({'partner': partner})

    @http.route('/lead/form', auth="user", type="http", csrf=False)
    def lead_form(self, **post):
        request.env['crm.lead'].sudo().create([{
                    'description': post.get('description'),
                    'partner_id': int(post.get('partner_id')),
                    'name': post.get('name'),
                    'user_id': False
                    }])
        return http.local_redirect('/owl_demo')
