# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class OwlController(http.Controller):

    @http.route('/owl_demo', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("owl_task.demo_template")

    @http.route('/services/form', auth="user", type="json", csrf=False)
    def services_form(self, **kw):
        print('\n\n\n\n\n\n\n\n', kw)
        pm = request.env['product.product'].sudo().create([{
                    'name': kw.get('name'),
                    'purchase_ok': kw.get('purchase_ok'),
                    'sale_ok': kw.get('sale_ok'),
                    'type': kw.get('type'),
                    'standard_price': kw.get('standard_price'),
                    'list_price': kw.get('list_price'),
                    }])
        # return http.local_redirect('/owl_demo')
        return {"pm": pm}
