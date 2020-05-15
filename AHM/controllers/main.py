# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
from . import checksum
import werkzeug
from datetime import datetime
from odoo import http, _
from odoo.http import request
from odoo.addons.web.controllers.main import Home
from odoo.exceptions import ValidationError
from werkzeug import urls


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
        dept_ids = request.env['res.company'].sudo().search([])
        return request.render('AHM.customer_index2', {'dept_ids': dept_ids})

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

            request.env['ahm.organization.registration'].sudo().create({'org_id': post.get('username'),
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
        org_id = request.env['ahm.organization.registration'].sudo().search([])
        p_ids = request.env['ahm.patient.detail'].sudo().search([('name', '=', request.session.login)])
        return request.render('AHM.appointment_index', {'animal_type': animal_type,
                                                        'org_id': org_id,
                                                        'patient_id': p_ids})

    @http.route('/appointment/confirm/', method="post", auth="public", website=True, type="http", csrf=False)
    def appointment_confirm(self, **post):
        appointments_id = request.env['ahm.appointment'].sudo().create({
                                    'breed_type_id': post.get('breed_type_id'),
                                    'org_id': int(post.get('org_name')),
                                    'name': post.get('name'),
                                    'contact': post.get('contact'),
                                    'patient_id': int(post.get('patient_id')),
                                    'visiting_date': post.get('visiting_date'),
                                    'visiting_time': post.get('visiting_time'),
                                    'visit_charges': int(post.get('visit_charges')),
                                    'address': post.get('address')})
        return request.render('AHM.portal_patient_payment', {'appointments_id': appointments_id})

    @http.route('/appointment/detail/', method="post", auth="public", website=True, type="http", csrf=False)
    def appointment_detail(self, **post):
        return request.render('AHM.patient_appointment_portal', {'appointments': request.env['ahm.appointment'].sudo().search([('create_uid', '=', request.session.uid)])})

    @http.route('/patientbill', method="post", auth="public", type="http", csrf=False)
    def patientbill(self, **post):
        p_id = request.env['ahm.patient.detail'].sudo().search([('name', '=', request.session.login)])
        app = request.env['ahm.appointment'].sudo().search([('patient_id', '=', p_id.id)])
        patientbills1 = request.env['ahm.total.charges'].sudo().search([('app_id', 'in', app.ids)])
        return request.render('AHM.patient_bill_index', {'patientbills': patientbills1})

    @http.route('/payment_confirm/', method="post", auth="public", website=True, type="http", csrf=False)
    def payment_confirm(self, **post):
        config_sudo = request.env['ir.config_parameter'].sudo()
        base_url = config_sudo.get_param('web.base.url')
        merchant_id = config_sudo.get_param('sandbox_merchant_id')
        # merchant_key = config_sudo.get_param('sandbox_merchant_key')
        appointment = request.env['ahm.appointment'].sudo().browse(int(post.get('appointments_id')))
        if not merchant_id:
            raise ValidationError(_('please fill value of [base url, merchant id, order id, merchant key]'))
        else:
            data_dict = {
               'MID': 'amitgo59443067266036',
               'WEBSITE': 'WEBSTAGING',
               'ORDER_ID': appointment.order_id,
               'CUST_ID': str(request.uid),
               'INDUSTRY_TYPE_ID': 'Retail',
               'CHANNEL_ID': 'WEB',
               'TXN_AMOUNT': str(float(post.get('visit_charges'))),
               'CALLBACK_URL': urls.url_join(base_url, '/paytm_response')}
            data_dict['CHECKSUMHASH'] = checksum.generate_checksum(data_dict, 'bQfzzkKzeCbR7jOl')
            data_dict['redirection_url'] = "https://securegw-stage.paytm.in/order/process"
            return request.make_response(json.dumps(data_dict))

    @http.route('/paytm_response/', method="post", auth="public", website=True, type="http", csrf=False)
    def paytm_response(self, **post):
        checksum_status = checksum.verify_checksum(post, 'bQfzzkKzeCbR7jOl', post.get('CHECKSUMHASH'))
        order_id = post.get('ORDERID')
        contract = request.env['ahm.appointment'].sudo().search([('order_id', '=', order_id)])
        if checksum_status:
            today = datetime.today()
            payment_status = post.get('STATUS')
            if payment_status == 'TXN_SUCCESS':
                contract.write({'acquirer_ref': post.get('TXNID'), 'status': 'confirm', 'payment_status': 'success', 'payment_date': today})
            elif payment_status == 'TXN_FAILURE':
                contract.write({'acquirer_ref': post.get('TXNID'), 'status': 'pending', 'payment_status': 'fail', 'payment_date': today})
            elif payment_status == 'TXN_PENDING':
                contract.write({'acquirer_ref': post.get('TXNID'), 'status': 'pending', 'payment_status': 'pending', 'payment_date': today})
            else:
                raise ValidationError(_('please fill value of [base url, merchant id, order id, merchant key]'))
            return werkzeug.utils.redirect('/paytm/process/?order_id=%s' % (order_id))

    @http.route('/paytm/process/', method="post", auth="public", website=True, type="http", csrf=False)
    def paytm_process(self, **post):
        order_id = post.get('order_id')
        contract = request.env['ahm.appointment'].sudo().search([('order_id', '=', order_id)])
        return request.render('AHM.paytm_process', {'contract': contract})

    @http.route('/user/complaint/', method="post", auth="public", website=True, type="http", csrf=False)
    def user_complaint(self, **post):
        return request.render('AHM.user_complaint')

    @http.route('/user/feedback/', method="post", auth="public", website=True, type="http", csrf=False)
    def user_feedback(self, **post):
        return request.render('AHM.user_feedback')

    @http.route('/user/rating/', method="post", auth="public", website=True, type="http", csrf=False)
    def user_rating(self, **post):
        return request.render('AHM.user_rating')
