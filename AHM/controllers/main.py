# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home


class Home(Home):
    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('AHM.group_manager'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_portal'):
            return '/my/home'
        return super(UserRegister, self)._login_redirect(uid, redirect=redirect)


class UserRegister(http.Controller):
    @http.route('/userregister/', auth="public", type="http", csrf=False)
    def customer_index1(self, **kw):
        currency = http.request.env['res.currency'].sudo().search([])
        return http.request.render('AHM.customer_index1', {'currency': currency})

    @http.route('/my/home', method="post", auth="user", type="http", csrf=False)
    def homepage(self, **post):
        hospital_detail = request.env['res.company'].sudo().search([])
        return request.render('AHM.customer_index2', {'hospital_detail': hospital_detail})

    @http.route('/registration/<string:user>', method="post", auth="public", type="http", csrf=False)
    def service_provider_index1(self, user=None, **post):
        if user == 'hospital':
            groups_id_name = [(6, 0, [request.env.ref('AHM.group_manager').id])]
            currency_name = post.get('currency')
            currency = request.env['res.currency'].sudo().search([('name', '=', currency_name)], limit=1)

            partner = request.env['res.partner'].sudo().create({'name': post.get('username'),
                                                                'email': post.get('email')})

            company = request.env['res.company'].sudo().create({'name': post.get('username'),
                                                                'partner_id': partner.id,
                                                                'currency_id': currency.id})

            request.env['res.users'].sudo().create({'partner_id': partner.id,
                                                    'login': post.get('username'),
                                                    'password': post.get('password'),
                                                    'company_id': company.id,
                                                    'company_ids': [(4, company.id)],
                                                    'groups_id': groups_id_name})

            request.env['ahm.organization.registration'].sudo().create({'org_name': post.get('username'),
                                                                        'email': post.get('email')})
        else:

            groups_id_name = [(6, 0, [request.env.ref('base.group_portal').id])]
            partner = request.env['res.partner'].sudo().create({'name': post.get('username'),
                                                                'email': post.get('email')})
            request.env['res.users'].sudo().create({'partner_id': partner.id,
                                                    'login': post.get('username'),
                                                    'password': post.get('password'),
                                                    'groups_id': groups_id_name})

            request.env['ahm.patient.detail'].sudo().create({'name': post.get('username'),
                                                            'email': post.get('email')})
        return http.local_redirect('/web/login?redirect=/homepage')

    @http.route('/appointment', method="post", auth="public", type="http", csrf=False)
    def appointment(self, **post):
        animal_type = request.env['ahm.animal.type'].sudo().search([])
        org_name = request.env['ahm.organization.registration'].sudo().search([])
        p_id = request.env['ahm.patient.detail'].sudo().search([('name', '=', request.session.login)])
        return request.render('AHM.appointment_index', {'animal_type': animal_type,
                                                        'org_name': org_name,
                                                        'patient_id': p_id})

    @http.route('/appointment/confirm/', method="post", auth="public", website=True, type="http", csrf=False)
    def appointment_confirm(self, **post):
        appointments = request.env['ahm.appointment']
        appointments.sudo().create({'b_type': post.get('b_type'),
                                    'hospital_name': post.get('org_name'),
                                    'name': post.get('name'),
                                    'contact': post.get('contact'),
                                    'patient_id': int(post.get('patient_id')),
                                    'visiting_date': post.get('visiting_date'),
                                    'visiting_time': post.get('visiting_time'),
                                    'visit_charges': post.get('visit_charges'),
                                    'address': post.get('address')})
        return request.redirect('/appointment')

    @http.route('/patientbill', method="post", auth="public", type="http", csrf=False)
    def patientbill(self, **kw):
        p_id = request.env['ahm.patient.detail'].sudo().search([('name', '=', request.session.login)])
        app = request.env['ahm.appointment'].sudo().search([('patient_id', '=', p_id.id)])
        patientbills1 = request.env['ahm.total.charges'].sudo().search([('app_id', 'in', app.ids)])
        return request.render('AHM.patient_bill_index', {'patientbills': patientbills1})
