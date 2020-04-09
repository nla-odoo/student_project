# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import http
from odoo.http import request


class Member(http.Controller):

    @http.route(['/society', '/web/signup'], auth="public", type="http", csrf=False)
    def society_register_form(self, **kw):
        currency = request.env['res.currency'].sudo().search([])
        return request.render('society_managment.society_form', {'currency': currency})

    @http.route(['/homepage', '/sub/<int:att>'], auth="user", type="http", csrf=False)
    def servicesForm(self, att=0):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        subscriptions = request.env['sale.subscription.template'].sudo().search([('company_id', '=', user.company_id.id)])
        attributes = request.env['product.attribute'].sudo().search([('create_uid', '=', request.session.uid)])
        if att != 0:
            values = request.env['product.attribute.value'].sudo().search([('attribute_id.id', '=', att)])
        else:
            values = []
        return request.render('society_managment.services_form', {'subscriptions': subscriptions, 'attributes': attributes, 'values': values, 'att': att})

    @http.route('/services/form', auth="user", type="http", csrf=False)
    def services_form(self, **post):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        print('\n\n\n\n\n\n\n\n\n\n\n', post.get('subscription_template_id'))
        request.env['product.product'].sudo().create([{
                    'name': post.get('name'),
                    'purchase_ok': post.get('purchase_ok'),
                    'sale_ok': post.get('sale_ok'),
                    'rent_ok': post.get('rent_ok'),
                    'type': post.get('type'),
                    'standard_price': post.get('standard_price'),
                    'list_price': post.get('list_price'),
                    'recurring_invoice': post.get('recurring_invoice'),
                    'subscription_template_id': post.get('subscription_template_id'),
                    'attribute_line_ids': [(6, 0, [post.get('attribute_line_ids')])],
                    'company_id': user.company_id.id
                    }])
        return http.local_redirect('/homepage')

    @http.route(['/subscription', '/sub/<int:att>'], auth="user", type="http", csrf=False)
    def subscriptionForm(self, att=0):
        emails_temp = request.env['mail.template'].sudo().search([])
        return request.render('society_managment.subscription_form', {'emails_temp': emails_temp})

    @http.route('/subscription/form', auth="user", type="http", csrf=False)
    def subscription_form(self, **post):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        request.env['sale.subscription.template'].sudo().create([{
                    'name': post.get('name'),
                    'recurring_interval': post.get('recurring_interval'),
                    'recurring_rule_type': post.get('recurring_rule_type'),
                    'recurring_rule_boundary': post.get('recurring_rule_boundary'),
                    'recurring_rule_count': post.get('recurring_rule_count'),
                    'payment_mode': post.get('payment_mode'),
                    'invoice_mail_template_id': post.get('invoice_mail_template_id'),
                    'user_closable': post.get('user_closable'),
                    'company_id': user.company_id.id
                    }])
        return http.local_redirect('/homepage')

    @http.route('/attribute', auth="user", type="http")
    def attributeForm(self):
        return request.render('society_managment.attribute_form')

    @http.route('/attribute/form', auth="user", type="http", csrf=False)
    def attribute_form(self, **post):
        attribute = request.env['product.attribute'].sudo().create([{
                    'name': post.get('name')
                    }])
        for i in range(int(post.get('dem'))):
            request.env['product.attribute.value'].sudo().create([{
                    'name': post.get('value_name{}'.format(i+1)),
                    'attribute_id': attribute.id
                    }])
        return http.local_redirect('/homepage')

    @http.route('/society/form/', auth="user", type="http", csrf=False)
    def society_register(self, **post):
        groups_id_name = [(6, 0, [request.env.ref('base.group_portal').id])]
        currency_code = post.get('currency')
        currency = request.env['res.currency'].sudo().search([('name', '=', currency_code)], limit=1)
        partner = request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email')
        })
        company = request.env['res.company'].sudo().create({
            'name': post.get('companyname'),
            'partner_id': partner.id,
            'currency_id': currency.id
        })
        request.env['res.users'].sudo().create({
            'partner_id': partner.id,
            'login': post.get('name'),
            'password': post.get('password'),
            'company_id': company.id,
            'company_ids': [(4, company.id)],
            'groups_id': groups_id_name
        })
        return http.local_redirect('/web/login')
