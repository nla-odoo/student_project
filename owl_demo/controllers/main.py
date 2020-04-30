# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class OwlController(http.Controller):

    @http.route('/owl_demo', type='http', auth="public", csrf=False, website=True)
    def owl_demo(self, **post):
        return http.request.render("owl_demo.demo_template")

    @http.route('/get_partner_data', type='json', auth="public", csrf=False, website=True)
    def get_partner(self, **post):
        product_list = []
        products = request.env['product.template'].sudo().search([])
        for product in products:
            product_list.append({
                "id": product.id,
                "name": product.name,
                "price": product.list_price,
                "type": product.type,
                "image": product.image_1024
            })
            print(product.list_price, "\n\n")
        return product_list
