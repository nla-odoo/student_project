# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class OwlController(http.Controller):

    # item_count = 1
    # prouct_count = 0
    # item_dict = dict()

    @http.route('/owl_demo', type='http', auth="public", csrf=False, website=True)
    def owl_demo(self, **post):
        return http.request.render("owl_demo.demo_template")

    @http.route('/get_partner_data', type='json', auth="public", csrf=False, website=True)
    def get_partner(self, offset=0, limit=0):
        # product_list = []
        request.env.cr.execute("""SELECT count(*) FROM product_template;""")
        count = request.env.cr.fetchone()[0] / 6
        if isinstance(count, (float)):
            count = int(count) + 1
        return request.env['product.template'].sudo().search_read([], ['id', 'image_1920', 'name', 'type', 'list_price', 'active'], offset=offset, count=count, limit=limit, )
        # products = request.env['product.template'].sudo().search([], offset=offset, ,limit=limit)
        # for product in products:
        #     product_list.append({
        #         "id": product.id,
        #         "name": product.name,
        #         "price": product.list_price,
        #         "type": product.type,
        #         "image": product.image_1024
        #     })
        # return { "product_list": product_list , "count": count}
