# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import werkzeug
from . import checksum
from datetime import datetime
from werkzeug import urls

from odoo import http, _
from odoo.addons.web.controllers.main import Home
from odoo.http import request
from odoo.exceptions import ValidationError


class Home(Home):
    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('task_cart_payment.group_manager'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('task_cart_payment.group_driver'):
            return '/my/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('task_cart_payment.group_customer'):
            return '/product_list/'
        return super(UserRegister, self)._login_redirect(uid, redirect=redirect)


class UserRegister(http.Controller):
    @http.route('/userregister/', auth="public", type="http")
    def customer_index1(self, **kw):
        currency = http.request.env['res.currency'].sudo().search([])
        return http.request.render('task_cart_payment.customer_index1', {'currency_ids': currency})

    @http.route('/my/', method="post", auth="public", type="http")
    def homepage(self, **post):
        return request.render('task_cart_payment.home_page', {'odometer_ids': request.env['fleet.odometer'].sudo().search([])})

    @http.route(['/product_list/'], type='http', auth="public", website=True, csrf=False)
    def product(self, page=1, date_begin=None, date_end=None, sortby=None, **post):
        product_template = request.env['product.template'].sudo().search([])
        return request.render("task_cart_payment.product_list", {"products": product_template})

    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['GET', 'POST'], website=True, csrf=False)
    def cart_update(self, add_qty=1, set_qty=0, **kw):
        product_id = request.env['product.template'].sudo().browse(int(kw['product_template_id']))
        print("--------------------request.session.order_id", request.session.order_id)
        if not request.session.order_id:

            slae_order = request.env['sale.order'].sudo().create({
                'partner_id': request.env['res.users'].browse([request.session.uid]).partner_id.id,
                'amount_total': product_id.list_price
                })
            print("--------------------in not orderid", slae_order.order_id)

            order = request.env['sale.order.line'].sudo().create({
                'order_id': slae_order.id,
                'sale_order_id': slae_order.order_id,
                'name': product_id.name,
                'product_id': product_id.id,
                'price_unit': product_id.list_price,
                'product_uom_qty': 1,
                })
            print("--------------------order.orderid", order.sale_order_id)

            request.session['order_id'] = order.sale_order_id
            request.session['slae_order_id'] = slae_order.id
            return werkzeug.utils.redirect("/cart/")
        else:
            order = request.env['sale.order'].sudo().browse(int(request.session.slae_order_id))
            order.write({
                'amount_total': product_id.list_price + order.amount_total
                })
            product_id = request.env['product.template'].sudo().browse(int(kw['product_template_id']))
            request.env['sale.order.line'].sudo().create({
                'order_id': order.id,
                'name': product_id.name,
                'product_id': product_id.id,
                'price_unit': product_id.list_price,
                'product_uom_qty': 1,
            })
            return werkzeug.utils.redirect("/cart/")

    @http.route('/confirm_order', method="post", auth="public", type="http", csrf=False)
    def confirm_booking(self, **post):
        # MID = amitgo59443067266036
        # Merchant Key= bQfzzkKzeCbR7jOl
        # Industry Type= Retail
        # Website Name = WEBSTAGING
        print(post.get('contract_id'), "***********", post.get('amount'))
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        merchant_id = request.env['ir.config_parameter'].sudo().get_param('sandbox_merchant_id')
        merchant_key = request.env['ir.config_parameter'].sudo().get_param('sandbox_merchant_key')
        data_dict = {
            'MID': merchant_id,
            'WEBSITE': 'WEBSTAGING',
            'ORDER_ID': post.get('contract_id'),
            'CUST_ID': str(request.uid),
            'INDUSTRY_TYPE_ID': 'Retail',
            'CHANNEL_ID': 'WEB',
            'TXN_AMOUNT': str(post.get('amount')),
            'CALLBACK_URL': urls.url_join(base_url, '/paytm_response')
        }
        print("data_dict------------", data_dict)
        data_dict['CHECKSUMHASH'] = checksum.generate_checksum(data_dict, merchant_key)
        data_dict['redirection_url'] = "https://securegw-stage.paytm.in/order/process"
        return request.make_response(json.dumps(data_dict))

    @http.route('/paytm_response', method="post", type="http", csrf=False)
    def paytm_response(self, **post):
        merchant_key = request.env['ir.config_parameter'].sudo().get_param('sandbox_merchant_key')
        checksum_status = checksum.verify_checksum(post, merchant_key, post.get('CHECKSUMHASH'))
        order_id = post.get('ORDERID')
        contract = request.env['fleet.vehicle.contract.booking'].sudo().search([('order_id', '=', order_id)])
        if checksum_status:
            today = datetime.today()
            payment_status = post.get('STATUS')
            if payment_status == 'TXN_SUCCESS':
                contract.write({'acquirer_ref': post.get('TXNID'), 'state': 'confirm', 'payment_status': 'success', 'payment_date': today})
            elif payment_status == 'TXN_FAILURE':
                contract.write({'acquirer_ref': post.get('TXNID'), 'state': 'draft', 'payment_status': 'fail', 'payment_date': today})
            elif payment_status == 'TXN_PENDING':
                contract.write({'acquirer_ref': post.get('TXNID'), 'state': 'draft', 'payment_status': 'pending', 'payment_date': today})
            else:
                raise ValidationError(_('For some reasion, There some error accure in payment process!'))
        return werkzeug.utils.redirect('/payment/process?order_id=%s' % (order_id))

    @http.route('/payment/process', method="post", type="http", csrf=False)
    def paytm_process(self, **post):
        request.session['order_id'] = None
        order_id = post.get('order_id')
        contract = request.env['sale.order'].sudo().search([('id', '=', order_id)])
        return request.render('task_cart_payment.payment_process', {'contract': contract})

    @http.route('/cart', method="post", type="http", csrf=False)
    def cart(self, **post):
        if request.session.order_id:
            return request.render('task_cart_payment.cart', {'sale_order_lines': request.env['sale.order.line'].sudo().search([]).filtered(lambda order_line: order_line.sale_order_id == request.session['order_id']),
                                  'order_id': request.env['sale.order'].sudo().browse(int(request.session.slae_order_id))})
        else:
            return request.render('task_cart_payment.cart', {'sale_order_lines': None})
