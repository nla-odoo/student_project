# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home


class Home(Home):
    # pass
    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
            return '/web/'
        if request.session.uid:
            user = request.env['res.users'].sudo().browse(request.session.uid)
            if user.has_group('base.group_portal'):
                if user.is_customer:
                    return '/owldemo'
                return'/AddProduct'
        return super(OwlController, self)._login_redirect(uid, redirect=redirect)


class OwlController(http.Controller):
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

    @http.route('/AddProduct_rpc', type="json", auth="public", csrf=False)
    def AddProduct_rpc(self, form_data=False,  **post):
        if form_data:
            product = request.env['product.template'].sudo().create({
                'name': form_data.get("name"),
                'list_price': form_data.get('list_price'),
            })
        var = 1
        print('\n\n\n\n', form_data)
        return var

# product add kraviye
# ema product type e Product_Attribute
# n product_value half n full
# etle e varients baki add krwanu
# n product image baki
