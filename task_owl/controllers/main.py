# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import werkzeug
from werkzeug import urls
from . import checksum
import json

class OwlController(http.Controller):

    @http.route('/product_list', type='http', auth="public", csrf=False)
    def product_list(self, **post):
        return http.request.render("task_owl.product_list")

    @http.route('/get_product_data', type='json', auth="public", csrf=False)
    def get_product_data(self, **post):
        products = request.env['product.template'].sudo().search([])
        mylist = ['id', 'image_1920', 'name', 'type', 'list_price', 'active']
        return products.read(mylist)

    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['GET', 'POST'], website=True, csrf=False)
    def cart_update(self, add_qty=1, set_qty=0, **kw):
        print("kw******************", kw)
        product_tmplet_id = request.env['product.template'].sudo().browse(int(kw['product_template_id']))
        product_id = request.env['product.product'].sudo().search([('product_tmpl_id', '=', product_tmplet_id.id)])
        print("--------------------product_tmplet_id", product_tmplet_id.id)
        print("product_id=", product_id)
        if not request.session.order_id:

            slae_order = request.env['sale.order'].sudo().create({
                'partner_id': request.env['res.users'].browse([request.session.uid]).partner_id.id,
                'amount_total': product_id.list_price
                })
            print("if order does not exist--------------------in not orderid", slae_order.order_id)

            order = request.env['sale.order.line'].sudo().create({
                'order_id': slae_order.id,
                'sale_order_id': slae_order.order_id,
                'name': product_tmplet_id.name,
                'product_id': product_id.id,
                'price_unit': product_tmplet_id.list_price,
                'product_uom_qty': 1,
                })
            print("--------------------order.orderid", order.sale_order_id)

            request.session['order_id'] = order.sale_order_id
            request.session['slae_order_id'] = slae_order.id
            return werkzeug.utils.redirect("/display_cart/")
            # sale_order_lines = request.env['sale.order.line'].sudo().search([]).filtered(lambda order_line: order_line.sale_order_id == request.session['order_id'])
            # print(len(sale_order_lines))
            # return len(sale_order_lines)
            # return
        else:

            order = request.env['sale.order'].sudo().browse(int(request.session.slae_order_id))
            order.write({
                'amount_total': product_tmplet_id.list_price + order.amount_total
                })
            # product_id = request.env['product.template'].sudo().browse(int(kw['product_template_id']))
            print("if order exist--------------------in order")
            request.env['sale.order.line'].sudo().create({
                'order_id': order.id,
                'sale_order_id': order.order_id,
                'name': product_tmplet_id.name,
                'product_id': product_id.id,
                'price_unit': product_tmplet_id.list_price,
                'product_uom_qty': 1,
            })
            # return 0
            return werkzeug.utils.redirect("/display_cart/")

    @http.route('/get_cart_detail', type='json', auth="public", csrf=False)
    def cart(self, **post):
        print("in cart")
        if request.session.order_id:
            sale_order_lines = request.env['sale.order.line'].sudo().search([]).filtered(lambda order_line: order_line.sale_order_id == request.session['order_id'])
            product_details = ['name', 'product_id', 'price_unit', 'sale_order_id']
            print(sale_order_lines.read(['name']))
            return sale_order_lines.read(product_details)
            # return request.render('task_cart_payment.cart', {'sale_order_lines': request.env['sale.order.line'].sudo().search([]).filtered(lambda order_line: order_line.sale_order_id == request.session['order_id']),
            #                       'order_id': request.env['sale.order'].sudo().browse(int(request.session.slae_order_id))})
        else:
            return [{}]
            # return request.render('task_cart_payment.cart', {'sale_order_lines': None})

    @http.route('/order', type='json', auth="public", csrf=False)
    def order(self, **post):
        if request.session.order_id:
            order = request.env['sale.order'].sudo().browse(int(request.session.slae_order_id))
            order_details = ['amount_total']
            return order.read(order_details)
        else:
            return [{}]

    @http.route('/display_cart/', type='http', auth="public", csrf=False)
    def display_cart(self, **post):
        return http.request.render("task_owl.cart")

    @http.route('/get_total_item', type='json', auth="public", csrf=False)
    def total_item_in_cart(self, **post):
        print("asdxasasasc===========================")
        # return 1
        if request.session.order_id:
            sale_order_lines = request.env['sale.order.line'].sudo().search([]).filtered(lambda order_line: order_line.sale_order_id == request.session['order_id'])
            print(len(sale_order_lines))
            return len(sale_order_lines)
        else:
            return 0

    @http.route('/confirm_order', method="post", auth="public", type="http", csrf=False)
    def confirm_booking(self, **post):
        # MID = amitgo59443067266036
        # Merchant Key= bQfzzkKzeCbR7jOl
        # Industry Type= Retail
        # Website Name = WEBSTAGING

        print("adbsdkjask==============================")
        # print(post.get('contract_id'), "***********", post.get('amount'))
        # base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # merchant_id = request.env['ir.config_parameter'].sudo().get_param('sandbox_merchant_id')
        # merchant_key = request.env['ir.config_parameter'].sudo().get_param('sandbox_merchant_key')
        # data_dict = {
        #     'MID': merchant_id,
        #     'WEBSITE': 'WEBSTAGING',
        #     'ORDER_ID': post.get('contract_id'),
        #     'CUST_ID': str(request.uid),
        #     'INDUSTRY_TYPE_ID': 'Retail',
        #     'CHANNEL_ID': 'WEB',
        #     'TXN_AMOUNT': str(post.get('amount')),
        #     'CALLBACK_URL': urls.url_join(base_url, '/paytm_response')
        # }
        # print("data_dict------------", data_dict)
        # data_dict['CHECKSUMHASH'] = checksum.generate_checksum(data_dict, merchant_key)
        # data_dict['redirection_url'] = "https://securegw-stage.paytm.in/order/process"
        # return request.make_response(json.dumps(data_dict))