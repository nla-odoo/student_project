# import json
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class StudentDetails(CustomerPortal):

    item_count = 1
    prouct_count = 0
    item_dict = dict()

    @http.route(['/cource/', '/cource/<int:offset>'], type='http', offset=0, auth="public", website=True, csrf=False)
    def product(self, page=1, offset=0, date_begin=None, date_end=None, sortby=None, **post):
        product_templates = None
        if not len(self.item_dict):
            item_value = list()
            products = request.env['product.template'].sudo().search([])
            print("\n\n\n\n\n", products)
            for product in products:
                if self.prouct_count < 10:
                    item_value.append(product)
                    self.prouct_count += 1
                    if product.name == products[-1].name:
                        self.item_dict[str(self.item_count)] = item_value
                        self.item_count = 0
                        self.prouct_count = 0
                else:
                    self.item_dict[str(self.item_count)] = item_value
                    item_value = []
                    self.item_count += 1
                    self.prouct_count = 1
                    item_value.append(product)
            product_templates = self.item_dict.get('1')
        else:
            product_templates = self.item_dict.get(str(offset), self.item_dict['1'])
        return {"product_templates": product_templates,
                'offsets': len(self.item_dict.keys())
                }
