from odoo import fields, models


class ResUser(models.Model):
    _inherit = "res.users"

    course_name = fields.Many2one('product.template')
    fess = fields.Integer('Color Index')
    is_student = fields.Integer(string='student')


# class ResPatner(models.Model):
#     _inherit = "res.patners"

#     course_name = fields.Many2one('product.template')
#     fess = fields.Integer('Color Index')
#     is_student = fields.Integer(string='student')
