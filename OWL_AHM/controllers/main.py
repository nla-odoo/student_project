# -*- coding: utf-8 -*-
import json
# import logging
# import werkzeug
# from datetime import datetime
from odoo import http
from odoo.http import request


class OwlController(http.Controller):
    @http.route('/owl_ahm', type='http', auth="public", csrf=False)
    def owl_ahm(self, **post):
        return http.request.render("OWL_AHM.owl_component")

    @http.route('/register', type='http', auth="public", csrf=False, website=True)
    def demo_AddStudent(self, **post):
        count = request.env.cr.fetchone()[0] / 6
        if isinstance(count, (float)):
            count = int(count) + 1
            results = request.env['OWL_AHM.regsitration].sudo().search_read([], ['name', 'email', 'passwd'], offset=offset, limit=limit, order=order)
        # return {"results": results, 'count': count, 'order': order}
            return http.request.render("OWL_AHM.regsitration")
