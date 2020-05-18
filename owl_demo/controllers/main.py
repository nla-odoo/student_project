# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class OwlController(http.Controller):

    @http.route('/my_orders', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("owl_demo.orders_template")

    @http.route('/get_order_details', type='json', auth="public", csrf=False)
    def get_partner(self, **post):
        domain = [
            ('partner_id', '=', request.env.user.partner_id.id),
            ('state', 'in', ['sale', 'done'])
        ]
        return request.env['sale.order'].sudo().search_read(domain, ['id', 'name', 'date_order', 'amount_total'])

    @http.route('/get_data/', type='http', auth="public", csrf=False)
    def owl_details(self, **post):
        return http.request.render("owl_demo.detail_template")

    @http.route('/order_detail', type='json', auth="public", csrf=False)
    def order_data(self, **kw):
        order = request.env['sale.order'].sudo().search([('id', '=', kw.get('order_id'))])
        order_detail = order.order_line.read(['id', 'name', 'price_unit', 'price_tax', 'price_total', 'product_uom_qty'])
        sale_detail = order.read(['name', 'date_order'])
        partner_detail = order.partner_id.read(['id', 'name', 'street', 'city', 'zip'])
        return {'details': order_detail, 'order': sale_detail, 'partner': partner_detail}
