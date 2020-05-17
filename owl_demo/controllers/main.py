# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
# from odoo.addons.web.controllers.main import Home


# class Home(Home):
#     # pass
#     def _login_redirect(self, uid, redirect=None):
#         if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
#             return '/web/'
#         if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
#             return'/web/'
#         return super(OwlController, self)._login_redirect(uid, redirect=redirect)


class OwlController(http.Controller):

    @http.route('/owl_demo', type='http', auth="public", csrf=False, website=True)
    def owl_demo(self, **post):
        return http.request.render("owl_demo.demo_template")

    @http.route('/owl_demo_student', type='http', auth="public", csrf=False, website=True)
    def student(self, **post):
        return http.request.render("owl_demo.student")

    @http.route('/owl_demo_ragi', type='http', auth="public", csrf=False, website=True)
    def demo_ragi(self, **post):
        return http.request.render("owl_demo.demo_ragi")

    @http.route('/owl_demo_add_Student', type='http', auth="public", csrf=False, website=True)
    def demo_AddStudent(self, **post):
        return http.request.render("owl_demo.demo_AddStudent")

    @http.route('/demo_AddStudent', type='json', auth="public", csrf=False, website=True)
    def demo_AddStudents(self, form_data=False, **post):
        # print('\n\n\n\n', form_data)
        if form_data:
            partner = request.env['res.partner'].sudo().create({
                'name': form_data.get("name"),
                "email": form_data.get("email"),
            })
            print("\n\n\n\n")
            print(form_data, "partner")
            print("\n\n\n\n")
            var = request.env["res.users"].sudo().create({
                'login': form_data.get("name"),
                'password': form_data.get('password'),
                'name': form_data.get('name'),
                'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
            })
            print("\n\n\n\n")
            print(var, "var?????????????????????????????????????")
            print("\n\n\n\n")
        # resulrt = request.env['product.template'].sudo().search_read([], ['id',  'name'])
        # print(resulrt, "\n\n\n\n")
        # import pdb
        # pdb.set_trace()
        # return resulrt
        # return {'resulrt': request.env['product.template'].sudo().search_read(["res_user_id", "=", request.env.user.id], ['id',  'name'])}
        return {'resulrt': request.env['product.template'].sudo().search_read([], ['id',  'name'])}

    @http.route('/owl_demo_add_cource', type='http', auth="public", csrf=False, website=True)
    def demo_AddCource(self, **post):
        return http.request.render("owl_demo.demo_AddCource")

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
