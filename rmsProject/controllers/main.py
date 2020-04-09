import json

from odoo import http
from odoo.http import request
from datetime import datetime
from . import checksum
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
        return request.render('rms.rms_form', {'currency': currency})

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

    @http.route('/home/inquiry/<model("training.propertyregi"):editid>', auth='public', type='http')
    def inquiry(self, editid=None):
        return request.render('rms.inquiry_form', {'inq': editid})

    @http.route('/home/inquiry/submit/<model("training.propertyregi"):editid>/', type='http', auth="public", method='post', csrf=False)
    def adddata(self, editid=None, **post):
        if post and editid:
                request.env['training.inquiry'].sudo().create({
                        'name': post.get('name'),
                        'email': post.get('email'),
                        'phone': post.get('phone'),
                        'check_in': post.get('CheckIn'),
                        'intrest_in': post.get('Intrestin'),
                        'company_id': editid.company_id.id
                        })
        return http.local_redirect('/home')

    # Check Your Inquiry
    @http.route('/home/yourinquiry', auth='public', csrf=False, type='http')
    def yourinquiry(self):
        check = request.env['training.inquiry'].sudo().search([('create_uid', '=', request.session.uid)])
        print("\n\n\n\n check", check)
        return request.render('rms.yourinquiry', {'idata': check})

    # more information about Property
    @http.route('/home/details/<model("training.propertyregi"):did>', type='http', auth="public")
    def details(self, did=None):
        return request.render('rms.details', {'info': did})

    @http.route(['/home/', '/home/checkInquiry/<int:s>'], method="post", auth='public', csrf=False)
    def index(self, s=None, **post):
        rent = post.get('rent')
        place = post.get('palce')
        propertyregi_sudo = request.env['training.propertyregi'].sudo()
        if place and rent:
            dataa = propertyregi_sudo.search(['|', ('city', '=', place), ('rent', '=', rent)])
            return http.request.render('rms.rms_index', {'data': dataa})
        elif place:
            dataa = propertyregi_sudo.search([('city', '=', place)])
            return http.request.render('rms.rms_index', {'data': dataa})
        elif rent:
            dataa = propertyregi_sudo.search([('rent', '=', rent)])
            return http.request.render('rms.rms_index', {'data': dataa})

        data = request.env['training.propertyregi'].sudo().search([])
        return request.render('rms.rms_index', {'data': data})

    @http.route('/home/tenantregi/<model("training.inquiry"):s>', type='http', auth="public")
    def regi(self, s=None):
            return http.request.render('rms.tenantregi', {'data': s})

    @http.route(['/home/tenantregi/submit/<model("training.inquiry"):inid>'], type='http', auth="public", method='post', csrf=False)
    def tenantsedit(self, inid=None, **kw):
        if kw:
            request.env["training.tenants"].sudo().create({
                    'name': kw.get('name'),
                    'dob': kw.get('dob'),
                    'phone': kw.get('phone'),
                    'gender': kw.get('gender'),
                    'email': kw.get('email'),
                    'occupation': kw.get('Occupation'),
                    'home_address': kw.get('Home_address'),
                    'father_name': kw.get('Father_name'),
                    'father_phone': kw.get('Fphone'),
                    'rent_type': kw.get('renttype'),
                    'company_id': inid.company_id.id
                    })
        return http.local_redirect("/home/")

    @http.route('/home/tenants/', auth='public', type='http')
    def tenantDetails(self, tid=None, **kw):
        tenants_details = request.env['training.tenants'].sudo().search([('create_uid', '=', request.session.uid)])
        allotid = request.env['training.allot'].sudo().search([])
        return request.render('rms.tenant_webview', {'tenantsDetail': tenants_details, 'allotid': allotid})

    @http.route('/home/roomdetail/<int:tid>', auth='public', type='http')
    def room_allot(self, tid=None):
        allot = request.env['training.allot'].sudo().search([('tenant_id', '=', tid)])
        print("\n\n\n\n\n", allot)
        return request.render('rms.tenant_allot', {'allot': allot})

    @http.route('/home/rooms/<model("training.tenants"):tid>', auth='public', type='http')
    def room_details(self, tid=None, **kw):
        room_detils = request.env['training.rooms'].sudo().search([('company_id', '=', tid.company_id.id)])
        return request.render('rms.room_details', {'room_detils': room_detils})

    @http.route('/home/payment/<model("training.allot"):aid>', auth="public", type='http')
    def payment(self, aid=None):
        return request.render('rms.payment', {'i': aid})

    @http.route('/payment_controller', auth="public", type="http", csrf=False)
    def payment_controller(self, **kw):
        marchant_id = request.env['ir.config_parameter'].sudo().get_param('rms.sandbox_merchant_id')
        print("\n\n\n\n", marchant_id)
        merchant_key = request.env['ir.config_parameter'].sudo().get_param('rms.sandbox_merchant_key')
        print("\n\n\n\n", merchant_key)
        order_id = http.request.env['training.allot'].sudo().browse([int(kw.get('tenant_id'))])
        print("\n\n\n\n id =", order_id)
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        data_dict = {
            'MID': marchant_id,
            'WEBSITE': 'WEBSTAGING',
            'ORDER_ID': str(order_id.order_ref),
            'CUST_ID': str(request.uid),
            'INDUSTRY_TYPE_ID': 'Retail',
            'CHANNEL_ID': 'WEB',
            'TXN_AMOUNT': str(order_id.rent),
            'CALLBACK_URL': urls.url_join(base_url, '/paytm_response')
        }
        print("\n\n\n data = ", data_dict)
        data_dict['CHECKSUMHASH'] = checksum.generate_checksum(data_dict, merchant_key)
        data_dict['redirection_url'] = "https://securegw-stage.paytm.in/order/process"
        return request.make_response(json.dumps(data_dict))

    @http.route('/paytm_response', auth="public", type="http", csrf=False)
    def payment_response(self, **kw):
        order_id = request.env['training.allot'].sudo().search([('order_ref', '=', kw.get('ORDERID'))])
        if checksum.verify_checksum(kw, 'bQfzzkKzeCbR7jOl', kw.get('CHECKSUMHASH')):
            if(kw.get('STATUS') == 'TXN_SUCCESS'):
                payment_date = kw.get('TXNDATE')
                order_id.write({'payment_date': datetime.strptime(payment_date[:-2], '%Y-%m-%d %H:%M:%S'), 'acquirer_ref': kw.get('TXNID'), 'status': 'success'})
                return request.render('rms.paytm_payment_success')
            elif(kw.get('STATUS') == 'TXN_FAILURE'):
                order_id.write({'status': 'failure'})
                return request.render('rms.paytm_payment_failure')
        return request.render('rms.paytm_payment_response')
