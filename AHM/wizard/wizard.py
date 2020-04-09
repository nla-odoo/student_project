from odoo import models, fields


class Stock(models.TransientModel):
    _name = 'ahm.stocks.transient'
    _description = "AHM Stock"

    stock_id = fields.Char("stock id")
    name = fields.Char("name")
    comp = fields.Char("comp")

    def get_default_stock(self):
        self.env['ahm.stock'].create({
            'name': self.stock_id,
            'comp': self.comp})
