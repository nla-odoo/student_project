{
    'name': "Animal Health Monitoring",
    'version': '1.0',
    'depends': ['web_dashboard', 'portal', 'sale_timesheet', 'sale_management'],
    'author': "Animal Health Monitorig",
    'category': 'Category',
    'description': """
    ahm@gmail.com
    """,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'reports/reports.xml',
        'views/ahm_payment_view.xml',
        'views/cost_management_view.xml',
        'views/inventory_view.xml',
        'views/appointment_views.xml',
        'views/organization_views.xml',
        'views/payment_view.xml',
        'views/userregistration_view.xml',
        'views/homepage_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
