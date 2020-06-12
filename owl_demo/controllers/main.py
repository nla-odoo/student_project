# -*- coding: utf-8 -*-
from . import checksum
import logging
import uuid
from odoo import http, SUPERUSER_ID
from odoo.http import request
from werkzeug import urls
from odoo.addons.web.controllers.main import Home
# from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class Home(Home):
    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
            return '/web/'
        if request.session.uid:
            user = request.env['res.users'].sudo().browse(request.session.uid)
            if user.has_group('base.group_portal'):
                if user.is_student:
                    return '/studentpaymentdetails'
                return'/college'
        return super(Home, self)._login_redirect(uid, redirect=redirect)

    @http.route('/', type='http', auth="none")
    def index(self, s_action=None, db=None, **kw):
        url = '/register'
        if request.session.uid:
            url = '/web'
            user = request.env['res.users'].sudo().browse(request.session.uid)
            if user.has_group('base.group_portal'):
                if user.is_student:
                    url = '/studentpaymentdetails'
                url = '/college'
        return http.local_redirect(url, query=request.params, keep_hash=True)


class OwlController(http.Controller):

    @http.route('/college', type="http", auth="user", csrf=False, website=True)
    def collge(self, **post):
        return http.request.render("owl_demo.menu_item")

    @http.route('/studentpaymentdetails', type="http", auth="user", csrf=False, website=True)
    def studentpayment(self, **post):
        return http.request.render("owl_demo.menu_item")

    # institute login after come this page add student
    @http.route('/register', type='http', auth="public", csrf=False, website=True)
    def register_redirect(self, **post):
        return http.request.render("owl_demo.menu_item")

    @http.route('/acceptedstudent_rpc', type='json', auth="public", csrf=False, website=True)
    def acceptedstudentrpc(self, **post):
        res_active = request.env['res.users'].sudo().search_read([('company_id', '=', request.env.user.company_id.id), ('active', '=', True)], ['id',  'name', 'active', 'fess', 'course_names'])
        for data in res_active:
            course = request.env['product.template'].sudo().browse([data['course_names']])
            data['course_name'] = course.name
        return {'res_active': res_active}

    # Student list all student list rpc
    @http.route('/studentlists', type='json', auth="public", csrf=False, website=True)
    def studen_list(self, action=False, student_id=False, **post):
        if action and student_id:
            template_obj = None
            user = request.env['res.users'].sudo().browse([int(student_id)])
            if action == 'active':
                user.write({'active': True})
                try:
                    user.with_context(create_user=True).action_reset_password()
                except:
                    pass
            elif action == 'delete':
                user.unlink()
                template_obj = request.env['mail.template'].sudo().search([('name', '=', 'Rejected')], limit=1)
                if template_obj:
                    mail_values = {
                        'body_html': template_obj.body_html,
                        'email_to': user.email,
                        'email_from': user.company_id.email,
                    }
                request.env['mail.mail'].sudo().create(mail_values).send()
        res = request.env['res.users'].sudo().search_read([('company_id', '=', request.env.user.company_id.id), ('active', '=', False)], ['id',  'name', 'active', 'fess', 'course_names'])
        for data in res:
            course = request.env['product.template'].sudo().browse([data['course_names']])
            data['course_name'] = course.name
        return {'resulrt': res, }

    @http.route('/studentpayment', type='json', auth="public", csrf=False, website=True)
    def payment(self, **post):
        res_user = request.env.user
        course = request.env['product.template'].sudo().browse([res_user.course_names])
        journal = request.env['account.journal'].sudo().search([('company_id', '=', res_user.company_id.id)], limit=1)
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # print('\n\n\n>>>>>> journal', journal)
        invoice = request.env['account.move'].sudo().create({
            'partner_id': res_user.partner_id.id,
            'journal_id': journal.id,
            'company_id': res_user.company_id.id,

        })
        vals = {
            'acquirer_id': request.env['payment.acquirer'].search([('company_id', '=', request.env.user.company_id.id)], limit=1).id,
            'reference': str(uuid.uuid4())
        }
        # import pdb
        # pdb.set_trace()
        print("\n\n\n\n\npost", res_user.fess)
        print("\n\n\n\n\npost", course.id)
        # import pdb;pdb.set_trace()
        transaction = invoice._create_payment_transaction(vals)
        data_dict = {
            'MID': 'amitgo59443067266036',
            'WEBSITE': 'WEBSTAGING',
            'ORDER_ID': transaction.reference,
            'CUST_ID': str(request.uid),
            'INDUSTRY_TYPE_ID': 'Retail',
            'CHANNEL_ID': 'WEB',
            'TXN_AMOUNT': str(res_user.fess),
            # 'TXN_AMOUNT': str(1000),
            'CALLBACK_URL': urls.url_join(base_url, '/paytm_response')
        }
        data_dict['CHECKSUMHASH'] = checksum.generate_checksum(data_dict, 'bQfzzkKzeCbR7jOl')
        data_dict['redirection_url'] = "https://securegw-stage.paytm.in/order/process"
        return {
            'data_dict': data_dict,
            "name": res_user.name,
            "course_name": course.name,
            "fees": res_user.fess,
            'id': res_user.id,
        }

    @http.route('/paytm_response', type='http', auth="public", website=True, methods=['GET', 'POST'], csrf=False)
    def paytm_response_in(self, form_data=False, **kw):
        pyment_order = request.params.get('ORDERID')
        institute = request.env['payment.acquirer'].sudo().search([('reference', '=', pyment_order)])
        checksum_status = checksum.verify_checksum(
            kw, 'bQfzzkKzeCbR7jOl', request.params.get('CHECKSUMHASH'))
        if checksum_status:
            payment_status = request.params.get('STATUS')
            if payment_status == 'TXN_SUCCESS':
                # import pdb
                # pdb.set_trace()
                # institute.write({'acquirer_ref': request.params.get('TXNID'), 'state': 'done'})
                print(kw)
                return request.render('owl_demo.response')
                # return http.local_redirect('/success/')
            if payment_status == 'TXN_FAILURE':
                print(kw)
                print("good bye"*10)
                return request.render('owl_demo.response')
                # return http.local_redirect('/cancel/')
        return http.local_redirect('/response')

    @http.route('/response', type='http', auth="public", csrf=False, website=True)
    def responsepay(self, **post):
        return request.render("owl_demo.response")

    @http.route('/is_student', type='json', auth="public", csrf=False, website=True)
    def is_student(self, **post):
        user = request.env['res.users'].sudo().browse(request.session.uid)
        if user.has_group('base.group_portal') and user.is_student:
            return True
        return False

    @http.route('/coursefillter', type='json', auth="public", csrf=False, website=True)
    def coursefillter(self, cource_id=False, **post):
        return request.env['product.template'].sudo().search_read([('cource_id', '=', cource_id)], ['id', 'name'])

    @http.route('/get_institutes', type='json', auth="public", csrf=False)
    def get_institutes(self, **post):
        return request.env['res.company'].sudo().search([]).read(['name'])

    @http.route('/get_courses', type='json', auth="public")
    def get_courses(self, **post):
        institute_id = post.get('institute_id') or request.env.user.company_id.id
        return request.env['product.template'].sudo().search([('company_id', '=', institute_id)]).read(['name', 'list_price'])

    # rpc page for studnet add
    @http.route('/add_student', type='json', auth="public", csrf=False, website=True)
    def demo_AddStudents(self, **post):
        partner = request.env['res.partner'].sudo().create({
            'name': post.get("name"),
            "email": post.get("email"),
            'country_id': request.env['res.country'].search([])[0].id
        })
        course = request.env['product.template'].sudo().search([('id', '=', int(post.get('cource_dropdown')))])
        company = request.env['res.company'].sudo().browse(int(post.get("ins_dropdown")))
        vals = {
            'login': post.get("email"),
            'name': post.get('name'),
            'password': post.get('password'),
            'email': post.get('email'),
            'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
            'is_student': 1,
            'active': False,
            'course_names': course.id,
            'fess': course.list_price,
            'partner_id': partner.id,
            'company_id': company.id,
            'company_ids': [(4, company.id)],
        }
        request.env["res.users"].with_user(SUPERUSER_ID).with_context(no_reset_password=True).create(vals)
        # request.env["res.users"].sudo().create(vals)
        return True

    # add course
    @http.route('/owl_demo_add_cource', type='http', auth="public", csrf=False, website=True)
    def demo_AddCource(self, **post):
        user = request.env['res.users'].sudo().browse(request.session.uid)
        if user.has_group('base.group_portal') and not user.is_student:
            return http.request.render("owl_demo.demo_AddCource")
        return request.redirect('/owl_demo_student')

    # add course rpc page
    @http.route('/demo_AddCource', type='json', auth="public", csrf=False, website=True)
    def demo_AddCources(self, **post):
        print("\n\n\n request.env.user.company_id.id\n\n\n\n >>>>>>>>>>>", request.env.user.company_id.id)
        request.env['product.template'].sudo().create({
            'name': post.get("name"),
            "list_price": post.get("list_price"),
            'company_id': request.env.user.company_id.id})

    @http.route('/get_partner_data', type='json', auth="public", csrf=False, website=True)
    def get_partner(self, offset=0, limit=0):
        request.env.cr.execute("""SELECT count(*) FROM product_template;""")
        count = request.env.cr.fetchone()[0] / 6
        if isinstance(count, (float)):
            count = int(count) + 1
        resulrt = request.env['product.template'].sudo().search_read([], ['id', 'image_1920', 'name', 'type', 'list_price', 'active'], offset=offset, limit=limit)
        return {"resulrt": resulrt, 'count': count}

    # institute refistartion epc page
    @http.route(['/my/user_register'], type='json', auth="public", website=True, methods=['GET', 'POST'])
    def user_registration(self, form_data=False, **kw):
        if form_data:
            partner = request.env['res.partner'].sudo().create({
                'name': form_data.get("name"),
                "email": form_data.get("email"), })

            currency = request.env['res.currency'].browse(
                [int(form_data.get("currency_id"))])

            company = request.env['res.company'].sudo().create({
                "name": form_data.get("name"),
                "partner_id": partner.id,
                "currency_id": currency.id,
                'is_Institute': 1})

            request.env["res.users"].sudo().create({
                'login': form_data.get("email"),
                'password': form_data.get('password'),
                'name': form_data.get('name'),
                'email': form_data.get('email'),
                'company_id': company.id,
                'company_ids': [(4, company.id)],
                'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
            })
            journal = request.env['account.journal'].sudo().create({
                'name': form_data.get('name'),
                'type': 'general',
                'code': 'INV',
                'company_id': company.id})

            request.env['payment.acquirer'].sudo().create({
                'name': company.name,
                'company_id': company.id,
                'state': 'test',
                'journal_id': journal.id
            })
        return {'resulrt': request.env['res.currency'].sudo().search_read([], ['id',  'name'])}

        # return '/studentpaymentdetails'
