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

    @http.route('/lead/form/', auth="public", type="json", csrf=False)
    def lead_form(self, **kw):
        print('\n\n\n\n\n\n\n\n', kw)
        var = request.env['crm.lead'].sudo().create([{
                    'description': kw.get('description'),
                    'name': kw.get('name'),
                    'user_id': False
                    }])
        return {'var': var}

    # @http.route('/services/form', auth="user", type="json", csrf=False)
    # def services_form(self, **kw):
    #     print('\n\n\n\n\n\n\n\n', kw)
    #     pm = request.env['product.product'].sudo().create([{
    #                 'name': kw.get('name'),
    #                 'purchase_ok': kw.get('purchase_ok'),
    #                 'sale_ok': kw.get('sale_ok'),
    #                 'type': kw.get('type'),
    #                 'standard_price': kw.get('standard_price'),
    #                 'list_price': kw.get('list_price'),
    #                 }])
    #     # return http.local_redirect('/owl_demo')
    #     return {"pm": pm}
