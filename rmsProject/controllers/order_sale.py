import json

from odoo import http
from odoo.http import request
from datetime import datetime
from . import checksum
from werkzeug import urls


class Tenants(http.Controller):

    @http.route('/my/home', auth='public', type="http")
    def tenants_demo(self, **kw):
        return request.render('rms.demo, {}')

    @http.route('/saleorder', auth='public', csrf=False, type="http")
    def tenants_details(self, **kw):
        user_id = request.env.user.partner_id
        print("\n\n\n\n\n", user_id.street)
        SaleOrder = request.env['sale.order']

        domain = [
            ('partner_id', '=', user_id.id),
            ('state', 'in', ['sale', 'done'])
        ]
        order = SaleOrder.search(domain)
        print("\n\n\n\n\n", order)
        return request.render('rms.sale_order_lines', {'orders': order})

    @http.route('/saleorder/detail/<model("sale.order"):saleid>', auth='public', csrf=False, type="http")
    def order_details(self, saleid=None):
        user_id = request.env.user.partner_id
        details = request.env['sale.order.line'].search([('order_id', '=', saleid.id)])
        return request.render('rms.sale_order_details', {'details': details, 'order': saleid, 'partner': user_id})
