from odoo import http
from odoo.http import request


class OwlController(http.Controller):

    @http.route('/owl_demo', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("loading_transportation_system.demo_template")

    @http.route('/get_partner_data', type='json', auth="public", csrf=False)
    def get_partner(self, **post):
        # return request.env['res.partner'].search([]).mapped('name')
        return http.request.env['res.users'].sudo().search_read([('id' , '=', request.session.uid)], ['name' , 'type' , 'street' , 'zip' , 'city' , 'email' , 'phone'])

    @http.route('/inquirey', type='json', auth="public", csrf=False)
    def get_leads(self, **post):
        partner = request.env.user.partner_id
        return http.request.env['crm.lead'].sudo().search_read([('partner_id', '=', partner.id)], ['name', 'description', 'partner_id', 'type'])
        return request.env['crm.lead'].sudo().search_read([], ['name', 'description', 'partner_id', 'type'])

    @http.route('/lead/form/', auth="public", type="json", csrf=False)
    def lead_form(self, **kw):
        print('\n\n\n\n\n\n\n\n', kw)
        request.env['crm.lead'].sudo().create([{
                    'description': kw.get('description'),
                    'name': kw.get('name'),
                    'user_id': False,
                    'partner_id': request.env.user.partner_id.id
                    }])
        return self.get_leads()
