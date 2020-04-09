{
    'name': 'Tenants Management system',
    'summary': 'manage the tenants',
    'author': "Harjindar Kaur",
    'depends': ['web_dashboard', 'portal', 'sale_management', 'project', 'sale_renting'],
    'demo': [
        'demo/demo.xml',
        'demo/products.xml'
    ],
    'data': [
        'security/rmssecurity.xml',
        'security/ir.model.access.csv',
        'views/expenses_inquiry_view.xml',
        'views/training_view.xml',
        'views/rms_template.xml',
        'views/tenant_template.xml',
        'views/res_config_setting.xml',
        'views/order_sale_template.xml',
    ],
}
