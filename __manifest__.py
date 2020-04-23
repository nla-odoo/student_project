# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "CMT",
    'summary': "Construction Material Testing",
    'description': """
        Provide Construction Material Testing Releted Information of Different Laboratories
    """,
    'author': "JS",
    'depends': ['sale_timesheet'],
    'data': [
        'views/templates.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
