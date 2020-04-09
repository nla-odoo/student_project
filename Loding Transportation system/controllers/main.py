# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.http import request
import json
from . import checksum
from werkzeug import urls
from datetime import datetime
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

    @http.route('/transporterregister/', auth="public", type="http")
    def Transporter_Register(self, **kw):
        currency = http.request.env['res.currency'].sudo().search([])
        return http.request.render('lts.transporteregister', {'currency': currency})

    @http.route('/transporterregister/form', auth="public", type="http", csrf=False)
    def Transporter_register_form(self, **post):
        groups_id_name = [(6, 0, [request.env.ref('lts.group_transporter').id])]
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
            'password': post.get('password'),
            'company_id': company.id,
            'company_ids': [(4, company.id)],
            'groups_id': groups_id_name,
        })
        return http.local_redirect('/web/login?redirect=/home')

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
        })
        request.env['res.users'].sudo().create({
            'partner_id': partner.id,
            'login': post.get('name'),
            'password': post.get('password'),
            'groups_id': groups_id_name,
        })
        return http.local_redirect('/web/login?redirect=/home')

    @http.route(['/transporters/'], auth='public')
    def TransporterForm(self, **kw):
        transporters = http.request.env['transporter.transporter'].sudo().search([])
        return http.request.render('lts.lts_transporters', {'transporters': transporters})

    @http.route(['/vehicles/<int:vid>'], auth='public')
    def VehiclesForm(self, vid=False, **kw):
        vehicles = http.request.env['vehicles.vehicles'].sudo().search([('company_id', '=', vid), ('available', '=', 'available')])
        return http.request.render('lts.lts_vehicles', {'vehicles': vehicles})

    @http.route(['/drivers/<int:did>'], auth='public')
    def DriversForm(self, did=False, **kw):
        drivers = http.request.env['drivers.drivers'].sudo().search([('company_id', '=', did), ('available', '=', 'available')])
        return http.request.render('lts.lts_drivers', {'drivers': drivers})

    @http.route(['/inquirey/<int:tid>'], auth='public')
    def Inquirey(self, tid=False, **kw):
        transporter = http.request.env['transporter.transporter'].sudo().search([('id', '=', tid)])
        vehicles = http.request.env['vehicles.vehicles'].sudo().search([('company_id', '=', transporter.company_id.id)])
        drivers = http.request.env['drivers.drivers'].sudo().search([('company_id', '=', transporter.company_id.id)])
        return http.request.render('lts.lts_createinquirey', {
                'vehicles': vehicles, 'tid': tid, 'drivers': drivers})

    @http.route('/getvehicle_details', auth="public", csrf=False)
    def vehicle_details(self, **kw):
        vehicle = request.env['vehicles.vehicles'].sudo().browse(int(kw.get('type')))
        result = {'vehicle_capacity': vehicle.vehicle_capacity, 'vehicle_speed': vehicle.vehicle_speed, 'vehicle_weight': vehicle.vehicle_weight}
        return request.make_response(json.dumps(result))

    @http.route('/createinquirey/<int:tid>', auth='public', csrf=False, method='post')
    def CreateInquirey(self, tid=False, **post):
        if post:
            transporters = http.request.env['transporter.transporter'].sudo().browse([(tid)])
            http.request.env['inquirey.inquirey.demo'].sudo().create({
                'source_add': post.get('source_add'),
                'desti_add': post.get('desti_add'),
                'distance': int(post.get('distance')),
                'duration': int(post.get('duration')),
                'weight': int(post.get('weight')),
                'driver_id': post.get('dname'),
                'vehicle_type': int(post.get('vehicle_type')),
                'date': post.get('date'),
                'company_id': transporters.company_id.id,
                })
        return http.local_redirect('/yourinquirey/')

    @http.route(['/yourinquirey/'], auth='public')
    def YourInquirey(self, vid=False, **kw):
        order = http.request.env['order.order'].sudo().search([])
        inquiries = http.request.env['inquirey.inquirey.demo'].sudo().search([('create_uid', '=', request.session.uid)])
        return http.request.render('lts.lts_displayinquires', {'inquiries': inquiries, 'order': order})

    @http.route('/paycharge/<int:order_id>', type="http", csrf=False)
    def paycharge(self, order_id=None, **kw):
        order = http.request.env['order.order'].sudo().browse([order_id])
        return http.request.render('lts.lts_paycharge', {'order': order})

    @http.route('/payment', auth='public', type="http", csrf=False)
    def payment(self, **kw):
        orderid = http.request.env['order.order'].sudo().browse([int(kw.get('order_id'))])
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        config = request.env['res.config.settings'].sudo().search([])
        data_dict = {
            'MID': config.merchant_id,
            'WEBSITE': 'WEBSTAGING',
            'ORDER_ID': str(orderid.order_ref),
            'CUST_ID': str(request.uid),
            'INDUSTRY_TYPE_ID': 'Retail',
            'CHANNEL_ID': 'WEB',
            'TXN_AMOUNT': str(orderid.amount),
            'CALLBACK_URL': urls.url_join(base_url, '/payment_response')
        }
        data_dict['CHECKSUMHASH'] = checksum.generate_checksum(data_dict, config.merchant_key)
        data_dict['redirection_url'] = 'https://securegw-stage.paytm.in/order/process'
        return request.make_response(json.dumps(data_dict))

    @http.route('/payment_response', type="http", csrf=False)
    def payment_response(self, **kw):
        payment_date = datetime.today()
        order_payment = request.env['order.order'].sudo().search([('order_ref', '=', kw.get('ORDERID'))], limit=1)
        if(kw.get('STATUS') == 'TXN`_SUCCESS'):
            order_payment.sudo().write({'acquirer_ref': kw.get('TXNID'), 'payment_state': 'done', 'payment_date': payment_date})
            return request.render("lts.payment_done")

        if(kw.get('STATUS') == 'TXN_FAILURE'):
            order_payment.sudo().write({'payment_state': 'fail', 'payment_date': payment_date})
            return request.render("lts.payment_fail")
