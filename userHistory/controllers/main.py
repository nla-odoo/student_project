from odoo import http
from odoo.http import request
from datetime import datetime
from werkzeug import urls
from odoo.addons.web.controllers.main import Home


class Home(Home):

    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('rms.group_owner'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_portal'):
            return '/home'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
            return '/web/'
        return super(Tenants, self)._login_redirect(uid, redirect=redirect)


class Tenants(http.Controller):

    @http.route('/rms', auth='public', csrf=False, type="http")
    def tenants_details(self, **kw):
        currency = request.env["res.currency"].sudo().search([])
        return request.render('userHistory.rms_form', {'currency': currency})

    @http.route('/rms/form/', auth="public", type="http", method="post", csrf=False)
    def check(self, **post):
        if post.get('user') == 'Owner':
            groups_id_name = [(6, 0, [request.env.ref('rms.group_owner').id])]
            currency_name = post.get('currency')
            currency = request.env['res.currency'].sudo().search([('name', '=', currency_name)], limit=1)
            partner = request.env['res.partner'].sudo().create({
                'name': post.get('name'),
                'email': post.get('email')
            })

            company = request.env['res.company'].sudo().create({
                'name': post.get('companyname'),
                'partner_id': partner.id,
                'currency_id': currency.id,
            })

            request.env['res.users'].sudo().create({
                'partner_id': partner.id,
                'login': post.get('name'),
                'password': post.get('Password'),
                'company_id': company.id,
                'company_ids': [(4, company.id)],
                'groups_id': groups_id_name
            })
            return http.local_redirect('/web/login')
        else:
            groups_id_name = [(6, 0, [request.env.ref('base.group_portal').id])]
            currency_name = post.get('currency')
            currency = request.env['res.currency'].sudo().search([('name', '=', currency_name)], limit=1)
            partner = request.env['res.partner'].sudo().create({
                'name': post.get('name'),
                'email': post.get('email')
            })
            request.env['res.users'].sudo().create({
                'partner_id': partner.id,
                'login': post.get('name'),
                'password': post.get('Password'),
                'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])]
            })
            return http.local_redirect('/web/login?redirect=/rmshome')

    @http.route('/home/', method="post", auth='public', csrf=False)
    def index(self, s=None, **post):
        return request.render('userHistory.rms_index')
