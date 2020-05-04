# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class OwlController(http.Controller):

    @http.route('/owl_demo', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("owl_demo.demo_template")

    @http.route('/get_partner_data', type='json', auth="public", csrf=False)
    def get_partner(self, **post):
        user_id = request.env.user.partner_id
        print("\n\n\n\n", user_id)
        SaleOrder = request.env['sale.order']
        domain = [
            ('partner_id', '=', user_id.id),
            ('state', 'in', ['sale', 'done'])
        ]
        orders = SaleOrder.search(domain)
        print("\n\n\n\n order", orders)
        hh = orders.read(['id', 'name', 'date_order', 'amount_total'])
        print("\n\n\n\n hh", hh)
        return orders.read(['id', 'name', 'date_order', 'amount_total'])

    # @http.route('/owl_details', type='http', auth="public", csrf=False)
    # def owl_details(self, **post):
    #     return http.request.render("owl_demo.detail_template")

    # @http.route('/get_data/<model("sale.order"):saleid>', type='http', auth="public", csrf=False)
    # def get_data(self, saleid=None):
    #     print("\n\n\n\nsaleid ", saleid)
    #     details = request.env['sale.order.line'].search([])
    #     order_detail = details.read(['id', 'name', 'price_unit', 'price_tax', 'price_total', 'product_uom_qty'])
    #     return http.request.render("owl_demo.detail_template", {"order_detail": order_detail})
