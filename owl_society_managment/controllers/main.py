# -*- coding: utf-8 -*-
from datetime import date

from odoo import http
from odoo.http import request
import json
import base64


class OwlController(http.Controller):

    @http.route('/owl_demo', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("owl_society_managment.demo_template")

    @http.route('/society_create', type='http', auth="public", csrf=False)
    def society_form(self, **post):
        return http.request.render("owl_society_managment.society_form")

    @http.route('/member_create', type='http', auth="public", csrf=False)
    def member_register(self, **post):
        return http.request.render("owl_society_managment.member_register")

    @http.route('/complaint_create', type='http', auth="public", csrf=False)
    def complaint_register(self, **post):
        return http.request.render("owl_society_managment.complaint_register")

    @http.route('/event_create', type='http', auth="public", csrf=False)
    def event_register(self, **post):
        return http.request.render("owl_society_managment.event_register")

    @http.route('/balance_create', type='http', auth="public", csrf=False)
    def balance_register(self, **post):
        return http.request.render("owl_society_managment.balance_register")

    @http.route('/jounral_create', type='http', auth="public", csrf=False)
    def jounral_register(self, **post):
        return http.request.render("owl_society_managment.jounral_register")

    @http.route('/account_create', type='http', auth="public", csrf=False)
    def account_register(self, **post):
        return http.request.render("owl_society_managment.account_register")

    @http.route('/society', auth="public", type="json", csrf=False)
    def society_register_form(self, **kw):
        currencys = request.env['res.currency'].sudo().search_read([], ['id', 'name'])
        print('\n\n\n\n\n\n 111111', currencys)
        return currencys

    @http.route('/society/form/', auth="public", type="json", csrf=False)
    def society_register(self, **post):
        print('\n\n\n\n\n\n\n\n', post)
        groups_id_name = [(6, 0, [request.env.ref('base.group_portal').id])]
        currency_code = post.get('currency')
        currency = request.env['res.currency'].sudo().search([('id', '=', currency_code)], limit=1)
        partner = request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'commercial_company_name': post.get('name')
        })
        company = request.env['res.company'].sudo().create({
            'name': post.get('name'),
            'partner_id': partner.id,
            'currency_id': currency.id
        })
        request.env['res.users'].sudo().create({
            'partner_id': partner.id,
            'login': post.get('email'),
            'password': post.get('name'),
            'company_id': company.id,
            'company_ids': [(4, company.id)],
            'groups_id': groups_id_name
        })
        return http.local_redirect('/web/login')

    @http.route('/member/form', auth="user", type="json", csrf=False)
    def member_form(self, **kw):
        u = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        print('\n\n\n\n\n\n\n\n33333333', u)
        print('\n\n\n\n\n\n\n\n44444444', kw)
        groups_id_name = [(6, 0, [request.env.ref('base.group_portal').id])]
        partner = request.env['res.partner'].sudo().create({
            'name': kw.get('name'),
            'email': kw.get('email')
        })
        user = request.env['res.users'].sudo().create({
            'partner_id': partner.id,
            'login': kw.get('email'),
            'password': kw.get('name'),
            'groups_id': groups_id_name
        })
        return {"user": user}

    @http.route('/get_Product_data', auth="user", type="json", csrf=False)
    def get_product(self, **post):
        subscriptions = request.env['sale.subscription.template'].sudo().search_read([], ['id', 'name'])
        print('\n\n\n\n\n\n 111111', subscriptions)
        return subscriptions

    @http.route('/services/form', auth="user", type="json", csrf=False)
    def services_form(self, **kw):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        print('\n\n\n\n\n\n\n\n', kw)
        # file = open(kw.get('image_1920'), 'rb')base64.encodestring(file.read()),base64.encodebytes
        # print('\n\n\n\n\n\n\n\n22222', file)
        prod = request.env['product.template'].sudo().create([{
                    'name': kw.get('name'),
                    'purchase_ok': kw.get('purchase_ok'),
                    'sale_ok': kw.get('sale_ok'),
                    'rent_ok': kw.get('rent_ok'),
                    'type': kw.get('type'),
                    'standard_price': kw.get('standard_price'),
                    'list_price': kw.get('list_price'),
                    'image_1920': base64.encodebytes(kw.get('image_1920')),
                    'company_id': user.company_id.id
                    }])
        print('\n\n\n\n\n\n\n\n\n50000', prod.id)
        request.env['rental.pricing'].sudo().create([{
                    'duration': kw.get('duration'),
                    'unit': kw.get('unit'),
                    'price': kw.get('price'),
                    'product_template_id': prod.id,
                    }])
        # return http.request.render("owl_society_managment.demo_template")
        # return http.local_redirect('/owl_demo')
        return {"prod": prod}

    @http.route('/complaint/form', auth="user", type="json", csrf=False)
    def complaint_form(self, **kw):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        request.env['helpdesk.ticket'].sudo().create([{
                'name': kw.get('name'),
                'partner_name': user.partner_id.name,
                'partner_email': user.partner_id.email,
                'company_id': user.company_id.id
                }])
        # return http.request.render("owl_society_managment.demo_template")
        return http.local_redirect('/owl_demo')
        # return {"am": am}

    @http.route('/event/form', auth="user", type="json", csrf=False)
    def event_form(self, **kw):
        events = request.env['event.event'].sudo().search([('company_id', '=', request.session.uid)])

        def deactive(self):
            record = self.env['event.event'].sudo().search([])
            for i in record:
                if i.date_end < date.today():
                    i.active = False
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        print('\n\n\n\n\n\n\n000000', kw)
        request.env['event.event'].sudo().create([{
                'name': kw.get('name'),
                'date_begin': kw.get('date_begin'),
                'date_end': kw.get('date_end'),
                'date_tz':  'Asia/Kolkata',
                'note': kw.get('note'),
                'company_id': user.company_id.id
                }])
        # return http.request.render("owl_society_managment.demo_template")
        return events
        # return {"am": am}

    @http.route('/get_Parnter_data', auth="user", type="json", csrf=False)
    def get_partner(self, **post):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        partners = request.env['res.partner'].sudo().search_read([('create_uid', '=', user.id)], ['id', 'name'])
        accounts = request.env['account.account'].sudo().search_read([('create_uid', '=', user.id)], ['id', 'name'])
        jounrals = request.env['account.journal'].sudo().search_read([('create_uid', '=', user.id)], ['id', 'name'])
        return (partners, accounts, jounrals)

    @http.route('/balance/form', auth="user", type="json", csrf=False)
    def balance_form(self, **kw):
        print('\n\n\n\n\n\n\n000000', kw)
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        # partners = request.env['res.partner'].sudo().search([('id', '=', kw.get('partner_id'))])
        # print('\n\n\n\n\n\n\n\n222222222', partners.id)
        # accounts = request.env['account.account'].sudo().search([('id', '=', kw.get('destination_account_id'))])
        # print('\n\n\n\n\n\n\n\n55555555555555', accounts.id)
        # method = request.env['account.payment.method'].sudo().search([('payment_type', '=', kw.get('payment_type'))], limit=1)
        # print('\n\n\n\n\n\n\n\n\n\n\n111111', method.id)
        vals = {
                'move_type': 'entry',
                'journal_id': int(kw.get('journal_id')),
                'partner_id': int(kw.get('partner_id')),
                'company_id': user.company_id.id,
        }
        print('\n\n\n\n\n\n 88888888888', vals)
        move = request.env['account.move'].sudo().create([{
                'move_type': 'entry',
                'journal_id': int(kw.get('journal_id')),
                'partner_id': int(kw.get('partner_id')),
                'company_id': user.company_id.id,
            }])
        print('\n\n\n\n\n\n\n\n\n\n\n\n777777', move.id)
        # payment = request.env['account.payment'].sudo().create([{
        #         'move_id': move.id,
        #         'payment_type': kw.get('payment_type'),
        #         'partner_type': kw.get('partner_type'),
        #         'amount': kw.get('amount'),
        #         'partner_id': partners.id,
        #         'date': date.today(),
        #         'destination_account_id': accounts.id,
        #         'payment_method_id': method.id,
        #         }])
        # print('\n\n\n\n\n\n\n\n\n\n4444444', payment)
        # return http.request.render("owl_society_managment.demo_template")
        return http.local_redirect('/owl_demo')

    @http.route('/jounral/form', auth="user", type="json", csrf=False)
    def jounral_form(self, **kw):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        request.env['account.journal'].sudo().create([{
                'name': kw.get('name'),
                'type': kw.get('type'),
                'code': kw.get('code'),
                'company_id': user.company_id.id
                }])
        # return http.request.render("owl_society_managment.demo_template")
        return http.local_redirect('/owl_demo')

    @http.route('/get_account_data', auth="user", type="json", csrf=False)
    def get_account_data(self, **post):
        accounts = request.env['account.account.type'].sudo().search([]).mapped('name')
        return accounts

    @http.route('/account/form', auth="user", type="json", csrf=False)
    def account_form(self, **kw):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        accounts = request.env['account.account.type'].sudo().search([('name', '=', kw.get('user_type_id'))])
        print('\n\n\n\n\n\n\n\n\n', accounts)
        request.env['account.account'].sudo().create([{
                'name': kw.get('name'),
                'user_type_id': accounts.id,
                'code': kw.get('code'),
                'company_id': user.company_id.id
                }])
        # return http.request.render("owl_society_managment.demo_template")
        return http.local_redirect('/owl_demo')
