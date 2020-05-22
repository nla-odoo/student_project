from odoo import fields, models


class ResUser(models.Model):
    _inherit = "res.users"

    course_names = fields.Integer()
    fess = fields.Integer('Color Index')
    is_student = fields.Integer(string='student')

    def send_mail_to_student(self, sm, rm, pas):
        template_obj = self.env['mail.template'].sudo().search([('name', '=', 'Student')], limit=1)
        body = template_obj.body_html % (sm, pas)
        if template_obj:
            mail_values = {
                'body_html': body,
                'email_to': rm,
                'email_from': sm,
            }
            self.env['mail.mail'].create(mail_values).send()


# class ResPatner(models.Model):
#     _inherit = "res.patners"

#     course_name = fields.Many2one('product.template')
#     fess = fields.Integer('Color Index')
#     is_student = fields.Integer(string='student')
