# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

from . import checksum


class OwlController(http.Controller):

    @http.route('/shop', type='http', auth="public", csrf=False)
    def product_list(self, **post):
        return http.request.render("task_owl.product_list")

    @http.route('/get_product_data', type='json', auth="public", csrf=False)
    def get_product_data(self, **post):
        products = request.env['product.template'].sudo().search([])
        mylist = ['id', 'image_1920', 'name', 'type', 'list_price', 'active']
        return products.read(mylist)

    @http.route(['/shop/cart/update'], type='json', auth="public", website=True, csrf=False)
    def cart_update(self, **kw):
        product_id = request.env['product.product'].sudo().search([('product_tmpl_id', '=', int(kw['product_template_id']))])
        if not request.session.order_id:
            sale_order = request.env['sale.order'].sudo().create({
                'partner_id': request.env['res.users'].browse([request.session.uid]).partner_id.id,
                })
            request.session['order_id'] = sale_order.id
        else:
            sale_order = request.env['sale.order'].sudo().browse(int(request.session.order_id))
        request.env['sale.order.line'].sudo().create({
            'order_id': sale_order.id,
            'sale_order_id': sale_order.order_id,
            'product_id': product_id.id,
        })
        return len(sale_order.order_line)

    @http.route('/get_cart_detail', type='json', auth="public", csrf=False)
    def cart(self, **post):
        if request.session.order_id:
            sale_order = request.env['sale.order'].sudo().browse(int(request.session.order_id))
            product_details = ['name', 'product_id', 'price_unit', 'sale_order_id']
            return sale_order.order_line.read(product_details)
        return [{}]

    @http.route('/order', type='json', auth="public", csrf=False)
    def order(self, **post):
        if request.session.order_id:
            order = request.env['sale.order'].sudo().browse(int(request.session.order_id))
            order_details = ['amount_total']
            return order.read(order_details)
        return [{}]

    @http.route('/get_total_item', type='json', auth="public", csrf=False)
    def total_item_in_cart(self, **post):
        return len(request.env['sale.order'].sudo().browse(int(request.session.order_id)).order_line) if request.session.order_id else 0

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
