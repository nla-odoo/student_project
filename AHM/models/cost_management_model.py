from odoo import models, fields, api


class TotalCharges(models.Model):
    _name = 'ahm.total.charges'
    _description = "AHM Total Charges"

    app_id = fields.Many2one(comodel_name="ahm.appointment", ondelete="cascade")
    company_id = fields.Many2one('res.company',  default=lambda self: self.env.company)
    medicine_charges = fields.Integer(string="Medicine Charges", required=True)
    total_bill = fields.Float(compute="_compute_total")
    visiting_charges = fields.Integer("Visiting Charges", default=450)

    @api.depends('medicine_charges', 'visiting_charges')
    def _compute_total(self):
        for ahm in self:
            ahm.total_bill = ahm.medicine_charges + ahm.visiting_charges
