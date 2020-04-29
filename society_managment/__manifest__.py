# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Society Managment',
    'summary': 'Manage Society as your requirment',
    'depends': ['web_dashboard', 'portal', 'sale_management', 'sale_renting', 'sale_subscription'],
    'data': [
        'security/ir.model.access.csv',
        'views/portal_member.xml'
    ],
    'demo': ['demo/demo.xml'],
    'application': True
}
