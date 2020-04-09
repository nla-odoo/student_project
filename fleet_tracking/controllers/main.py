# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import werkzeug
from . import checksum
from datetime import datetime
from werkzeug import urls

from odoo import http, _
from odoo.addons.web.controllers.main import Home
from odoo.http import request
from odoo.exceptions import ValidationError


class Home(Home):
    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('fleet_tracking.group_manager'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('fleet_tracking.group_driver'):
            return '/my/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('fleet_tracking.group_customer'):
            return '/product_list/'
        return super(UserRegister, self)._login_redirect(uid, redirect=redirect)


class UserRegister(http.Controller):
    @http.route('/userregister/', auth="public", type="http")
    def customer_index1(self, **kw):
        currency = http.request.env['res.currency'].sudo().search([])
        return http.request.render('fleet_tracking.customer_index1', {'currency_ids': currency})

    @http.route('/my/', method="post", auth="user", type="http")
    def homepage(self, **post):
        return request.render('fleet_tracking.home_page', {'odometer_ids': request.env['fleet.odometer'].sudo().search([])})

    @http.route('/odometer/', method="post", auth="user", type="http")
    def odometer(self, **post):
        return request.render('fleet_tracking.odometer', {'vehicle_ids': request.env['fleet.vehicle'].sudo().search([]),
                                                          'driver_ids': request.env['res.users'].search([])})

    @http.route('/save/odometer/', method="post", auth="user", type="http", csrf=False)
    def create_update(self, **post):
        request.env['fleet.odometer'].create({'vehicle_id': int(post.get('vehicle')),
                                              'driver_id': request.session.uid,
                                              'date': post.get('date'),
                                              'odometer_reading': post.get('reading'),
                                              'reading_unit': post.get('unit')})
        return werkzeug.utils.redirect('/odometer/')

    @http.route('/map/', method="post", auth="user", type="http")
    def map(self, **post):
        return request.render('fleet_tracking.map_maker')

    @http.route('/trip_address/', method="post", auth="user", type="http")
    def trip_address(self, **post):
        return request.render('fleet_tracking.trip_address')

    @http.route('/contract/', method="post", auth="user", type="http", csrf=False)
    def booking(self, **post):
        if post.get('submit') == 'find_vehicle':
            booking_ids = request.env['fleet.vehicle.contract.booking'].search(['&', ('state', '!=', 'cancelled'), '|', '&', ('start_date', '<=', post.get('start_date')), ('end_date', '>=', post.get('start_date')),
                                                                                '&', ('start_date', '<=', post.get('end_date')), ('end_date', '>=', post.get('end_date'))])

            booking_renew_ids = request.env['fleet.contract.renew'].search(['&', ('state', '!=', 'cancelled'), '|', '&', ('start_date', '<=', post.get('start_date')), ('end_date', '>=', post.get('start_date')),
                                                                            '&', ('start_date', '<=', post.get('end_date')), ('end_date', '>=', post.get('end_date'))])

            vehicle_list = booking_ids.filtered(lambda con: con.state in ['confirm', 'running']).mapped('vehicle_ids.id')
            vehicle_list += booking_renew_ids.filtered(lambda con: con.state in ['confirm', 'running']).mapped('vehicle_ids.id')

            vehicle_ids = request.env['fleet.vehicle'].search([('id', 'not in', vehicle_list)])
            return request.render('fleet_tracking.contract_booking', {'vehicle_ids': vehicle_ids,
                                                                      'start_date': post.get('start_date'),
                                                                      'end_date': post.get('end_date')})
        elif post.get('submit') == 'next':
            contract_record = request.env['fleet.vehicle.contract.booking'].create({'customer_id': request.session.uid,
                                                                                    'vehicle_ids': [int(post.get('vehicle_id'))],
                                                                                    'start_date': post.get('start_date'),
                                                                                    'end_date': post.get('end_date'),
                                                                                    'state': 'draft'})
            return request.render('fleet_tracking.payment', {'contract_record': contract_record})
        else:
            return request.render('fleet_tracking.contract_booking')

    @http.route('/registration/<string:user>', method="post", auth="public", type="http", csrf=False)
    def service_provider_index1(self, user=None, **post):
        # match confirm password
        if user == 'company':
            partner = request.env['res.partner'].sudo().create({'name': post.get('username'),
                                                                'email': post.get('email')})

            company = request.env['res.company'].sudo().create({'name': post.get('username'),
                                                                'partner_id': partner.id,
                                                                'currency_id': request.env['res.currency'].sudo().search([('symbol', '=', post.get('currency'))], limit=1).id})

            request.env['res.users'].sudo().create({'partner_id': partner.id,
                                                    'login': post.get('username'),
                                                    'password': post.get('password'),
                                                    'company_id': company.id,
                                                    'company_ids': [(4, company.id)],
                                                    'users_type': 'company'
                                                    })

        else:
            partner = request.env['res.partner'].sudo().create({'name': post.get('username'),
                                                                'email': post.get('email')})
            request.env['res.users'].sudo().create({'partner_id': partner.id,
                                                    'login': post.get('username'),
                                                    'password': post.get('password'),
                                                    'groups_id': [(6, 0, [request.env.ref('fleet_tracking.group_customer').id])]})

        return http.local_redirect('/web/login?redirect=/web')

    @http.route(['/product_list/'], type='http', auth="user", website=True, csrf=False)
    def product(self, page=1, date_begin=None, date_end=None, sortby=None, **post):
        product_template = request.env['product.template'].sudo().search([])
        return request.render("fleet_tracking.product_list", {"products": product_template})

    @http.route(['/shop/cart/update'], type='http', auth="user", methods=['GET', 'POST'], website=True, csrf=False)
    def cart_update(self, add_qty=1, set_qty=0, **kw):
        product_id = request.env['product.template'].sudo().browse(int(kw['product_template_id']))
        if not request.session.order_id:
            order_id = request.env['sale.order'].sudo().create({
                'partner_id': request.env['res.users'].browse([request.session.uid]).partner_id.id,
                'amount_total': product_id.list_price
                })

            request.env['sale.order.line'].sudo().create({
                'order_id': order_id.id,
                'name': product_id.name,
                'product_id': product_id.id,
                'price_unit': product_id.list_price,
                'product_uom_qty': 1,
                })
            request.session['order_id'] = order_id.id
            return werkzeug.utils.redirect("/cart/")
        else:
            order = request.env['sale.order'].sudo().browse(int(request.session.order_id))
            order.write({
                'amount_total': product_id.list_price + order.amount_total
                })
            product_id = request.env['product.template'].sudo().browse(int(kw['product_template_id']))
            request.env['sale.order.line'].sudo().create({
                'order_id': order.id,
                'name': product_id.name,
                'product_id': product_id.id,
                'price_unit': product_id.list_price,
                'product_uom_qty': 1,
            })
            return werkzeug.utils.redirect("/cart/")

    @http.route('/confirm_order', method="post", auth="user", type="http", csrf=False)
    def confirm_booking(self, **post):
        print(post.get('contract_id'), "***********", post.get('amount'))
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        merchant_id = request.env['ir.config_parameter'].sudo().get_param('sandbox_merchant_id')
        merchant_key = request.env['ir.config_parameter'].sudo().get_param('sandbox_merchant_key')
        data_dict = {
            'MID': merchant_id,
            'WEBSITE': 'WEBSTAGING',
            'ORDER_ID': post.get('contract_id'),
            'CUST_ID': str(request.uid),
            'INDUSTRY_TYPE_ID': 'Retail',
            'CHANNEL_ID': 'WEB',
            'TXN_AMOUNT': str(post.get('amount')),
            'CALLBACK_URL': urls.url_join(base_url, '/paytm_response')
        }
        data_dict['CHECKSUMHASH'] = checksum.generate_checksum(data_dict, merchant_key)
        data_dict['redirection_url'] = "https://securegw-stage.paytm.in/order/process"
        return request.make_response(json.dumps(data_dict))

    @http.route('/paytm_response', method="post", type="http", csrf=False)
    def paytm_response(self, **post):
        merchant_key = request.env['ir.config_parameter'].sudo().get_param('sandbox_merchant_key')
        checksum_status = checksum.verify_checksum(post, merchant_key, post.get('CHECKSUMHASH'))
        order_id = post.get('ORDERID')
        contract = request.env['fleet.vehicle.contract.booking'].sudo().search([('order_id', '=', order_id)])
        if checksum_status:
            today = datetime.today()
            payment_status = post.get('STATUS')
            if payment_status == 'TXN_SUCCESS':
                contract.write({'acquirer_ref': post.get('TXNID'), 'state': 'confirm', 'payment_status': 'success', 'payment_date': today})
            elif payment_status == 'TXN_FAILURE':
                contract.write({'acquirer_ref': post.get('TXNID'), 'state': 'draft', 'payment_status': 'fail', 'payment_date': today})
            elif payment_status == 'TXN_PENDING':
                contract.write({'acquirer_ref': post.get('TXNID'), 'state': 'draft', 'payment_status': 'pending', 'payment_date': today})
            else:
                raise ValidationError(_('For some reasion, There some error accure in payment process!'))
        return werkzeug.utils.redirect('/payment/process?order_id=%s' % (order_id))

    @http.route('/payment/process', method="post", type="http", csrf=False)
    def paytm_process(self, **post):
        request.session['order_id'] = None
        order_id = post.get('order_id')
        contract = request.env['sale.order'].sudo().search([('id', '=', order_id)])
        return request.render('fleet_tracking.payment_process', {'contract': contract})

    @http.route('/cart', method="post", type="http", csrf=False)
    def cart(self, **post):
        if request.session.order_id:
            return request.render('fleet_tracking.cart', {'sale_order_lines': request.env['sale.order.line'].sudo().search([]).filtered(lambda order_line: order_line.order_id.id == request.session['order_id']),
                                  'order_id': request.env['sale.order'].sudo().browse(int(request.session.order_id))})
        else:
            return request.render('fleet_tracking.cart', {'sale_order_lines': None})
