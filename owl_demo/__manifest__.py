# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Owl Demo',
    'summary': 'Owl Demo',
    'depends': ['base', 'portal', 'sale_management', 'mail'],
    'data': [
        'views/templates.xml',
        'views/views_email_send.xml',

    ],
    'installable': True,
    'application': True,
}
