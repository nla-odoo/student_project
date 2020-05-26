# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request
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
                    return '/owl_demo_student'
                return'/owl_demo_ragi'
        return super(OwlController, self)._login_redirect(uid, redirect=redirect)


class OwlController(http.Controller):

    @http.route('/college', type="http", auth="user", csrf=False, website=True)
    def collge(self, **post):
        return http.request.render("owl_demo.college")

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
    @http.route('/institute_register', type='http', auth="public", csrf=False, website=True)
    def demo_ragi(self, **post):
        if request.session.uid:
            if request.env['res.company'].browse(request.session.uid):
                return http.request.render("owl_demo.demo_AddStudent")
        return http.request.render("owl_demo.demo_ragi")

    # institute login after come this page add student
    @http.route('/register', type='http', auth="public", csrf=False, website=True)
    def demo_AddStudent(self, **post):
        return http.request.render("owl_demo.demo_AddStudent")

    @http.route('/get_institutes', type='json', auth="public", csrf=False)
    def get_institutes(self, **post):
        return request.env['res.company'].sudo().search([]).read(['name'])

    @http.route('/get_course', type='json', auth="public")
    def get_course(self, institute_id, **post):
        return request.env['product.template'].sudo().search([('company_id', '=', institute_id)]).read(['name'])

    # rpc page for studnet add
    @http.route('/add_student', type='json', auth="public", csrf=False, website=True)
    def demo_AddStudents(self, **post):
        partner = request.env['res.partner'].sudo().create({
            'name': post.get("name"),
            "email": post.get("email"),
        })
        course = request.env['product.template'].sudo().search([('id', '=', int(post.get('cource_dropdown')))])
        vals = {
            'login': post.get("email"),
            'name': post.get('name'),
            'email': post.get('email'),
            'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
            'is_student': 1,
            'active': False,
            'course_names': course.id,
            'fess': course.list_price,
            'partner_id': partner.id,
            'company_id': int(post.get("ins_dropdown"))
        }
        request.env["res.users"].sudo().with_context(no_reset_password=True).create(vals)
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
    def demo_AddCources(self, form_data=False, **post):
        if form_data:
            request.env['product.template'].sudo().create({
                'name': form_data.get("name"),
                "list_price": form_data.get("list_price"),
                'company_id': request.env.user.company_id.id})
        return True

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
                'login': form_data.get("name"),
                'password': form_data.get('password'),
                'name': form_data.get('name'),
                'email': form_data.get('email'),
                'company_id': company.id,
                'company_ids': [(4, company.id)],
                'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
            })
        return {'resulrt': request.env['res.currency'].sudo().search_read([], ['id',  'name'])}
