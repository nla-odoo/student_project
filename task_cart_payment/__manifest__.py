# -*- coding: utf-8 -*-
{
    'name': "task_cart_payment",
    'depends': ['base', 'portal', 'web_dashboard', 'sale_timesheet', 'sale_management', 'sale_renting', 'sale'],
    'author': 'Tandel Yograj ',
    'category': 'Category',
    'description': """Manage & track vehicles in business like travells,transportation etc,""",
    'data': [
             'views/res_config_settings_views.xml',
             'views/homepage_template.xml'
            ],

    'application': True
}
