from odoo import fields, models, api
from datetime import date, timedelta
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"
    _order = "price desc"


    price = fields.Float(string="Price")
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help="Type is used to separate choices",
        copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    created_date = fields.Date(compute='_compute_created_date', store=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)


    _sql_constraints = [
        ('strictly_positive_offer_price', 'CHECK(price > 0)',
         'The offer price should be greater than 0.')
    ]

    @api.model
    def create(self, vals):
        self.env['estate.property'].browse(vals['property_id']).set_state()
        self.env['estate.property'].browse(vals['property_id']).check_price(vals['price'])
        return super(EstatePropertyOffer, self).create(vals)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.created_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.created_date).days

    @api.depends('property_id.date_availability')
    def _compute_created_date(self):
        for record in self:
            if record.property_id:
                record.created_date = record.property_id.date_availability

    def accept_offer(self):
        for record in self:
            if not record.property_id.accepted_offer:
                record.status = "accepted"
                record.property_id.res_partner_id = record.partner_id
                record.property_id.selling_price = record.price
            else:
                raise UserError('There is already an offer accepted')

        return True

    def reject_offer(self):
        for record in self:
            record.status = "refused"
        return True
