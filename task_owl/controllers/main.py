# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.http import request
import werkzeug


class UserRegister(http.Controller):

    @http.route('/home/', method="post", auth="public", type="http")
    def homepage1(self, **post):
        return request.render('task_owl.abc')
