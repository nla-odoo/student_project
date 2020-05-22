from odoo import http
from odoo.http import request
import logging
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home
from odoo.exceptions import UserError


class Home(Home):
    # pass
    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
            return '/web/'
        if request.session.uid:
            user = request.env['res.users'].sudo().browse(request.session.uid)
            if user.has_group('base.group_portal'):
                # if user.is_student:
                #     return '/owl_demo_student'
                return'/transporter_register'
        return super(OwlController, self)._login_redirect(uid, redirect=redirect)


class OwlController(http.Controller):

    @http.route('/owl_demo', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("loading_transportation_system.demo_template2")

    @http.route('/get_partner_data', type='json', auth="public", csrf=False)
    def get_partner(self, **post):
        partner = request.env.user.partner_id
        # return request.env['res.partner'].search([]).mapped('name')
        return http.request.env['res.partner'].sudo().search_read([('id' , '=', partner.id)] ,['name' , 'type' , 'street' , 'city' , 'email' , 'phone'])

    @http.route('/inquirey', type='json', auth="public", csrf=False)
    def get_leads(self, **post):
        partner = request.env.user.partner_id
        return http.request.env['crm.lead'].sudo().search_read([('partner_id', '=', partner.id)], ['name', 'description', 'partner_id', 'type'])
        return request.env['crm.lead'].sudo().search_read([], ['name', 'description', 'partner_id', 'type'])

    @http.route('/transporters', type='json', auth="public", csrf=False)
    def get_transporters(self, **post):
        return request.env['res.company'].sudo().search_read([], ['name', 'email', 'phone'])

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

    @http.route('/owl_demo_ragi', type='http', auth="public", csrf=False, website=True)
    def demo_ragi(self, **post):
        if request.session.uid:
            if request.env['res.company'].browse(request.session.uid):
                return http.request.render("loading_transportation_system.demo_template")
        return http.request.render("loading_transportation_system.demo_ragi")

    @http.route('/transporter_register', type='http', auth="public", csrf=False, website=True)
    def transporter_register(self, **post):
        if request.session.uid:
            if request.env['res.company'].browse(request.session.uid):
                return http.request.render("loading_transportation_system.display_template")
        return http.request.render("loading_transportation_system.transporter_template")

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

            request.env["res.users"].sudo().create({
                'login': form_data.get("name"),
                'password': form_data.get('password'),
                'name': form_data.get('name'),
                'company_id': company.id,
                'company_ids': [(4, company.id)],
                'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
            })
        return {'resulrt': request.env['res.currency'].sudo().search_read([], ['id',  'name'])}

    @http.route(['/my/transporter_register'], type='json', auth="public", website=True, methods=['GET', 'POST'])
    def transporter_registration(self, form_data=False, **kw):
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

            request.env["res.users"].sudo().create({
                'login': form_data.get("name"),
                'password': form_data.get('password'),
                'name': form_data.get('name'),
                'company_id': company.id,
                'company_ids': [(4, company.id)],
                'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
            })
        return {'resulrt': request.env['res.currency'].sudo().search_read([], ['id',  'name'])}

    @http.route('/vehicle', type='json', auth="public", csrf=False)
    def get_vehicle(self, **post):
        # partner = request.env.user.partner_id
        # return http.request.env['crm.lead'].sudo().search_read([('partner_id', '=', partner.id)], ['name', 'description', 'partner_id', 'type'])
        return request.env['product.template'].sudo().search_read([], ['name', 'description', ])

    @http.route('/vehicle/form/', auth="public", type="json", csrf=False)
    def vehicle_form(self, **kw):
        # print('\n\n\n\n\n\n\n\n', kw)
        request.env['product.template'].sudo().create([{
                    'description': kw.get('description'),
                    'name': kw.get('name'),
                    'user_id': False,
                    'partner_id': request.env.user.partner_id.id
                    }])
        return self.get_vehicle()
