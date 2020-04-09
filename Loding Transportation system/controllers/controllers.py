# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http


class Lts(http.Controller):

    @http.route('/lts/lts/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/lts/lts/agent/', auth='public', website=True, csrf=False)
    def agentdata(self, **kw):
        agents = http.request.env['agent.agent'].search([])
        return http.request.render('lts.agentdata', {'agents': agents})

    @http.route(['/lts/lts/createform/', '/lts/lts/editform/<model("agent.agent"):editid>'], auth='public', website=True, csrf=False)
    def createform(self, editid=None):
        agent = None
        if editid:
            agent = http.request.env['agent.agent'].browse([editid.id])
        return http.request.render('lts.createdata', {'agent': agent})

    @http.route(['/lts/lts/data/', '/lts/lts/data/<int:editid>'], auth='public', website=True, csrf=False, method='post')
    def create(self, editid=None, **post):
        if post:
            if editid:
                http.request.env['agent.agent'].browse([editid]).write({
                    'name': post.get('name'),
                    'email': post.get('email'),
                    'contactnumber': post.get('contactnumber'),
                    'gender': post.get('gender'),
                    'address': post.get('address'),
                    'city': post.get('city'),
                    'state': post.get('state'),
                    })
            else:
                http.request.env['agent.agent'].create({
                    'name': post.get('name'),
                    'email': post.get('email'),
                    'c_number': post.get('c_number'),
                    'gender': post.get('gender'),
                    'address': post.get('address'),
                    'city': post.get('city'),
                    'state': post.get('state'),
                    })
        return http.request.redirect('/lts/lts/agent/')

    @http.route('/lts/lts/delete/<model("agent.agent"):deleteid>', auth='public', website=True, csrf=False)
    def delete(self, deleteid=None):
        if deleteid:
            deleteid.unlink()
        return http.request.redirect('/lts/lts/agent/')

    @http.route('/lts/inquirey', auth='public', website=True, csrf=False)
    def inquireydata(self, **kw):
        inq = http.request.env['inquirey.inquirey.demo'].search([])
        return http.request.render('lts.inquireyTemp', {
            'inq': inq,
            })

    @http.route(['/lts/inquirey/createform', '/lts/inquirey/editform/<model(inquirey.inquirey.demo):editid>'], auth='public', website=True, csrf=False)
    def inquireycreateform(self, editid=None):

        if editid:
            enqe = http.request.env['inquirey.inquirey.demo'].browse([editid.id])
        return http.request.render('lts.inquireyformtemp', {
            'enqe': enqe,
            })

    @http.route('/lts/inquirey/create/', auth='public', website=True, csrf=False)
    def inquireycreate(self, **post):
        if post:
            http.request.env['inquirey.inquirey.demo'].create({
                'source_add': post.get('source_add'),
                'desti_add': post.get('desti_add'),
                'KM': post.get('KM'),
                'duration': post.get('duration'),
                'vehicle_type': post.get('vehicle_type'),
                'vehicle_capacity': post.get('vehicle_capacity'),
                'vehicle_speed': post.get('vehicle_speed'),
                'date_start': post.get('date_start'),
                'date_stop': post.get('date_stop'),
            })
        return http.request.redirect('/lts/inquirey')

    @http.route('/lts/inquirey/delete/<model("inquirey.inquirey.demo"):deleteid>', auth='public', website=True, csrf=False)
    def deleteinquirey(self, deleteid=None):
        if deleteid:
            deleteid.unlink()
        return http.request.redirect('/lts/inquirey')
