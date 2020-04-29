# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class OwlController(http.Controller):

    @http.route('/product_list', type='http', auth="public", csrf=False)
    def product_list(self, **post):
        return http.request.render("task_owl.product_list")

    @http.route('/get_product_data', type='json', auth="public", csrf=False)
    def get_product_data(self, **post):
        products = request.env['product.template'].sudo().search([])
        mylist = ['id', 'image_1920', 'name', 'type', 'price', 'active']
        return products.read(mylist)
