from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"
    _order = "name"

    name = fields.Char(string='Name', required=True)
    property_ids = fields.Many2many("estate.property", string="Name")
    color = fields.Integer()

    _sql_constraints = [
        ('unique_property_tag', 'UNIQUE(name)',
         'The name should be unique.')
    ]