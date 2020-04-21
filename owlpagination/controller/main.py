from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class StudentDetails(CustomerPortal):

    @http.route('/cource/', type='http', offset=0, auth="public", website=True, csrf=False)
    def product(self, page=1, offset=0, date_begin=None, date_end=None, sortby=None, **post):
        return request.render("owlpagination.cource")
