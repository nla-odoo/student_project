from odoo import fields, models
import random
import uuid


class ResUser(models.Model):
    _inherit = "res.users"

    course_names = fields.Integer()
    institute_id = fields.Integer()
    fess = fields.Integer('Color Index')
    is_student = fields.Integer(string='student')


class ResCompany(models.Model):
    _inherit = "res.company"

    is_Institute = fields.Integer(string='Institute')


# class productTemplate(models.Model):
#     _inherit = "product.template"

#     def _default_order_ref(self):
#         return str(uuid.uuid4()) + str(random.randint(1, 2000000))

#     cource_id = fields.Integer(string='Institute')
#     order_ref = fields.Char(default=lambda self: self._default_order_ref(), store=True)

    # order_ref = fields.Char(default=lambda self: self._default_order_ref(), store=True)

    # def send_mail_to_student(self, sm, rm, pas):
    #     template_obj = self.env['mail.template'].sudo().search([('name', '=', 'Student')], limit=1)
    #     body = template_obj.body_html % (sm, pas)
    #     if template_obj:
    #         mail_values = {
    #             'body_html': body,
    #             'email_to': rm,
    #             'email_from': sm,
    #         }
    #         self.env['mail.mail'].create(mail_values).send()


# class ResPatner(models.Model):
#     _inherit = "res.patners"

#     course_name = fields.Many2one('product.template')
#     fess = fields.Integer('Color Index')
#     is_student = fields.Integer(string='student')
