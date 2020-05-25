# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Society Managment',
    'summary': 'Society Managment',
    'depends': ['base', 'portal', 'sale_management', 'sale_subscription', 'sale_renting', 'event', 'helpdesk'],
    'data': [
        # 'data/ir_cron_data.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': True,
}
