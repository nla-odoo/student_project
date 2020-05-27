# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'OWL_DEMO',
    'summary': 'OWL_DEMO',
    'depends': ['base', 'portal', 'rating', 'sale_management', 'im_livechat'],
    'data': [
        'views/templates.xml',
        'views/homepage_view.xml',
    ],
    'installable': True,
    'application': True,
}
