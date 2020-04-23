# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request


class Registration(http.Controller):
    @http.route(['/reg/', '/web/signup'], auth='public', type="http", csrf=False)
    def custmoer_register(self, **kw):
        currency = http.request.env['res.currency'].sudo().search([])
        state = http.request.env['res.country.state'].sudo().search([('country_id.code', "=", "IN")])
        return http.request.render('cmt.reg_user', {'currency': currency, 'state': state})

    @http.route('/reg/form/<string:user_type>', auth='public', type="http", csrf=False)
    def custmoer_register_form(self, user_type=None, **post):
        if user_type == "laboratory":
            groups_id_name = [(6, 0, [request.env.ref("base.group_portal").id])]
            currency_name = post.get('currency')
            currency = request.env['res.currency'].sudo().search([('name', '=', currency_name)], limit=1)
            state = request.env['res.country.state'].sudo().browse(int(post.get('labstate')))
            partner = request.env['res.partner'].sudo().create({
                'name': post.get('username'),
                'email': post.get('email'),
                'mobile': post.get('labcontact'),
                'street': post.get('addressline1'),
                'street2': post.get('addressline2'),
                'city': post.get('city'),
                'state_id': state.id,
                'zip': post.get('pincode'),
                'country_id': state.country_id.id
            })
            company = request.env['res.company'].sudo().create({
                'name': post.get('company'),
                'partner_id': partner.id,
                'currency_id': currency.id,
            })
            request.env['res.users'].sudo().create({
                'partner_id': partner.id,
                'login': post.get('username'),
                'password': post.get('password'),
                'company_id': company.id,
                'company_ids': [(4, company.id)],
                'groups_id': groups_id_name,
            })
        else:
            groups_id_name = [(6, 0, [request.env.ref('base.group_portal').id])]

            partner = request.env['res.partner'].sudo().create({
                'name': post.get('username'),
                'email': post.get('email')
            })
            usr = request.env['res.users'].sudo().create({
                'partner_id': partner.id,
                'login': post.get('username'),
                'password': post.get('password'),
                'groups_id': groups_id_name,
            })
            request.env['customer.detail'].sudo().create({
                'user_id': usr.id,
                'contact': post.get('contact'),
                'address': post.get('address'),
                'city': post.get('city'),
                'state_id': request.env['res.country.state'].sudo().browse([post.get('state')]).id,
                })
        return http.local_redirect('/web/login')
