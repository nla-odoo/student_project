# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.http import request


class SearchBox(http.Controller):

    @http.route(['/search', '/sort/<string:order_by>'], auth='public', csrf=False)
    def search_box(self, order_by=None):
        domain = http.request.env['product.product'].sudo()
        if order_by:
            if order_by == 'name_asc':
                products = domain.search([], order='name asc')
            elif order_by == 'name_desc':
                products = domain.search([], order='name desc')
            elif order_by == 'price_asc':
                products = domain.search([], order='list_price asc')
            elif order_by == 'price_desc':
                products = domain.search([], order='list_price desc')
            elif order_by == 'type_service':
                products = domain.search([('type', '=', 'service')])
            elif order_by == 'type_consu':
                products = domain.search([('type', '=', 'consu')])
            else:
                products = domain.search([])
        else:
            products = domain.search([])
        return request.render('search_box.portal_search_box', {'products': products})
