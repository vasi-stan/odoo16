from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"
    _order = "sequence, name"

    name = fields.Char(string='type', required=True)
    property_ids = fields.One2many("estate.property", 'property_type_id')
    sequence = fields.Integer()
    offer_ids = fields.One2many("estate.property.offer", 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count', store=True)

    @api.model
    def default_get(self):
        res = super(EstatePropertyType, self).default_get(fields)
        return res

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)',
         'The name should be unique.')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)


    def count_offer_action(self):
        return {
            'name': 'Offer Counts',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'estate.property.offer',
            'target': 'current',
        }

