# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class OwlController(http.Controller):
    @http.route('/owl_demo', type='http', auth="public", csrf=False)
    def owl_demo(self, **post):
        return http.request.render("OWL_DEMO.demo_template")

    @http.route('/owl_demo_rating', type='json', auth="user", csrf=False)
    def owl_rating(self, **kw):
            rating = request.env['rating.rating']
            pm = request.env['rating.rating'].sudo().create([{
                'rating': int(kw.get('rating')),
                'feedback': kw.get('feedback'),
                'res_id': http.request.env['product.product'].sudo().browse(int(kw['res_id'])),
                # 'res_model': http.request.env['product.product'].sudo().check_object_name(kw['res_model'])
                # 'res_model': http.request.env['rating.rating'].sudo().browse(['res_id']).name_get()
                'res_model': http.request.env[rating.res_model].sudo().browse(rating.res_id)
            }])
            print("\n\n\n\n\n\n\n\n\n", pm.res_id)
            print("\n\n\n\n\n\n\n\n\n", pm.res_model)
            print("\n\n\n\n\n\n\n\n\n", pm.rating)
            print("\n\n\n\n\n\n\n\n\n", pm.feedback)
            return {"pm": pm}
# browse(rating.res_id)

    @http.route('/get_partner_data', type='json', auth="public", csrf=False)
    def get_partner(self, **post):
        return request.env['res.partner'].search([]).mapped('name')

    @http.route('/feedback', type='json', auth="user", csrf=False)
    def get_feedback(self, **post):
        partner = request.env.user.partner_id
        return http.request.env['rating.rating'].sudo().search_read([('partner_id', '=', partner.id)], ['feedback',  'res_id', ])




# rate = int(kwargs.get('rate'))
#         assert rate in (1, 5, 10), "Incorrect rating"
#         rating = request.env['rating.rating'].sudo().search([('access_token', '=', token)])
#         if not rating:
#             return request.not_found()
#         record_sudo = request.env[rating.res_model].sudo().browse(rating.res_id)
#         record_sudo.rating_apply(rate, token=token, feedback=kwargs.get('feedback'))
#         lang = rating.partner_id.lang or get_lang(request.env).code
#         return request.env['ir.ui.view'].with_context(lang=lang).render_template('rating.rating_external_page_view', {
#             'web_base_url': request.env['ir.config_parameter'].sudo().get_param('web.base.url'),
#             'rating': rating,
#         })
    # @http.route('/services/form', auth="user", type="json", csrf=False)
    # def services_form(self, **kw):
    #     print('\n\n\n\n\n\n\n\n', kw)
    #     pm = request.env['product.product'].sudo().create([{
    #                 'name': kw.get('name'),
    #                 'purchase_ok': kw.get('purchase_ok'),
    #                 'sale_ok': kw.get('sale_ok'),
    #                 'type': kw.get('type'),
    #                 'standard_price': kw.get('standard_price'),
    #                 'list_price': kw.get('list_price'),
    #                 }])
    #     # return http.local_redirect('/owl_demo')
    #     return {"pm": pm}