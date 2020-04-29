# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class OwlController(http.Controller):

    @http.route('/owl_demo', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("owl_demo.demo_template")

    @http.route('/get_partner_data', type='json', auth="public", csrf=False)
    def get_partner(self, **post):
        result = request.env['res.partner'].search([])
        print(result.city)
        return request.env['res.partner'].search([]).mapped('name')
