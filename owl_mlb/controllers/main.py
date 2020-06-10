# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home


class Home(Home):
    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
            return '/web/'
        if request.session.uid:
            user = request.env['res.users'].sudo().browse(request.session.uid)
            if user.has_group('base.group_portal'):
                if user.is_customer:
                    return '/owldemo'
                return'/menu'
        return super(OwlController, self)._login_redirect(uid, redirect=redirect)

    @http.route('/', type='http', auth="none")
    def index(self, s_action=None, db=None, **kw):
        url = '/menu'
        if request.session.uid:
            url = '/web'
            user = request.env['res.users'].sudo().browse(request.session.uid)
            if user.has_group('base.group_portal'):
                if user.is_student:
                    url = '/owldemo'
                url = '/menu'
        return http.local_redirect(url, query=request.params, keep_hash=True)


class OwlController(http.Controller):

    @http.route('/menu', type="http", auth="public", csrf=False)
    def menu(self, **post):
        return http.request.render('owl_mlb.menu')

    @http.route('/is_customer', type='json', auth="public", csrf=False, website=True)
    def is_customer(self, **post):
        user = request.env['res.users'].sudo().browse(request.session.uid)
        if user.has_group('base.group_portal') and user.is_customer:
            return True
        return False

    @http.route('/owldemo', type="http", auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render('owl_mlb.demo_template')

    @http.route('/get_partner_data', type='json', auth="public", csrf=False, website=True)
    def get_partner(self, offset=0, limit=0):
        request.env.cr.execute("""SELECT count(*) FROM product_template;""")
        count = request.env.cr.fetchone()[0] / 6
        if isinstance(count, (float)):
            count = int(count) + 1
        result = request.env['product.template'].sudo().search_read(
            [], ['id', 'image_1920', 'name', 'type', 'list_price', 'active'], offset=offset, limit=limit)
        print("\n\n\n\n", result)
        return {"result": result, 'count': count}

    @http.route('/Meal_Register', type="http", auth="public", csrf=False)
    def meal_register(self, **post):
        return http.request.render('owl_mlb.meal_prov_regi')

    @http.route('/Meal_Register_rpc', type="json", auth="public", csrf=False)
    def meal_register_rpc(self, form_data=False, **post):
        if form_data:
            partner = request.env['res.partner'].sudo().create({
                'name': form_data.get("name"),
                "email": form_data.get("email"),
            })

            currency = request.env['res.currency'].browse(
                [int(form_data.get("currency_id"))])

            company = request.env['res.company'].sudo().create({
                "name": form_data.get("name"),
                "partner_id": partner.id,
                "currency_id": currency.id,

            })

            request.env["res.users"].sudo().create({
                'login': form_data.get("name"),
                'password': form_data.get('password'),
                'name': form_data.get('name'),
                'contact_no': form_data.get('contact_no'),
                'address': form_data.get('address'),
                'email': form_data.get('email'),
                'company_id': company.id,
                'company_ids': [(4, company.id)],
                'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
            })
            print('>>>>>>>>>>>>>>>>>>>>>>>>>\n\n\n\n', form_data)
        return {'result': request.env['res.currency'].sudo().search_read([], ['id',  'name'])}

    @http.route('/Cust_Register', type="http", auth="public", csrf=False)
    def cust_register(self, **post):
        return http.request.render('owl_mlb.customer_registration')

    @http.route('/Cust_Register_rpc', type="json", auth="public", csrf=False)
    def cust_register_rpc(self, form_data=False, **post):
        if form_data:
            partner = request.env['res.partner'].sudo().create({
                'mobile': form_data.get("mobile"),
                "email": form_data.get("email"),
                'name': form_data.get('name'),
                "address": form_data.get("address"),
            })
            user = request.env["res.users"].sudo().create({
                'login': form_data.get("name"),
                'password': form_data.get('password'),
                'name': form_data.get('name'),
                'email': form_data.get('email'),
                'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
                'is_customer': 1,
            })
            print('\n\n\n\n\n\n', form_data)
            var = 1
        return var

    @http.route('/AddProduct', type="http", auth="public", csrf=False)
    def AddProduct(self, **post):
        return http.request.render('owl_mlb.addproduct')

    @http.route('/get_product_attribute', type="json", auth="public")
    def get_product_attribute(self, ** post):
        attribute = request.env['product.attribute'].sudo().search([('name', '=', 'plate')])
        return {
            'attribute_id': attribute.id,
            'values': attribute.value_ids.read(['name'])
        }

    @http.route('/AddProduct_rpc', type="json", auth="public", csrf=False)
    def AddProduct_rpc(self, **post):
        vals = {
            'name': post.get('name'),
            'image_1920': post.get('image_1920'),
            'list_price': post.get('list_price'),
            'attribute_line_ids': [(0, 0, {'attribute_id': post.get('attribute_id'), 'value_ids': post.get('value_ids')})]
        }
        print("\n\n\n\n\n\n >>>>>>>>>>", post)
        request.env['product.template'].sudo().create(vals)

    @http.route('/get_products', type='json', auth="public")
    def get_products(self, **post):
        print(">>>\n\n\n\n", request.env.user.company_id.id)
        res_userm = request.env.user
        print('\n\n\n\n res_userm', res_userm)
        products = request.env['product.template'].sudo().search([('create_uid', '=',  request.env.user.id)])
        print("\n\n\n", products)
        data = {}
        for p in products:
            print(request.env['product.attribute.value'].sudo().search_read([('attribute_id', '=', p.attribute_line_ids.attribute_id.id)]))
            data[str(p.id) + '_' + p.name] = request.env['product.attribute.value'].sudo().search_read([('attribute_id', '=', p.attribute_line_ids.attribute_id.id)], ['name'])
            print("\n\n\n data ", data)
        getpro = request.env['product.template'].sudo().search_read([('create_uid', '=',  request.env.user.id)], ['name', 'id', 'list_price'])
        return {'getpro': getpro, 'data': data}

    @http.route(['/cart'], type='json', auth="public", website=True, csrf=False)
    def addtocart(self, **kw):
        product_id = request.env['product.product'].sudo().search([('product_tmpl_id', '=', int(kw['product_template_id']))])
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n\n\n\n", product_id)
        return {'product_id': product_id}
