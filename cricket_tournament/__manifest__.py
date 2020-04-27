# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Live Cricket Score Board",
    'summary': """cricket tournament""",
    'author': "Vivek Tiwari",
    'depends': ["event", "sale_management", "website_event_sale", "base", "portal", "web_dashboard"],
    'version': '0.1',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/user_detail_view.xml',
        'views/team_detail_view.xml',
        'views/match_detail_view.xml',
        'views/tournament_detail_view.xml',
        'views/prize_caremony_view.xml',
        'views/toss_detail_view.xml',
        'views/score_board_view.xml',
        'views/run_detail_view.xml',
        'views/cricket.xml',
        'views/registration.xml',
        'views/user_template_view.xml',
        'views/dashboard.xml',
        'views/res_config_setting_view.xml',
        'report/report.xml'
    ],
    'demo': [
        'demo/demo.xml'
    ],
}
