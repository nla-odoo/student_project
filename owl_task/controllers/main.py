# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class OwlController(http.Controller):

    @http.route('/owl_demo', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("owl_task.demo_template")

    @http.route('/services/form', auth="user", type="http", csrf=False)
    def services_form(self, **post):
        request.env['product.product'].sudo().create([{
                    'name': post.get('name'),
                    'purchase_ok': post.get('purchase_ok'),
                    'sale_ok': post.get('sale_ok'),
                    'type': post.get('type'),
                    'standard_price': post.get('standard_price'),
                    'list_price': post.get('list_price'),
                    }])
        return http.local_redirect('/owl_demo')
