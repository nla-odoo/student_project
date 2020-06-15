from odoo import http
from odoo.http import request
import logging
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home
from odoo.exceptions import UserError
import base64
import datetime


class Home(Home):
    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
            return '/web/'
        if request.session.uid:
            user = request.env['res.users'].sudo().browse(request.session.uid)
            if user.has_group('base.group_portal'):
                if user.is_customer:
                    return '/Customer_Portal'
                return'/Transporter_Portal'
        return super(OwlController, self)._login_redirect(uid, redirect=redirect)


class OwlController(http.Controller):

    @http.route('/Customer_Portal', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("loading_transportation_system.menu_item2")

    @http.route('/Transporter_Portal', type='http', auth="public", csrf=False)
    def owl_demo2(self, **post):
        return http.request.render("loading_transportation_system.transporter_item")

    @http.route('/get_partner_data', type='json', auth="public", csrf=False)
    def get_partner(self, **post):
        partner = request.env.user.partner_id
        # return request.env['res.partner'].search([]).mapped('name')
        return http.request.env['res.partner'].sudo().search_read([('id', '=', partner.id)], ['name', 'type', 'street', 'city', 'email', 'phone'])

    @http.route('/partner_data', type='http', auth="public", csrf=False)
    def partner_data(self, **post):
        # partner = request.env.user.partner_id
        # return request.env['res.partner'].search([]).mapped('name')
        # return http.request.env['res.partner'].sudo().search_read([('id' , '=', partner.id)] ,['name' , 'type' , 'street' , 'city' , 'email' , 'phone'])
        return http.request.render("loading_transportation_system.demo_template2")

    @http.route('/inquirey', type='json', auth="public", csrf=False)
    def get_leads(self, **post):
        partner = request.env.user.partner_id
        return http.request.env['crm.lead'].sudo().search_read([('partner_id', '=', partner.id)], ['name', 'description', 'partner_id', 'type'])

    @http.route('/get_inquirey', type='http', auth="public", csrf=False)
    def leads(self, **post):
        # partner = request.env.user.partner_id
        # return http.request.env['crm.lead'].sudo().search_read([('partner_id', '=', partner.id)], ['name', 'description', 'partner_id', 'type'])
        return http.request.render("loading_transportation_system.lead_temp")

    @http.route('/transporters', type='json', auth="public", csrf=False)
    def get_transporters(self, **post):
        return request.env['res.company'].sudo().search_read([], ['name', 'email', 'phone'])

    @http.route('/get_transporters', type='http', auth="public", csrf=False)
    def get_transporter(self, **post):
        # partner = request.env.user.partner_id
        # return http.request.env['crm.lead'].sudo().search_read([('partner_id', '=', partner.id)], ['name', 'description', 'partner_id', 'type'])
        return http.request.render("loading_transportation_system.demo_template")

    @http.route('/lead/form/', auth="public", type="json", csrf=False)
    def lead_form(self, **kw):
        # print('\n\n\n\n\n\n\n\n', kw)
        request.env['crm.lead'].sudo().create([{
            'description': kw.get('description'),
            'name': kw.get('name'),
            'user_id': False,
            'partner_id': request.env.user.partner_id.id
        }])
        return self.get_leads()

    # @http.route('/owl_demo_ragi', type='http', auth="public", csrf=False, website=True)
    # def demo_ragi(self, **post):
    #     if request.session.uid:
    #         if request.env['res.partner'].browse(request.session.uid):
    #             return http.request.render("loading_transportation_system.demo_template")
    #     return http.request.render("loading_transportation_system.demo_ragi")

    @http.route('/is_customer', type='json', auth="public", csrf=False, website=True)
    def is_customer(self, **post):
        user = request.env['res.users'].sudo().browse(request.session.uid)
        if user.has_group('base.group_portal') and user.is_customer:
            return True
        return False

    @http.route('/Cust_Register', type="http", auth="public", csrf=False)
    def cust_register(self, **post):
        return http.request.render('loading_transportation_system.customer_registration')

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
            print('\n\n\n\n\n\n parnerid', form_data)
            var = 1
        return var

    @http.route('/transporter_register', type="http", auth="public", csrf=False)
    def Transporter_Register(self, **post):
        return http.request.render('loading_transportation_system.transporter_registration')

    @http.route('/Transporter_Register_rpc', type="json", auth="public", csrf=False)
    def transporter_register_rpc(self, form_data=False, **post):
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

    @http.route('/my_vehicles', type='http', auth="public", csrf=False)
    def vehicles(self, **post):
        return http.request.render("loading_transportation_system.display_vehicle")

    @http.route('/vehicle', type='json', auth="public", csrf=False)
    def get_vehicle(self, **post):
        # partner = request.env.user.partner_id
        print("\n\n\n\n\n", request.session.uid)
        return request.env['product.template'].sudo().search_read([(['create_uid', '=', request.session.uid])], ['name', 'description', ])

    @http.route('/cust_vehicle', type='json', auth="public", csrf=False)
    def get_custs_vehicle(self, **post):
        # partner = request.env.user.partner_id
        print("\n\n\n\n\n", request.session.uid)
        return request.env['product.template'].sudo().search_read([], ['name', 'description'])

    # @http.route('/vehicle/form/', auth="public", type="json", csrf=False)
    # def vehicle_form(self, **kw):
    #     # print('\n\n\n\n\n\n\n\n', kw)
    #     request.env['product.template'].sudo().create([{
    #         'description': kw.get('description'),
    #         'name': kw.get('name'),
    #         # s'user_id': False,
    #         # 'partner_id': request.env.user.partner_id.id
    #     }])
    #     return self.get_vehicle()

    @http.route('/my_drivers', type='http', auth="public", csrf=False)
    def drivers(self, **post):
        return http.request.render("loading_transportation_system.display_driver")

    @http.route('/driver', type='json', auth="public", csrf=False)
    def get_driver(self, **post):
        return request.env['product.template'].sudo().search_read([(['create_uid', '=', request.session.uid])], ['name', 'description', ])

    @http.route('/driver/form/', auth="public", type="json", csrf=False)
    def driver_form(self, **kw):
        # print('\n\n\n\n\n\n\n\n', kw)
        p = request.env['product.template'].sudo().create([{
            'description': kw.get('description'),
            'name': kw.get('name'),
            # 'user_id': False,
            # 'partner_id': request.env.user.partner_id.id
        }])
        print("\n\n\n\n\n\n\n\n\n\n", p)
        return self.get_driver()

    @http.route('/addproduct', auth="public", type="http", csrf=False)
    def AddProduct(self, **post):
        return http.request.render('loading_transportation_system.display_vehicle')

    # @http.route('/AddProduct_rpc', type="json", auth="public", csrf=False)
    # def AddProduct_rpc(self, form_data=False,  **post):
    #     if form_data:
    #         product = request.env['product.template'].sudo().create({
    #             'name': form_data.get("name"),
    #             'list_price': form_data.get('list_price'),
    #             'partner_id': request.env.user.partner_id.id,
    #             'image_1920': base64.b64encode(kw.get('image_1920').read())
    #         })
    #     var = 1
    #     print('\n\n\n\n', form_data)
    #     return var

    @http.route('/get_product_attribute', type="json", auth="public")
    def get_product_attribute(self, ** post):
        attribute = request.env['product.attribute'].sudo().search(
            [('name', '=', 'type')])
        return {
            'attribute_id': attribute.id,
            'values': attribute.value_ids.sudo().read(['name'])
        }
        # print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n attribute", attribute)

    @http.route('/AddProduct_rpc', type="json", auth="public", csrf=False)
    def AddProduct_rpc(self, **post):
        vals = {
            'name': post.get('name'),
            'list_price': post.get('list_price'),
            'description': post.get('description'),
            'attribute_line_ids': [(0, 0, {'attribute_id': post.get('attribute_id'), 'value_ids': post.get('value_ids')})],
            'create_uid': request.session.uid,
        }
        request.env['product.template'].sudo().create(vals)

    @http.route('/get_p_att', type="json", auth="public", csrf=False)
    def get_p_attribute(self, **post):
        aid = request.env['product.template.attribute.value'].sudo().search(['product_attribute_value_id'])
        print("\n\n\n\n\n\n\n\n attribute---------id", aid)
        # attribute = request.env['product.attribute'].sudo().search(   
        #     [('name', '=', 'type')])
        # return {
        #     'attribute_id': attribute.id,
        #     'values': attribute.value_ids.sudo().read(['name'])
        # }
        return request.env['product.product'].sudo().search_read([(['product_template_attribute_value_ids', '=', aid])], ['id', 'name'])
        # return request.env['product.product'].sudo().search([], ['product_template_attribute_value_ids'])

    @http.route('/my_order', type='http', auth="public", csrf=False)
    def orders(self, **post):
        return http.request.render("loading_transportation_system.display_orders")

    @http.route('/get_order', type='json', auth="public", csrf=False)
    def get_order(self, **post):
        return request.env['sale.order'].sudo().search_read([(['create_uid', '=', request.session.uid])], ['create_date', 'amount_total', ])


    @http.route('/order/form/', auth="public", type="json", csrf=False)
    def order_form(self, md = False, **kw):
        if kw:
            user = request.env['res.users'].sudo().browse([request.session.uid])
            product = request.env['product.template'].sudo().browse([(kw.get('product_id'))])
            company_user = request.env['res.users'].sudo().browse([product.create_uid.id])
            partner = request.env['res.partner'].sudo().browse([company_user.partner_id.id])

            sale = request.env['sale.order'].sudo().create({
                        'partner_id': user.id,
                        # 'product_id': product.id,
                        'state': 'sale',
                        'user_id': partner.id,
                        'invoice_status': 'no',
                        'company_id': company_user.company_id.id,
                        # 'date_order': kw.get('date_order'),
                        'amount_total': kw.get('amount_total'),
                        'amount_tax': kw.get('amount_tax'),
                    })
            # sale_order = request.env['sale.order.line'].sudo().create({
            #             'order_id': sale.id,
            #             'name': kw.get('name'),
            #             'price_total': kw.get('price_total'),
            #             'price_unit': kw.get('price_unit'),
            #             'price_tax': kw.get('price_tax'),
            #             'product_uom_qty': kw.get('product_uom_qty'),
            #             'product_id': product.id

            #             # 'name': product.name,
            #             # 'price_total': int(product.list_price),
            #             # s'price_unit': int(product.list_price),
            #         })


            print("\n\n\n\n\n\n\n\n 3333333333", sale)


# if kw:
#             user = request.env['res.users'].sudo().browse([request.session.uid])
#             product = request.env['product.template'].sudo().browse([(kw.get('product_id'))])
#             company_user = request.env['res.users'].sudo().browse([product.create_uid.id])
#             partner = request.env['res.partner'].sudo().browse([company_user.partner_id.id])

#             sale = request.env['sale.order'].sudo().create({
#                         'partner_id': user.id,
#                         # 'product_id': product.id,
#                         'state': 'sale',
#                         'user_id': partner.id,
#                         'invoice_status': 'no',
#                         'company_id': company_user.company_id.id,
#                         # 'date_order': kw.get('date_order'),
#                         'amount_total': kw.get('amount_total'),
#                     })

#             print("\n\n\n\n\n\n\n\n 3333333333", sale)
