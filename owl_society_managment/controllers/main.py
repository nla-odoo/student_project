# -*- coding: utf-8 -*-
from datetime import date
import datetime
from werkzeug import urls
from . import checksum

from odoo import http, SUPERUSER_ID
from odoo.http import request
import json
import base64


class OwlController(http.Controller):

    # def getMemberType(self):
    #     member_type = None
    #     if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('owl_society_managment.society_secratery_group_admin'):
    #         member_type = "secretary"
    #     elif request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_portal'):
    #         member_type = "member"
    #     else:
    #         member_type = "treasurer"
    #     return member_type

    def getMemberType(self):
        member_type = None
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        if user.member_type == 'member':
            member_type = "member"
        elif user.member_type == 'secretary':
            member_type = "secretary"
        else:
            member_type = "treasurer"
        return member_type

    @http.route(['/my', '/my/home'], type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        member_type = self.getMemberType()
        return http.request.render("owl_society_managment.menu_item", {'member_type': member_type})

    @http.route(['/web/signup', '/society_create'], type='http', auth="public", csrf=False)
    def society_form(self, **post):
        return http.request.render("owl_society_managment.society_form")

    # @http.route('/member_create', type='http', auth="public", csrf=False)
    # def member_register(self, **post):
    #     member_type = self.getMemberType()
    #     return http.request.render("owl_society_managment.member_register", {'member_type': member_type})

    # @http.route('/complaint_create', type='http', auth="public", csrf=False)
    # def complaint_register(self, **post):
    #     member_type = self.getMemberType()
    #     return http.request.render("owl_society_managment.complaint_register", {'member_type': member_type})

    # @http.route('/event_create', type='http', auth="public", csrf=False)
    # def event_register(self, **post):
    #     member_type = self.getMemberType()
    #     return http.request.render("owl_society_managment.event_register", {'member_type': member_type})

    # @http.route('/balance_create', type='http', auth="public", csrf=False)
    # def balance_register(self, **post):
    #     return http.request.render("owl_society_managment.balance_register")

    # @http.route('/jounral_create', type='http', auth="public", csrf=False)
    # def jounral_register(self, **post):
    #     return http.request.render("owl_society_managment.jounral_register")

    # @http.route('/account_create', type='http', auth="public", csrf=False)
    # def account_register(self, **post):

    @http.route('/payment_create', type='http', auth="public", csrf=False)
    def payment_form(self, **post):
        return http.request.render("owl_society_managment.payment_form")

    @http.route('/society', auth="public", type="json", csrf=False)
    def society_register_form(self, **kw):
        currencys = request.env['res.currency'].sudo().search_read([], ['id', 'name'])
        print('\n\n\n\n\n\n 111111', currencys)
        return currencys

    @http.route('/society/form/', auth="public", type="json", csrf=False)
    def society_register(self, **post):
        currencys = request.env['res.currency'].sudo().search_read([], ['id', 'name'])
        print('\n\n\n\n\n\n\n\n', post)
        # groups_id_name = [(6, 0, [request.env.ref('base.group_portal').id])]
        groups_id_name = [(6, 0, [request.env.ref('owl_society_managment.society_secratery_group_admin').id])]
        currency = request.env['res.currency'].sudo().search([('id', '=', post.get('currency'))], limit=1)
        partner = request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'is_company': True,
            'street': post.get('street'),
            'zip': post.get('zip'),
            'city': post.get('city'),
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
            'member_type': 'secretary',
            'company_ids': [(4, company.id)],
            'groups_id': groups_id_name
        })
        request.env['account.journal'].sudo().create([{
                'name': post.get('name'),
                'type': 'cash',
                'code': post.get('code'),
                'company_id': company.id
                }])
        request.env['account.account'].sudo().create([{
                'name': post.get('name'),
                'user_type_id': 2,
                'code': post.get('code'),
                'company_id': company.id,
                'reconcile': 'TRUE',
                }])
        # alias = request.env['mail.alias'].sudo().create({
        #         'alias_name': post.get('alias_name'),
        #         'alias_model_id': 447,
        #     })
        # val = {
        #     'name': post.get('name'),
        #     'alias_id': alias.id,
        #     'company_id': company.id,
        # }
        # print('\n\n\n\n\n\n\n$$$$$$$$$$$', val)
        # team = request.env['helpdesk.team'].sudo().create({
        #     'name': post.get('name'),
        #     'alias_id': alias.id,
        #     'company_id': company.id,
        #         })
        # print('\n\n\n\n\n\n\n********', team)
        return currencys

    @http.route('/get_member_data', auth="user", type="json", csrf=False)
    def get_member(self, offset=0, limit=0):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        members = request.env['res.users'].sudo().search_read([('company_id', '=', user.company_id.id)], ['id', 'name', 'email', 'member_type'])
        print('\n\n\n\n\n\n 111111', members)
        member_type = self.getMemberType()
        return (members, member_type)

    @http.route('/member/form', auth="user", type="json", csrf=False)
    def member_form(self, **kw):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        products = request.env['product.product'].sudo().search([('company_id', '=', user.company_id.id)])
        print('\n\n\n\n\n\n\n\n33333333', user, '\n\n\n\n\n\n++++++++', products)
        print('\n\n\n\n\n\n\n\n44444444', kw, '\n\n\n\n\n\n*******', user.company_id.street)
        member_type = kw.get('member_type')
        if member_type == 'treasurer':
            groups_id_name = [(6, 0, [request.env.ref('owl_society_managment.society_treasurer_group_admin').id])]
        else:
            groups_id_name = [(6, 0, [request.env.ref('base.group_portal').id])]
        partner = request.env['res.partner'].sudo().create({
            'name': kw.get('name'),
            'email': kw.get('email'),
            'street': user.company_id.street,
            'street2': kw.get('street2'),
            'zip': user.company_id.zip,
            'city': user.company_id.city,
        })
        user = request.env['res.users'].sudo().create({
            'partner_id': partner.id,
            'login': kw.get('email'),
            'password': kw.get('name'),
            'member_type': kw.get('member_type'),
            'groups_id': groups_id_name
        })
        sale = request.env['sale.order'].sudo().create({
                    'partner_id': partner.id,
                    'state': 'sale',
                    'user_id': user.id,
                    'invoice_status': 'no',
                    'company_id': user.company_id.id,
                })
        subsciption = request.env['sale.subscription'].sudo().create({
                    'partner_id': partner.id,
                    'template_id': 2,
                    'user_id': user.id,
                    'recurring_total': sale.amount_total,
                    'recurring_total_incl': sale.amount_total,
                    'company_id': user.company_id.id,
                })
        print('\n\n\n\n\n\n\n\n\n555555555555', sale)
        for i in products:
            val = {
                        'order_id': sale.id,
                        'product_id': i.id,
                        'name': i.name,
                        'price_total': int(i.list_price),
                        'price_unit': int(i.list_price),
            }
            print('\n\n\n\n\n\n\n!!!!!!!!!!!!!!', val)
            sale_order = request.env['sale.order.line'].sudo().create({
                        'order_id': sale.id,
                        'product_id': i.id,
                        'name': i.name,
                        'price_total': int(i.list_price),
                        'price_unit': int(i.list_price),
                    })
            print('\n\n\n\n\n\n\n\n\n\n\n666666', sale_order)
            vals = {
                        'product_id': i.id,
                        'name': i.name,
                        'price_total': int(i.list_price),
                        'price_unit': int(i.list_price),
                        'uom_id': i.uom_id,
                        'company_id': user.company_id.id,
            }
            print('\n\n\n\n\n\n\n\n\n @@@@@@@@@@', vals)
            sale_subsciption = request.env['sale.subscription.line'].sudo().create({
                        'product_id': i.id,
                        'name': i.name,
                        'price_total': int(i.list_price),
                        'price_unit': int(i.list_price),
                        'uom_id': int(i.uom_id),
                        'analytic_account_id': subsciption.id,
                        'company_id': user.company_id.id,
                    })
            print('\n\n\n\n\n666666', sale_order, '\n\n\n\n\n\n\n777777', sale_subsciption)
        print('\n\n\n\n\n\n\n\n##########', sale_subsciption.price_total)
        print('\n\n\n\n\n\n\n\n888888', subsciption)
        return self.get_member()

    @http.route('/member/unlink', auth="user", type="json", csrf=False)
    def member_unlink(self, **kw):
        print('\n\n\n\n\n\n***********@@@@@', kw)
        if kw.get('partner_id'):
            print('\n\n\n\n\n\n I am PARTNER')
            request.env['res.users'].sudo().browse([int(kw.get('partner_id'))]).unlink()
        elif kw.get('event_id'):
            print('\n\n\n\n\n\n I am EVENT')
            request.env['event.event'].sudo().browse([int(kw.get('event_id'))]).unlink()
        else:
            complaint = request.env['helpdesk.ticket'].sudo().browse([int(kw.get('complaint_id'))])
            if int(complaint.stage_id) == 1:
                complaint.write({
                    'stage_id': 2
                    })
            else:
                complaint.write({
                    'stage_id': 3
                    })
            print('\n\n\n\n\n#########', complaint, '\n\n\n\n\n\n$$$$$$', complaint.stage_id)

        # print('\n\n\n\n\n\n 111111', subscriptions)
        return self.get_member()

    @http.route('/get_Product_data', auth="user", type="json", csrf=False)
    def get_product(self, **post):
        subscriptions = request.env['sale.subscription.template'].sudo().search_read([], ['id', 'name'])
        print('\n\n\n\n\n\n 111111', subscriptions)
        return subscriptions

    @http.route('/services/form', auth="user", type="json", csrf=False)
    def services_form(self, **kw):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        member = request.env['res.users'].sudo().search([('create_uid', '=', user.id)])
        print('\n\n\n\n\n\n\n\n', kw, '\n\n\n\n\n$$$$$$$$$', member)
        # umo = request.env['uom.uom'].sudo.search([])
        if int(kw.get('subscription_template_id')) == 1:
            print('\n\n\n\n\n\n\n1111111')
            uom_id = 23
        else:
            uom_id = 24
        # file = open(kw.get('image_1920'), 'rb')base64.encodestring(file.read()),base64.encodebytes
        # print('\n\n\n\n\n\n\n\n22222', file)
        prod = request.env['product.product'].sudo().create([{
                    'name': kw.get('name'),
                    'purchase_ok': False,
                    'sale_ok': kw.get('sale_ok'),
                    # 'rent_ok': kw.get('rent_ok'),
                    'type': kw.get('type'),
                    'standard_price': kw.get('standard_price'),
                    'list_price': kw.get('list_price'),
                    'recurring_invoice': kw.get('recurring_invoice'),
                    'subscription_template_id': kw.get('subscription_template_id'),
                    # 'image_1920': base64.encodebytes(kw.get('image_1920')),
                    'uom_id': uom_id,
                    'uom_po_id': uom_id,
                    'company_id': user.company_id.id
                    }])
        print('\n\n\n\n\n\n\n\n\n50000', prod.id)
        for i in member:
            sale = request.env['sale.order'].sudo().create({
                        'partner_id': i.partner_id.id,
                        'state': 'sale',
                        'user_id': user.id,
                        'invoice_status': 'no',
                        'company_id': user.company_id.id,
                    })
            subsciption = request.env['sale.subscription'].sudo().create({
                        'partner_id': i.partner_id.id,
                        'template_id': 2,
                        'user_id': user.id,
                        'recurring_total': sale.amount_total,
                        'recurring_total_incl': sale.amount_total,
                        'company_id': user.company_id.id,
                    })
            print('\n\n\n\n\n\n\n\n\n555555555555', sale)
            val = {
                        'order_id': sale.id,
                        'product_id': prod.id,
                        'name': prod.name,
                        'price_total': int(prod.list_price),
                        'price_unit': int(prod.list_price),
            }
            print('\n\n\n\n\n\n\n!!!!!!!!!!!!!!', val)
            sale_order = request.env['sale.order.line'].sudo().create({
                        'order_id': sale.id,
                        'product_id': prod.id,
                        'name': prod.name,
                        'price_total': int(prod.list_price),
                        'price_unit': int(prod.list_price),
                    })
            print('\n\n\n\n\n\n\n\n\n\n\n666666', sale_order)
            vals = {
                        'product_id': prod.id,
                        'name': prod.name,
                        'price_total': int(prod.list_price),
                        'price_unit': int(prod.list_price),
                        'uom_id': prod.uom_id,
                        'company_id': user.company_id.id,
            }
            print('\n\n\n\n\n\n\n\n\n @@@@@@@@@@', vals)
            sale_subsciption = request.env['sale.subscription.line'].sudo().create({
                        'product_id': prod.id,
                        'name': prod.name,
                        'price_total': int(prod.list_price),
                        'price_unit': int(prod.list_price),
                        'uom_id': int(prod.uom_id),
                        'analytic_account_id': subsciption.id,
                        'company_id': user.company_id.id,
                    })
            print('\n\n\n\n\n\n\n@@@@@@', sale_subsciption)
        # request.env['rental.pricing'].sudo().create([{
        #             'duration': kw.get('duration'),
        #             'unit': kw.get('unit'),
        #             'price': kw.get('price'),
        #             'product_template_id': prod.id,
        #             }])
        # return http.request.render("owl_society_managment.demo_template")
        # return http.local_redirect('/owl_demo')
        return self.get_product()

    @http.route('/get_complaint_data', auth="user", type="json", csrf=False)
    def get_complaint(self, **post):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        members = request.env['res.users'].sudo().search_read([('company_id', '=', user.company_id.id)], ['id', 'name', 'email'])
        complaints = request.env['helpdesk.ticket'].sudo().search_read([('company_id', '=', user.company_id.id)], ['id', 'name', 'partner_name', 'stage_id'])
        print('\n\n\n\n\n\n 111111', complaints)
        member_type = self.getMemberType()
        return (complaints, member_type, members)

    @http.route('/complaint/form', auth="user", type="json", csrf=False)
    def complaint_form(self, **kw):
        print('\n\n\n\n\n\n\n22222222', kw)
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        print('\n\n\n\n\n\n\n\n\n333333', user, '\n\n\n\n\n44444', user.company_id)
        team = request.env['helpdesk.team'].sudo().search([('company_id', '=', int(user.company_id))])
        complaint = request.env['helpdesk.ticket'].sudo().create([{
                'name': kw.get('name'),
                'partner_name': user.partner_id.name,
                'partner_email': user.partner_id.email,
                'team_id': team.id,
                'company_id': user.company_id.id,
                }])
        print('\n\n\n\n\n\n\n6666666', complaint.company_id)
        # return http.request.render("owl_society_managment.member_register")
        # return http.local_redirect('/owl_demo')
        return self.get_complaint()

    @http.route('/get_event_data', auth="user", type="json", csrf=False)
    def get_event(self, **post):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        events = request.env['event.event'].sudo().search_read([('company_id', '=', user.company_id.id)], ['id', 'name', 'date_begin', 'date_end', 'note'])
        # ev = request.env['event.event'].sudo().search([('company_id', '=', user.company_id.id)])
        # date = datetime.datetime.strftime(ev.date_begin, "%Y %m %d %H:%M:%S")
        # curr = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d").date()
        # for i in ev:
        #     start = datetime.datetime.strptime(str(i.date_begin), "%Y-%m-%d %H:%M:%S").date()
        #     print('\n\n\n\n\n\n@@@@', start)
        #     remaing = (start - curr).days
        #     print('\n\n\n\n\n\n#######', remaing)
        #     if remaing < 0:
        # if remaing < 0:
        #     events = request.env['event.event'].sudo().browse(int(ev.id)).write({
        #         'stage_id': 4
        #         })
        # elif remaing == 0:
        #     events = request.env['event.event'].sudo().browse(int(ev.id)).write({
        #         'stage_id': 2
        #         })
        # else:
        #     print('\n\n\n\n\n\n\n*******hiiiiiiiii')
        print('\n\n\n\n\n\n 111111', events)
        # member_type = self.getMemberType()
        print('\n\n\n\n\n\n\n\n\n**********', user.member_type)
        return (events, user.member_type)

    @http.route('/event/form', auth="user", type="json", csrf=False)
    def event_form(self, **kw):
        # events = request.env['event.event'].sudo().search([('company_id', '=', request.session.uid)])

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
        return self.get_event()
        # return {"am": am}

    @http.route('/paytm/payment', auth='user', type="json")
    def payment(self, **kw):
        print('\n\n\n\n\n\n\n\n\n@@@@@@@@@', kw)
        # inquiry = request.env['crm.lead'].sudo().browse([int(kw.get('inquiry_id'))])
        # user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        orders = request.env['account.payment'].sudo().browse([int(kw.get('payment'))])
        print('\n\n\n\n\n\n\n\n\n&&&&&&&&', orders.order_reference)
        print('\n\n\n\n\n\n\n\n\n^^^^^^^^^^', orders.amount)
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        data_dict = {
            'MID': 'TinyER40943268666403',
            'WEBSITE': 'WEBSTAGING',
            'ORDER_ID': str(orders.order_reference),
            'CUST_ID': str(request.uid),
            'INDUSTRY_TYPE_ID': 'Retail',
            'CHANNEL_ID': 'WEB',
            'TXN_AMOUNT': str(orders.amount),
            'CALLBACK_URL': urls.url_join(base_url, '/paytm_response')
        }
        data_dict['CHECKSUMHASH'] = checksum.generate_checksum(data_dict, 'XdanaSDPoWj#!P7s')
        data_dict['redirection_url'] = 'https://securegw-stage.paytm.in/order/process'
        return data_dict

    @http.route('/paytm_response', type="json", csrf=False)
    def paytm_response(self, **kw):
        print('\n\n\n', kw)
        # order_payment = request.env['print.order'].search([('order_reference', '=', kw.get('ORDERID'))], limit=1)
        if checksum.verify_checksum(kw, 'XdanaSDPoWj#!P7s', kw.get('CHECKSUMHASH')):
            if(kw.get('STATUS') == 'TXN_SUCCESS'):
                return http.local_redirect('/balance/form', kw)
            elif(kw.get('STATUS') == 'TXN_FAILURE'):
                pass
            return http.local_redirect('/my/home')
        else:
            return http.local_redirect("/my/home")

    @http.route('/get_Parnter_data', auth="user", type="json", csrf=False)
    def get_partner(self, **post):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        if user.member_type == 'treasurer':
            partners = request.env['res.partner'].sudo().search_read([('create_uid', '=', int(user.create_uid))], ['id', 'name'])
        else:
            partners = request.env['res.partner'].sudo().search_read([('create_uid', '=', user.id)], ['id', 'name'])
        # accounts = request.env['account.account'].sudo().search_read([('create_uid', '=', int(user.create_uid))], ['id', 'name'])
        accounts = request.env['account.account'].sudo().search_read([('company_id', '=', int(user.company_id))], ['id', 'name'])
        jounrals = request.env['account.journal'].sudo().search_read([('company_id', '=', int(user.company_id))], ['id', 'name'])
        # jounrals = request.env['account.journal'].sudo().search_read([('create_uid', '=', user.id)], ['id', 'name'])
        # jounrals = request.env['account.journal'].sudo().search_read([('create_uid', '=', user.id)], ['id', 'name'])
        member_type = self.getMemberType()
        print('\n\n\n\n\n\n\n\n\n\n\n\n^^^^^^^^^^^^^^^^^', member_type)
        return (partners, accounts, jounrals, member_type)

    @http.route('/balance/form', auth="user", type="json", csrf=False)
    def balance_form(self, **kw):
        print('\n\n\n\n\n\n\n000000', kw)
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        print('\n\n\n\n\n\n\n###########', user)
        if user.member_type == 'member':
            jou = request.env['account.journal'].sudo().search([('company_id', '=', int(user.company_id))], limit=1)
            journal_id = int(jou)
            print('\n\n\n\n\n\n\n**********', user.id)
            partner_id = int(user.partner_id)
            payment_type = 'inbound'
            partner_type = 'customer'
            method = request.env['account.payment.method'].sudo().search([('payment_type', '=', 'inbound')], limit=1)
            print('\n\n\n\n\n\n\n\n\n111111111', method.id)
        else:
            print('\n\n\n\n\n\n\n\n\n222222222222')
            partner_id = int(kw.get('partner_id'))
            payment_type = kw.get('payment_type')
            partner_type = kw.get('partner_type')
            journal_id = int(kw.get('journal_id'))
            method = request.env['account.payment.method'].sudo().search([('payment_type', '=', kw.get('payment_type'))], limit=1)
        # partners = request.env['res.partner'].sudo().search([('id', '=', kw.get('partner_id'))])
        # print('\n\n\n\n\n\n\n\n222222222', partners.id)
        # accounts = request.env['account.account'].sudo().search([('id', '=', kw.get('destination_account_id'))])
        # print('\n\n\n\n\n\n\n\n55555555555555', accounts.id)
        # print('\n\n\n\n\n\n\n\n\n\n\n111111', method.id)
        # currency = request.env['account.journal'].sudo().search([('id', '=', kw.get('journal_id'))], limit=1)
        vals = {
                'move_type': 'entry',
                'journal_id': journal_id,
                'partner_id': partner_id,
                'company_id': user.company_id.id,
        }
        print('\n\n\n\n\n\n 88888888888', vals)
        move = request.env['account.move'].with_user(SUPERUSER_ID).create([{
                'move_type': 'entry',
                'journal_id': journal_id,
                'partner_id': partner_id,
                'company_id': user.company_id.id,
            }])
        print('\n\n\n\n\n\n\n\n\n\n\n\n777777', move.id)
        payment = request.env['account.payment'].sudo().create([{
                'move_id': move.id,
                'payment_type': payment_type,
                'partner_type': partner_type,
                'amount': kw.get('amount'),
                'partner_id': partner_id,
                'date': date.today(),
                'destination_account_id': int(kw.get('destination_account_id')),
                'payment_method_id': method.id,
                }])
        print('\n\n\n\n\n\n\n\n\n\n4444444', payment)
        # return http.request.render("owl_society_managment.demo_template")
        return payment.id

    @http.route('/jounral/form', auth="user", type="json", csrf=False)
    def jounral_form(self, **kw):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        print('\n\n\n\n\n\n\n\n\n\n1111111111', kw)
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
        accounts = request.env['account.account.type'].sudo().search_read([], ['id', 'name'])
        return accounts

    @http.route('/account/form', auth="user", type="json", csrf=False)
    def account_form(self, **kw):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        # accounts = request.env['account.account.type'].sudo().search([('name', '=', kw.get('user_type_id'))])
        # print('\n\n\n\n\n\n\n\n\n', accounts)
        request.env['account.account'].sudo().create([{
                'name': kw.get('name'),
                'user_type_id': int(kw.get('user_type_id')),
                'code': kw.get('code'),
                'company_id': user.company_id.id,
                'reconcile': 'TRUE',
                }])
        # return http.request.render("owl_society_managment.demo_template")
        return http.local_redirect('/owl_demo')

    @http.route('/my_order', type='http', auth="public", csrf=False)
    def owl_demos(self, **post):
        return http.request.render("owl_society_managment.orders_template")

    @http.route('/get_order_details', type='json', auth="public", csrf=False)
    def get_partners(self, **post):
        users = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        if users.member_type == "member":
            domain = [
                ('partner_id', '=', request.env.user.partner_id.id),
                ('state', 'in', ['sale', 'done'])
            ]
        else:
            domain = [
                ('company_id', '=', request.env.user.company_id.id),
                ('state', 'in', ['sale', 'done'])
            ]
        return request.env['sale.order'].sudo().search_read(domain, ['id', 'name', 'date_order', 'amount_total'])

    @http.route('/get_data/', type='http', auth="public", csrf=False)
    def owl_details(self, **post):
        return http.request.render("owl_demo.detail_template")

    @http.route('/order_detail', type='json', auth="public", csrf=False)
    def order_data(self, **kw):
        order = request.env['sale.order'].sudo().search([('id', '=', kw.get('order_id'))])
        order_detail = order.order_line.read(['id', 'name', 'price_unit', 'price_tax', 'price_total', 'product_uom_qty', 'product_id'])
        products = {}
        # for line in order.order_line:
        #     products[line.id] = line.product_id.image_1920
        sale_detail = order.read(['name', 'date_order'])
        partner_detail = order.partner_id.read(['id', 'name', 'street', 'street2', 'city', 'zip'])
        return {'details': order_detail, 'order': sale_detail, 'partner': partner_detail, 'products': products}

    @http.route('/get_account_line_data', auth="user", type="json", csrf=False)
    def get_account_line_data(self, **post):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        domain = [
                ('company_id', '=', int(user.company_id)),
                ('account_internal_type', '=', 'payable')
            ]
        accounts = request.env['account.move.line'].sudo().search_read(domain, ['id', 'name', 'credit', 'debit', 'balance', 'move_name'])
        print('\n\n\n\n\n\n\n\n\n$$$$$$$$$$$$$$$', accounts)
        return accounts

    @http.route('/my_orders', type='http', auth="public", csrf=False)
    def owls_demos(self, **post):
        return http.request.render("owl_society_managment.orders_templates")

    @http.route('/gets_order_details', type='json', auth="public", csrf=False)
    def gets_partners(self, **post):
        users = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        if users.member_type == "member":
            domain = [
                ('partner_id', '=', request.env.user.partner_id.id),
                ('state', 'in', ['draft', 'posted'])
            ]
        else:
            domain = [
                ('company_id', '=', request.env.user.company_id.id),
                ('state', 'in', ['draft', 'posted'])
            ]
        return request.env['account.move'].sudo().search_read(domain, ['id', 'name', 'date', 'amount_total'])

    @http.route('/get_datas/', type='http', auth="public", csrf=False)
    def owls_details(self, **post):
        return http.request.render("owl_demo.detail_templates")

    @http.route('/order_details', type='json', auth="public", csrf=False)
    def order_datas(self, **kw):
        order = request.env['account.move'].sudo().search([('id', '=', kw.get('order_id'))])
        # order_detail = order.order_line.read(['id', 'name', 'price_unit', 'price_tax', 'price_total', 'product_uom_qty', 'product_id'])
        # products = {}
        # for line in order.order_line:
        #     products[line.id] = line.product_id.image_1920
        sale_detail = order.read(['name', 'date', 'amount_total', 'amount_tax'])
        partner_detail = order.partner_id.read(['id', 'name', 'street', 'city', 'zip'])
        return {'order': sale_detail, 'partner': partner_detail}

    @http.route('/get_payment_data', auth="user", type="json", csrf=False)
    def get_payment(self, **post):
        user = request.env['res.users'].sudo().search_read([('id', '=', request.session.uid)], ['id', 'name', 'email'])
        # members = request.env['res.users'].sudo().search_read([('company_id', '=', user.company_id.id)], ['id', 'name', 'email'])
        # complaints = request.env['helpdesk.ticket'].sudo().search_read([('company_id', '=', user.company_id.id)], ['id', 'name', 'partner_name', 'stage_id'])
        print('\n\n\n\n\n\n\n00000000', user)
        orders = request.env['sale.order'].sudo().search_read([('user_id', '=', request.session.uid)], ['id', 'name', 'partner_id', 'amount_total'])
        print('\n\n\n\n\n\n 111111', orders)
        member_type = self.getMemberType()
        return (orders, member_type, user)

    @http.route('/payment/form', auth="user", type="json", csrf=False)
    def payments_form(self, **kw):
        print('\n\n\n\n\n\n\n22222222', kw)
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)])
        print('\n\n\n\n\n\n\n\n\n333333', user, '\n\n\n\n\n44444', user.company_id)
        team = request.env['helpdesk.team'].sudo().search([('company_id', '=', user.company_id)])
        complaint = request.env['helpdesk.ticket'].sudo().create([{
                'name': kw.get('name'),
                'partner_name': user.partner_id.name,
                'partner_email': user.partner_id.email,
                'team_id': team.id,
                'company_id': user.company_id.id,
                }])
        print('\n\n\n\n\n\n\n6666666', complaint.company_id)
        # return http.request.render("owl_society_managment.member_register")
        # return http.local_redirect('/owl_demo')
        return self.get_payment()

    # @http.route('/account', type='http', auth="public", csrf=False)
    # def account(self, **post):
    #     # member_type = self.getMemberType()
    #     return http.request.render("owl_society_managment.account")
