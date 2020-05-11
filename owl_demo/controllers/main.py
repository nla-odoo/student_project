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
        # SaleOrder = request.env['sale.order']
        domain = [
            ('partner_id', '=', user_id.id),
            ('state', 'in', ['sale', 'done'])
        ]
        orders = request.env['sale.order'].sudo().search(domain)
        print("\n\n\n\n order", orders)
        hh = orders.read(['id', 'name', 'date_order', 'amount_total'])
        print("\n\n\n\n hh", hh)
        return orders.read(['id', 'name', 'date_order', 'amount_total'])
        # return request.env['sale.order'].search([]).mapped('name')

    @http.route('/get_order_detail', type='json', auth="public", csrf=False)
    def get_data(self, **kw):

        details = request.env['sale.order.line'].sudo().browse(int(kw['order_id']))
        order_detail = details.read(['id', 'name', 'price_unit', 'price_tax', 'price_total', 'product_uom_qty'])
        print("\n\n\n\n", order_detail)
        request.session['detail_id'] = details.id

    @http.route('/get_data/', type='http', auth="public", csrf=False)
    def owl_details(self, **post):
        return http.request.render("owl_demo.detail_template")

    @http.route('/order_detail', type='json', auth="public", csrf=False)
    def order_data(self, **kw):
        user_id = request.env.user.partner_id
        print("\n\n partner", request.session.detail_id)
        session_id = request.session.detail_id
        details = request.env['sale.order.line'].sudo().search([('order_id', '=', session_id)])
        order = request.env['sale.order'].sudo().search([('id', '=', request.session.detail_id)])
        partner = request.env['res.partner'].sudo().search([('id', '=', request.env.user.partner_id.id)])
        print("\n\n partner", partner.name)
        order_detail = details.read(['id', 'name', 'price_unit', 'price_tax', 'price_total', 'product_uom_qty'])
        sale_detail = order.read(['name', 'date_order'])
        partner_detail = partner.read(['id', 'name', 'street', 'city', 'zip'])
        print("\n\n\n\n sale", order_detail)
        return {'details': order_detail, 'order': sale_detail, 'partner': partner_detail}
