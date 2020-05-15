# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class OwlController(http.Controller):
    @http.route('/owl_demo', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("OWL_DEMO.demo_template")

    @http.route('/owl_demo_rating', type='json', auth="user", csrf=False)
    def owl_rating(self, **kw):
        pm = request.env['rating.rating'].sudo().create([{
                    'res_id': kw.get('res_id'),
                    'feedback': kw.get('feedback'),
                    'partner_id': request.env.user.partner_id.id
                    }])
        print("\n\n\n\n\n\n\n\n\n", pm.res_id)
        return self.get_feedback()

    @http.route('/get_partner_data', type='json', auth="public", csrf=False)
    def get_partner(self, **post):
        return request.env['res.partner'].search([]).mapped('name')

    @http.route('/feedback', type='json', auth="user", csrf=False)
    def get_feedback(self, **post):
        partner = request.env.user.partner_id
        return http.request.env['rating.rating'].sudo().search_read([('partner_id', '=', partner.id)], ['feedback',  'res_id', ])

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
