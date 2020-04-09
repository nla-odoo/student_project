# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details
{
    'name': "LTS",

    'summary': """
        Loading Transportation System """,

    'version': '1.0',


    'depends': ['base', 'web_dashboard', 'portal', 'sale_management', 'sale_timesheet', 'project', 'sale_renting'],


    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'views/transporters_views.xml',
        # 'views/drivers_views.xml',
        # 'views/inquiries_views.xml',
        # 'views/orders_views.xml',
        # 'views/vehicles_views.xml',
        # 'views/reports.xml',
        # 'views/template.xml',
        'views/project_temp.xml',
        'views/sysparam.xml',

    ],
    'demo': ['demo/demo.xml', 'demo/demo_project.xml', 'demo/order_demo.xml', ],
}
