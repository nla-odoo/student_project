# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Society Managment',
    'summary': 'Society Managment',
    'depends': ['base', 'portal', 'sale_management', 'sale_subscription', 'sale_renting', 'account_accountant', 'event', 'helpdesk'],
    'data': [
        'security/security.xml',
        # 'data/ir_cron_data.xml',
        'views/templates.xml',
        'views/society_managment_view.xml',
    ],
    'demo': ['demo/demo.xml'],
    'installable': True,
    'application': True,
}
