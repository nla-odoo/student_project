# -*- coding: utf-8 -*-
{
    'name': "fleet_tracking",
    'depends': ['base', 'portal', 'web_dashboard', 'sale_timesheet', 'sale_management', 'sale_renting', 'sale'],
    'author': 'Tandel Yograj ',
    'category': 'Category',
    'description': """Manage & track vehicles in business like travells,transportation etc,""",
    'data': ['security/fleet_security.xml',
             'security/ir.model.access.csv',
             'data/data.xml',
             'wizard/cancelled_reason.xml',
             'reports/reports.xml',
             'views/vehicle_brand_view.xml',
             'views/fleet_vehicle_view.xml',
             'views/fleet_vehicle_contract_view.xml',
             'views/fleet_cost_view.xml',
             'views/fleet_odometer_view.xml',
             'views/fleet_dashboard_view.xml',
             'views/registration_template.xml',
             'views/res_config_settings_views.xml',
             'views/homepage_template.xml',
             'views/res_users_views.xml'],

    'demo': ['demo/demo.xml'],
    'application': True
}
