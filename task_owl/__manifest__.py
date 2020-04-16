# -*- coding: utf-8 -*-
{
    'name': "task_owl",
    # 'depends': ['base', 'portal'],
    'depends': ['base', 'portal', 'sale_management', 'sale'],
    # 'depends': ['base', 'portal'],
    'author': 'Tandel Yograj ',
    'category': 'Category',
    'description': """Manage & track vehicles in business like travells,transportation etc,""",
    'data': ["views/app.xml",
             "views/res_config_settings_views.xml"
             ],
    'installable': True,
    'application': True,
}
