# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class OwlController(http.Controller):

    @http.route('/search', type='http', auth="public")
    def owl_search_component(self, **post):
        return http.request.render("owl_search_component.template")

    @http.route('/get_product_data', type='json', auth="public", csrf=False)
    def get_product(self, offset=0, limit=0, order=None):

        request.env.cr.execute("""SELECT count(*) FROM product_template;""")
        count = request.env.cr.fetchone()[0] / 6
        if isinstance(count, (float)):
            count = int(count) + 1
        results = request.env['product.template'].sudo().search_read([], ['id', 'image_1920', 'name', 'type', 'list_price', 'active'], offset=offset, limit=limit, order=order)
        return {"results": results, 'count': count, 'order': order}
