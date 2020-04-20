# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.http import request


class UserRegister(http.Controller):
    @http.route('/my/', method="post", auth="public", type="http")
    def homepage(self, **post):
        return request.render('task_owl.home')
