from odoo import http
from odoo.http import request


class Tenants(http.Controller):

    @http.route('/home', auth='public', type="http")
    def tenants_demo(self, **kw):
        return request.render('userHistory.demo, {}')

    @http.route('/saleorder', auth='public', csrf=False, type="http")
    def tenants_details(self, **kw):
        user_id = request.env.user.partner_id
        print("\n\n\n\n\n address", user_id.name)
        SaleOrder = request.env['sale.order']
        domain = [
            ('partner_id', '=', user_id.id),
            ('state', 'in', ['sale', 'done'])
        ]
        order = SaleOrder.sudo().search(domain)
        print("\n\n\n\n\n order", order)
        return request.render('userHistory.sale_order_lines', {'orders': order})

    @http.route('/saleorder/detail/<int:saleid>', auth='public', csrf=False, type="http")
    def order_details(self, saleid=None):
        SaleOrder = request.env['sale.order'].sudo().search([('id', '=', saleid)])
        sale = SaleOrder.id
        print("\n\n\n user", sale)
        user_id = request.env.user.partner_id
        details = request.env['sale.order.line'].sudo().search([('order_id', '=', SaleOrder.id)])
        print("\n\n\n", details)
        return request.render('userHistory.sale_order_details', {'details': details, 'order': SaleOrder, 'partner': user_id})
