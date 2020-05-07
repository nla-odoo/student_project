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

    # @http.route('/product', type='json', auth="public", csrf=False)
    # def get_product(self, **post):
    #     return request.env['product.product'].search([]).mapped('name')

    @http.route('/inquirey', type='json', auth="public", csrf=False)
    def get_leads(self, **post):
        return request.env['crm.lead'].search_read([], ['name', 'description'])
