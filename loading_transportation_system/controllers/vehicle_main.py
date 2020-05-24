# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class OwlController(http.Controller):

    @http.route('/my_vehicles', type='http', auth="public", csrf=False)
    def vehicles(self, **post):
        return http.request.render("loading_transportation_system.display_template")

    @http.route('/vehicle', type='json', auth="public", csrf=False)
    def get_vehicle(self, **post):
        # partner = request.env.user.partner_id
        # return http.request.env['crm.lead'].sudo().search_read([('partner_id', '=', partner.id)], ['name', 'description', 'partner_id', 'type'])
        v = request.env['product.template'].sudo().search_read([], ['name', 'description', ])
        # console.log(v)
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n vehicle", v)
        return request.env['product.template'].sudo().search_read([], ['name', 'description', ])

    @http.route('/vehicle/form/', auth="public", type="json", csrf=False)
    def vehicle_form(self, **kw):
        # print('\n\n\n\n\n\n\n\n', kw)
        request.env['product.template'].sudo().create([{
                    'description': kw.get('description'),
                    'name': kw.get('name'),
                    'user_id': False,
                    'partner_id': request.env.user.partner_id.id
                    }])
        return self.get_vehicle()
