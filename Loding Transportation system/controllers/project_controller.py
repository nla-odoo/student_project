# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http, SUPERUSER_ID
from odoo.http import request
from odoo.addons.web.controllers.main import Home


class Home(Home):
    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('lts.group_transporter'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_portal'):
            return '/home'
        return super(Home, self)._login_redirect(uid, redirect=redirect)


class Lts(http.Controller):

    @http.route('/home', auth='public', type="http")
    def index(self, **kw):
        return http.request.render('lts.lts_index')

    @http.route('/customerregister/', auth="public", type="http", csrf=False)
    def Customer_Register(self, **kw):
        currency = http.request.env['res.currency'].sudo().search([])
        return http.request.render('lts.customerregister', {'currency': currency})

    @http.route('/customerregister/form', auth="public", type="http", csrf=False)
    def CustomerRegisterForm(self, **post):

        groups_id_name = [(6, 0, [request.env.ref('base.group_portal').id])]
        currency_name = post.get('Currency')
        request.env['res.currency'].sudo().search([('name', '=', currency_name)], limit=1)
        partner = request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'city': post.get('city'),
            'phone': post.get('cnumber'),
            'date': post.get('date'),
        })
        request.env['res.users'].sudo().create({
            'partner_id': partner.id,
            'login': post.get('name'),
            'password': post.get('password'),
            'groups_id': groups_id_name,
        })
        return http.local_redirect('/web/login?redirect=/home')

    @http.route(['/product/'], auth='public')
    def Products(self, **kw):
        products = http.request.env['product.template'].sudo().search([])
        return http.request.render('lts.lts_products', {'products': products})

    @http.route(['/customer_detail/'], auth='public')
    def customerdetails(self, **kw):
        details = http.request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        return http.request.render('lts.lts_customerdetails', {'details': details, })

    @http.route(['/inquirey/'], auth='public')
    def Inquirey(self, **kw):
        partner = request.env.user.partner_id
        return http.request.render('lts.lts_createinquirey', {'partner': partner})

    @http.route('/createinquirey/', auth='public', csrf=False, method='post')
    def CreateInquirey(self, tid=False, **post):
        if post:
            http.request.env['crm.lead'].with_user(SUPERUSER_ID).create({
                'description': post.get('description'),
                'partner_id': int(post.get('partner_id')),
                'name': post.get('name'),
                'user_id': False
                })
            return http.local_redirect('/yourinquirey/')

    @http.route(['/yourinquirey/'], auth='public')
    def YourInquirey(self, **kw):
        partner = request.env.user.partner_id
        inquiries = http.request.env['crm.lead'].sudo().search([('partner_id', '=', partner.id)])
        return http.request.render('lts.lts_displayinquires', {'inquiries': inquiries})
