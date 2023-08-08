from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"

    _order = "id desc"

    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", default=date.today() + relativedelta(months=+3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Type is used to separate choices")
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('canceled', 'Canceled')],
        help="Type is used to separate choices")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    res_partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    res_users_id = fields.Many2one('res.users', string='Salesman', index=True,
                                   tracking=True, default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string=" ")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(string="Total area", compute='_compute_total_area')
    best_price = fields.Float(string='Best offer', compute='_compute_best_price')
    accepted_offer = fields.Boolean(compute='_compute_accepted_offer', store=True)

    _sql_constraints = [
        ('strictly_positive_expected_price', 'CHECK(expected_price > 0)',
         'The expected price should be strictly positive.'),
        ('positive_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price should be positive.')
    ]

    def set_state(self):
        self.state = "offer_received"


    def check_price(self, price):
        if self.offer_ids:
            highest_price = max(self.offer_ids.mapped('price'))
            if price < highest_price:
                raise UserError(f"The offer must be higher than {highest_price}")

    @api.ondelete(at_uninstall=False)
    def unlink(self):
        for record in self:
            if self.state == 'new' or self.state == 'canceled':
                raise UserError(f"You cannot delete a {self.state} property")
                print(f"You cannot delete a {self.state} property")




    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0


    @api.depends('offer_ids.status')
    def _compute_accepted_offer(self):
        contor = False
        for record in self:
            for l in record.offer_ids:
                if l.status == 'accepted':
                    contor = True
        if not contor:
            record.accepted_offer = False
            self.selling_price = 0
            self.res_partner_id = ""
        else:
            record.accepted_offer = True



    @api.onchange('garden')
    def _onchange_garden_area(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def sold_property(self):
        for record in self:
            if record.state != 'canceled':
                record.state = 'sold'
            else:
                raise UserError('Canceled properties cannot be sold')
        return True

    def cancel_property(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'canceled'
            else:
                raise UserError('Sold properties cannot be canceled')
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_price(self):
        for record in self:
            if not float_utils.float_is_zero(record.selling_price, 3):
                if float_utils.float_compare(record.selling_price, record.expected_price * 0.9, 3) == -1:
                    raise ValidationError('The selling price cannot be lower than 90% of the expected price')