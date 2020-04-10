# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details
{
    'name': "LTS",

    'summary': """
        Loading Transportation System """,

    'version': '1.0',


    'depends': ['base', 'web_dashboard', 'portal', 'sale_management', 'sale_timesheet', 'project', 'sale_renting'],


    'data': [
        'security/ir.model.access.csv',
        'views/project_temp.xml',

    ],
    'demo': ['demo/demo.xml', 'demo/demo_project.xml', 'demo/order_demo.xml', ],
}
