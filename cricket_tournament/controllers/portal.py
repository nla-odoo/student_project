# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home
import json
from werkzeug import urls
from . import checksum
import datetime


class Home(Home):
    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('cricket_tournament.group_organizer'):
            return '/dashboard/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_portal'):
            return '/yourhomepage'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
            return '/web/'
        return super(Register, self)._login_redirect(uid, redirect=redirect)


class Register(http.Controller):
    @http.route('/userregister/', auth="public", website=True, type="http", csrf=False)
    def customer_register(self, **kw):
        currency = request.env['res.currency'].sudo().search([])
        return request.render('cricket_tournament.organizer', {'currency': currency})

    @http.route('/userregister/form', auth="public", method="post", type="http", csrf=False)
    def register(self, **post):
        group_id_name = [(6, 0, [request.env.ref('cricket_tournament.group_organizer').id, http.request.env.ref('base.group_portal').id])]
        currency_name = post.get('currency')
        currency = request.env['res.currency'].sudo().search([('name', '=', currency_name)], limit=1)
        partner = request.env['res.partner'].sudo().create({
            'name': post.get('username'),
            'email': post.get('email')
            })
        company = request.env['res.company'].sudo().create({
            'name': post.get('companyname'),
            'partner_id': partner.id,
            'currency_id': currency.id,
            })
        request.env['res.users'].sudo().create({
            'partner_id': partner.id,
            'login': post.get('username'),
            'password': post.get('password'),
            'company_id': company.id,
            'company_ids': [(4, company.id)],
            'groups_id': group_id_name,
            })
        return http.local_redirect('/web/login')


class User_Portal(http.Controller):

    @http.route('/dashboard/', auth='public', type="http", website=True, csrf=False)
    def dashBoard(self, **kw):
        DashBoard = request.env['tournament.detail'].sudo().search([])
        # print ("\n\n\n\n\n", DashBoard)
        return request.render('cricket_tournament.dashboard', {
            'dashboards': DashBoard.search([])
            })

    @http.route(['/yourhomepage/', "/my"], auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        Tournament = request.env['tournament.detail'].sudo().search([])
        return request.render('cricket_tournament.sub', {
            'tournaments': Tournament.search([])
            })

    @http.route('/match_detail/', auth='public', type="http", website=True, csrf=False)
    def MatchDetail(self, **kw):
        Match = request.env['match.detail'].sudo().search([])
        return request.render('cricket_tournament.match', {
            'matchs_shedule': Match.search([])
            })

    @http.route(['/tournament_shedule/<int:tournament_id>'], auth='public', type='http', website=True, csrf=False)
    def shedule(self, tournament_id=None, **kw):
        if tournament_id:
            tournament = request.env['tournament.detail'].sudo().browse([tournament_id])
            match_shedule = request.env['match.detail'].sudo().search([('match_id', '=', int(tournament.id))])
        return request.render('cricket_tournament.match', {
            'matchs_shedule': match_shedule
            })

    @http.route(['/match_summary/<int:match_id>'], auth="public", type="http", website=True, csrf=False)
    def MatchScoreBoard(self, match_id=0, **kw):
        if match_id:
            Match = request.env['match.detail'].sudo().browse([match_id])
            print ('\n\n\n\n\n', Match)
            toss = request.env['toss.detail'].sudo().search([('id', '=', int(Match.id))])
            print ('\n\n\n\n\n\n', toss)
            ScoreBoard = request.env['score.board'].sudo().search([('id', '=', int(toss.id))])
        return request.render('cricket_tournament.match_form', {
            'tosss': toss,
            'scoreboards': ScoreBoard,
            'matchs': Match,
            })

    @http.route(['/match_detail/<int:match_id>'], auth='public', type='http', website=True, csrf=False)
    def TeamDetail(self, match_id=0, **kw):
        if match_id:
            Match = request.env['match.detail'].sudo().browse([match_id])
            Team1 = request.env['team.detail'].sudo().search([('id', '=', Match.team1name_id.id)])
            Team2 = request.env['team.detail'].sudo().search([('id', '=', Match.team2name_id.id)])
        return request.render('cricket_tournament.match_form', {
            'team1': Team1,
            'team2': Team2,
            'matchs': Match,
            })

    @http.route('/demo/<int:payment>', auth='public', type="http", csrf=False, website=True)
    def demo(self, payment=None, **kw):
        if payment:
            Payment = request.env['match.detail'].sudo().browse([payment])
        return request.render('cricket_tournament.payment', {
            'payments': Payment
            })

    @http.route('/payment/', auth='public', type="http", website=True, csrf=False)
    def demo1(self, **kw):
        order = request.env['match.detail'].sudo().browse([int(kw.get('payment_id'))])
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        data_dict = {
            'MID': "amitgo59443067266036",
            'WEBSITE': 'WEBSTAGING',  # fix value
            'ORDER_ID': order.order_id,
            'CUST_ID': str(request.uid),
            'INDUSTRY_TYPE_ID': 'Retail',  # fix value
            'CHANNEL_ID': 'WEB',  # furlsix value
            'TXN_AMOUNT': str(float(order.amount)),
            'CALLBACK_URL': urls.url_join(base_url, '/paytm_response')
        }
        data_dict['CHECKSUMHASH'] = checksum.generate_checksum(data_dict, "bQfzzkKzeCbR7jOl")
        data_dict['redirection_url'] = "https://securegw-stage.paytm.in/order/process"
        return request.make_response(json.dumps(data_dict))

    @http.route('/paytm_response/', method="post", auth="public", type="http", website=True, csrf=False)
    def demo2(self, **post):
        checksum_result = checksum.verify_checksum(post, "bQfzzkKzeCbR7jOl", post.get('CHECKSUMHASH'))
        payment = request.env['match.detail'].sudo().search([('order_id', '=', post.get('ORDERID'))])
        if checksum_result:
            if post.get('STATUS') == "TXN_SUCCESS":
                payment.write({
                    'payment_status': 'done',
                    'acquirer_ref': post.get('TXNID'),
                    'transaction_date': datetime.date.today(),
                    })
            elif post.get('STATUS') == "TXN_FAILURE":
                payment.write({
                    'payment_status': 'fail',
                    'transaction_date': datetime.date.today()
                    })
            elif post.get('STATUS') == "PENDING":
                payment.write({
                    'payment_status': 'pending',
                    'transaction_date': datetime.date.today()
                    })
        return request.render('cricket_tournament.payment_form', {'payment': payment})
