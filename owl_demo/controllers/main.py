# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home
# from odoo.exceptions import UserError

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

    @http.route('/acceptedstudent', type='http', auth="public", csrf=False, website=True)
    def acceptedstudent(self, **post):
        return http.request.render("owl_demo.acceptedstudentlist")

    @http.route('/acceptedstudent_rpc', type='json', auth="public", csrf=False, website=True)
    def acceptedstudentrpc(self, **post):
        res_users = request.env['res.users'].sudo().browse([request.session.uid])
        # res = request.env['res.users'].sudo().search_read([('institute_id', '=', res_users.company_id.id), ('active', '=', False)], ['id',  'name', 'active', 'fess', 'course_names'])
        res_active = request.env['res.users'].sudo().search_read([('institute_id', '=', res_users.company_id.id), ('active', '=', True)], ['id',  'name', 'active', 'fess', 'course_names'])
        for data in res_active:
            course = request.env['product.template'].sudo().browse([data['course_names']])
            data['course_name'] = course.name
        print("\n\n\n\n\n >>>>>>>>>>>>>>>>>>>>>>>>>>>", res_active)
        return {'res_active': res_active}

    # Student list all student list compny side

    @http.route('/studentlist', type='http', auth="public", csrf=False, website=True)
    def studentlist(self, **post):
        return http.request.render("owl_demo.studentlistent")

    # @http.route('/studentlist', type='http', auth="public", csrf=False, website=True)
    # def studentlist(self, **post):
    #     return http.request.render("owl_demo.studentlistent")

    # actionStudents

    # Student list all student list rpc
    @http.route('/studentlists', type='json', auth="public", csrf=False, website=True)
    def studen_list(self, action=False, student_id=False, **post):
        if action and student_id:
            template_obj = None
            user = request.env['res.users'].sudo().browse([int(student_id)])
            institute = request.env['res.company'].sudo().browse([user.institute_id])
            user_d = request.env['res.partner'].sudo().browse([user.partner_id.id])
            print("\n\n\n")
            print('user >>>>>>>>>>>>', user_d.email)
            if action == 'active':
                user.write({'active': True})
                template_obj = request.env['mail.template'].sudo().search([('name', '=', 'accepted')], limit=1)
            elif action == 'delete':
                # current_login = request.env['res.users'].sudo().browse([request.session.uid])
                # body = template_obj.body_html % (form_data.get("name"), form_data.get('password'))
                # print('\n\n\n\n current_login')
                user.unlink()
                template_obj = request.env['mail.template'].sudo().search([('name', '=', 'Rejected')], limit=1)
            print("\n\n\n\n\n")
            print("\n\n\n\n >>>>>>>>>>>>>>", template_obj)
            if template_obj:
                mail_values = {
                    'body_html': template_obj.body_html,
                    'email_to': user_d.email,
                    'email_from': institute.email,
                }
                print('\n\n\n\n', mail_values)
                request.env['mail.mail'].sudo().create(mail_values).send()
        res_users = request.env['res.users'].sudo().browse([request.session.uid])
        res = request.env['res.users'].sudo().search_read([('institute_id', '=', res_users.company_id.id), ('active', '=', False)], ['id',  'name', 'active', 'fess', 'course_names'])
        # cource_names = []
        for data in res:
            course = request.env['product.template'].sudo().browse([data['course_names']])
            data['course_name'] = course.name
        print("\n\n\n\n\n >>>>>>>>>>>>>>>>>>>>>>>>>>>", res)
        return {'resulrt': res,
                }

    # Student login after come this page
    @http.route('/owl_demo_student', type='http', auth="public", csrf=False, website=True)
    def student(self, **post):
        return http.request.render("owl_demo.student")

    @http.route('/studentpayment', type='json', auth="public", csrf=False, website=True)
    def payment(self, **post):
        res_users = request.env['res.users'].sudo().browse([request.session.uid])
        course = request.env['product.template'].sudo().browse([res_users.course_names])
        return {
            "name": res_users.name,
            "course_name": course.name,
            "fees": res_users.fess,
        }

    @http.route('/is_student', type='json', auth="public", csrf=False, website=True)
    def is_student(self, **post):
        user = request.env['res.users'].sudo().browse(request.session.uid)
        if user.has_group('base.group_portal') and user.is_student:
            return True
        return False

    @http.route('/coursefillter', type='json', auth="public", csrf=False, website=True)
    def coursefillter(self, cource_id=False, **post):
        return request.env['product.template'].sudo().search_read([('cource_id', '=', cource_id)], ['id', 'name'])

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
        if form_data:
            partner = request.env['res.partner'].sudo().create({
                'name': form_data.get("name"),
                "email": form_data.get("email"),
            })
            course = request.env['product.template'].sudo().search([('id', '=', form_data.get('cource_dropdown'))])
            print("\n\n\n")
            print(">>>>>> course", course.id)
            var = request.env["res.users"].sudo().create({
                'login': form_data.get("name"),
                # 'password': form_data.get('password'),
                'name': form_data.get('name'),
                'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
                'is_student': 1,
                'active': False,
                'course_names': course.id,
                'fess': course.list_price,
                'institute_id': form_data.get("ins_dropdown"),
            })
            print(var, "\n\n\n\n")
            # current_login = request.env['res.users'].sudo().browse([request.session.uid])

            # template_obj = request.env['mail.template'].sudo().search([('name', '=', 'Student')], limit=1)
            # body = template_obj.body_html % (form_data.get("name"))
            # print('\n\n\n\n', form_data.get("email"))
            # print('\n\n\n\n current_login', current_login.email)
            # if template_obj:
            #     mail_values = {
            #         'body_html': body,
            #         'email_to': form_data.get("email"),
            #         'email_from': current_login.email,
            #     }
            #     request.env['mail.mail'].sudo().create(mail_values).send()
        return {'resulrt': request.env['res.company'].sudo().search_read([('is_Institute', '=', 1)], ['id',  'name'])}
        # return {'resulrt': request.env['res.company'].sudo().search_read([('create_uid', '=', request.env.user.id)], ['id',  'name'])}

    # add course
    @http.route('/owl_demo_add_cource', type='http', auth="public", csrf=False, website=True)
    def demo_AddCource(self, **post):
        user = request.env['res.users'].sudo().browse(request.session.uid)
        if user.has_group('base.group_portal') and not user.is_student:
            return http.request.render("owl_demo.demo_AddCource")
        return request.redirect('/owl_demo_student')

    # add course rpc page
    @http.route('/demo_AddCource', type='json', auth="public", csrf=False, website=True)
    def demo_AddCources(self, form_data=False, **post):
        if form_data:
            # user = request.env['res.users'].browse([request.env.uid])
            prodct = request.env['product.template'].sudo().create({
                'name': form_data.get("name"),
                "list_price": form_data.get("list_price"),
                'cource_id': request.env['res.users'].browse([request.env.uid]).company_id,
                # 'cource_id': user.company_id,
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
        # print("\n\n\n\n", resulrt)
        return {"resulrt": resulrt, 'count': count}

    # institute refistartion epc page
    @http.route(['/my/user_register'], type='json', auth="public", website=True, methods=['GET', 'POST'])
    def user_registration(self, form_data=False, **kw):
        # print("\n\n\n\n\n")
        # print(form_data, form_data)
        if form_data:
            partner = request.env['res.partner'].sudo().create({
                'name': form_data.get("name"),
                "email": form_data.get("email"),
            })

            # print("\n\n\n\n\n")
            # print(partner)

            currency = request.env['res.currency'].browse(
                [int(form_data.get("currency_id"))])

            # print("\n\n\n\n\n")
            # print(currency)
            company = request.env['res.company'].sudo().create({
                "name": form_data.get("name"),
                "partner_id": partner.id,
                "currency_id": currency.id,
                'is_Institute': 1
            })
            # print("\n\n\n\n\n")
            # print(company)

            # currency_list = request.env['res.currency'].sudo().search([])
            # request.env['res.currency'].sudo().search_read([], ['id',  'name'])

            request.env["res.users"].sudo().create({
                'login': form_data.get("name"),
                'password': form_data.get('password'),
                'name': form_data.get('name'),
                'email': form_data.get('email'),
                'company_id': company.id,
                'company_ids': [(4, company.id)],
                'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
            })
        return {'resulrt': request.env['res.currency'].sudo().search_read([], ['id',  'name'])}
        # return ({"currency_list": request.env['res.currency'].sudo().search([])})

    # def send_email(self, sender_email, reciver_email, user):
    #     template = False
    #     try:
    #         template = request.env['mail.template'].sudo().search([('name', '=', 'Student')])
    #     except ValueError:
    #         pass
    #     body = template.body_html
    #     body = body % (reciver_email, reciver_email)
    #     print("\n\n")
    #     print(">>>> body", body)
    #     template_values = {
    #         'email_from': sender_email,
    #         'email_to': reciver_email,
    #         'html_body': body
    #     }
    #     request.env['mail.mail'].sudo().create(template_values).send()
    #     # template.write(template_values)

        # template.send_mail(user.id, force_send=True, raise_exception=True)
        # _logger.info("Password reset email sent for user <%s> to <%s>", user.login, user.email)
