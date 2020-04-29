# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class OwlController(http.Controller):

    @http.route('/product_list', type='http', auth="public", csrf=False)
    def product_list(self, **post):
        return http.request.render("task_owl.product_list")

    @http.route('/get_product_data', type='json', auth="public", csrf=False)
    def get_product_data(self, **post):
        products1 = request.env['product.template'].sudo().search([])
        mydict = {}
        # product.image_1920,
        for product in products1:
            mydict[product.id] = [product.name, product.type, product.list_price]
        # print("---------------------------", mydict)
        return json.dumps(mydict)
