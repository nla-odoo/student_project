# -*- coding: utf-8 -*-
from odoo import http


class OwlController(http.Controller):
    @http.route('/owl_work', type='http', auth='public', csrf=False, website=True)
    def owl_work(self, **post):
        return http.request.render("owl_work.btn_template")
