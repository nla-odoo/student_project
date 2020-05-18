# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class OwlController(http.Controller):
    @http.route('/owl_demo', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("OWL_DEMO.demo_template")

    @http.route('/owl_demo_rating', type='http', auth="user", csrf=False)
    def owl_rating(self, **kw):
            pm = request.env['rating.rating'].sudo().create([{
                'rating': int(kw.get('rating')),
                'feedback': kw.get('feedback'),
                'res_id': http.request.env['product.product'].sudo().browse(int(kw['res_id'])),
                'res_model': http.request.env['product.product'].sudo().browse(kw['res_model'])
            }])
            print("\n\n\n\n\n\n\n\n\n", pm.res_id)
            print("\n\n\n\n\n\n\n\n\n", pm.res_model)
            print("\n\n\n\n\n\n\n\n\n", pm.rating)
            print("\n\n\n\n\n\n\n\n\n", pm.feedback)
            return {"pm": pm}
# browse(rating.res_id)

    @http.route('/get_partner_data', type='http', auth="public", csrf=False)
    def get_partner(self, **post):
        return request.env['res.partner'].search([]).mapped('name')

    @http.route('/feedback', type='http', auth="user", csrf=False)
    def get_feedback(self, **post):
        partner = request.env.user.partner_id
        return http.request.env['rating.rating'].sudo().search_read([('partner_id', '=', partner.id)], ['feedback',  'res_id', ])
