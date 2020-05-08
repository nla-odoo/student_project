# -*- coding: utf-8 -*-
from odoo import http
# from odoo.http import request


class OwlController(http.Controller):
    @http.route('/owl_demo', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("OWL_DEMO.demo_template")


class OwlControllerComplain(http.Controller):
    @http.route('/owl_demo_complain', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("OWL_DEMO.demo_template_complain")


class OwlControllerFeedback(http.Controller):
    @http.route('/owl_demo_feedback', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("OWL_DEMO.demo_template_feedback")


class OwlControllerRating(http.Controller):
    @http.route('/owl_demo_rating', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("OWL_DEMO.demo_template_rating")
