# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class Home(Home):
    # pass
    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
            return '/web/'
        if request.session.uid:
            user = request.env['res.users'].sudo().browse(request.session.uid)
            if user.has_group('base.group_portal'):
                if user.is_student:
                    return '/owl_demo_student'
                return'/owl_demo_ragi'
        return super(OwlController, self)._login_redirect(uid, redirect=redirect)


class OwlController(http.Controller):

    @http.route('/owl_demo', type='http', auth="public", csrf=False, website=True)
    def owl_demo(self, **post):
        return http.request.render("owl_demo.demo_template")

    # Student list all student list compny side

    @http.route('/studentlist', type='http', auth="public", csrf=False, website=True)
    def studentlist(self, **post):
        return http.request.render("owl_demo.studentlistent")

    # Student list all student list rpc
    @http.route('/studentlists', type='json', auth="public", csrf=False, website=True)
    def studen_list(self, **post):
        return {'resulrt': request.env['res.users'].sudo().search_read([('create_uid', '=', request.env.user.id)], ['id',  'name'])}

    # Student login after come this page
    @http.route('/owl_demo_student', type='http', auth="public", csrf=False, website=True)
    def student(self, **post):
        return http.request.render("owl_demo.student")

    # register all  institute
    @http.route('/owl_demo_ragi', type='http', auth="public", csrf=False, website=True)
    def demo_ragi(self, **post):
        if request.session.uid:
            if request.env['res.company'].browse(request.session.uid):
                return http.request.render("owl_demo.demo_AddStudent")
        return http.request.render("owl_demo.demo_ragi")

    # institute login after come this page add student
    @http.route('/owl_demo_add_Student', type='http', auth="public", csrf=False, website=True)
    def demo_AddStudent(self, **post):
        return http.request.render("owl_demo.demo_AddStudent")

    # rpc page for studnet add
    @http.route('/demo_AddStudent', type='json', auth="public", csrf=False, website=True)
    def demo_AddStudents(self, form_data=False, **post):
        print('\n\n\n\n', form_data)
        if form_data:
            partner = request.env['res.partner'].sudo().create({
                'name': form_data.get("name"),
                "email": form_data.get("email"),
            })
            course = request.env['product.template'].sudo().search([('name', '=', form_data.get('course_id'))])
            print('\n\n\n\n', course.id)
            var = request.env["res.users"].sudo().create({
                'login': form_data.get("name"),
                'password': form_data.get('password'),
                'name': form_data.get('name'),
                'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
                'is_student': 1,
                'course_name': course.id,
                'fess': course.list_price
            })
            # current_login = request.env['res.partner'].sudo().browse([request.session.uid])
            # self.send_email(current_login.email, partner.email, var)
        # resulrt = request.env['product.template'].sudo().search_read([], ['id',  'name'])
        # print(resulrt, "\n\n\n\n")
        # import pdb
        # pdb.set_trace()
        # return resulrt
        # return {'resulrt': request.env['product.template'].sudo().search_read(["res_user_id", "=", request.env.user.id], ['id',  'name'])}

        # return {'resulrt': request.env['product.template'].sudo().search_read([('create_uid', '=', request.env.user.id)], ['id',  'name', 'list_price'])}
        return {'resulrt': request.env['product.template'].sudo().search_read([('create_uid', '=', request.env.user.id)], ['id',  'name', 'list_price'])}

    # add course
    @http.route('/owl_demo_add_cource', type='http', auth="public", csrf=False, website=True)
    def demo_AddCource(self, **post):
        return http.request.render("owl_demo.demo_AddCource")

    # add course rpc page
    @http.route('/demo_AddCource', type='json', auth="public", csrf=False, website=True)
    def demo_AddCources(self, form_data=False, **post):
        if form_data:
            prodct = request.env['product.template'].sudo().create({
                'name': form_data.get("name"),
                "list_price": form_data.get("list_price"),
            })
            # print('\n\n\n\n', form_data)
        var = [1]
        return var

    @http.route('/get_partner_data', type='json', auth="public", csrf=False, website=True)
    def get_partner(self, offset=0, limit=0):

        request.env.cr.execute("""SELECT count(*) FROM product_template;""")
        count = request.env.cr.fetchone()[0] / 6
        if isinstance(count, (float)):
            count = int(count) + 1
        resulrt = request.env['product.template'].sudo().search_read([], ['id', 'image_1920', 'name', 'type', 'list_price', 'active'], offset=offset, limit=limit)
        print("\n\n\n\n", resulrt)
        return {"resulrt": resulrt, 'count': count}

    # institute refistartion epc page
    @http.route(['/my/user_register'], type='json', auth="public", website=True, methods=['GET', 'POST'])
    def user_registration(self, form_data=False, **kw):
        print("\n\n\n\n\n")
        # print(form_data, form_data)
        if form_data:
            partner = request.env['res.partner'].sudo().create({
                'name': form_data.get("name"),
                "email": form_data.get("email"),
            })

            print("\n\n\n\n\n")
            print(partner)

            currency = request.env['res.currency'].browse(
                [int(form_data.get("currency_id"))])

            print("\n\n\n\n\n")
            print(currency)
            company = request.env['res.company'].sudo().create({
                "name": form_data.get("name"),
                "partner_id": partner.id,
                "currency_id": currency.id,
            })
            print("\n\n\n\n\n")
            print(company)

            # currency_list = request.env['res.currency'].sudo().search([])
            # request.env['res.currency'].sudo().search_read([], ['id',  'name'])

            request.env["res.users"].sudo().create({
                'login': form_data.get("name"),
                'password': form_data.get('password'),
                'name': form_data.get('name'),
                'company_id': company.id,
                'company_ids': [(4, company.id)],
                'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
            })
        return {'resulrt': request.env['res.currency'].sudo().search_read([], ['id',  'name'])}
        # return ({"currency_list": request.env['res.currency'].sudo().search([])})

    def send_email(self, sender_email, reciver_email, user):
        template = False
        try:
            template = request.env['mail.template'].sudo().search([('name', '=', 'Student')])
        except ValueError:
            pass

        template_values = {
            'email_from': 'anuch983@gmail.com',
            'email_to': reciver_email,
            'html_body': ''
        }
        template.write(template_values)

        template.send_mail(user.id, force_send=True, raise_exception=True)
        _logger.info("Password reset email sent for user <%s> to <%s>", user.login, user.email)
