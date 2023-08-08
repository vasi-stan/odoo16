from odoo import fields, models, api
from odoo import Command

class EstateProperty(models.Model):
    _inherit = 'estate.property'



    def sold_property(self):
        print("self.res_partner_id", self.res_partner_id.id)
        in_invoices = self.env['account.move'].create([{
            'name': 'sell property',
            'move_type': 'out_invoice',
            'partner_id': self.res_partner_id.id,
            'date': '2023-01-01',
            'invoice_date': '2017-01-01',
            'invoice_line_ids': [Command.create({
                'price_unit': self.selling_price * 6 /100 + 100,
                'quantity': 1
            })]
        }])
        in_invoices.action_post()
        return super(EstateProperty, self).sold_property()