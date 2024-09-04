from odoo import models, fields, api

class CustomSalesOrder(models.Model):
    _inherit = 'sale.order'

    consumable_lines = fields.One2many('sale.order.line', 'order_id', domain=[('product_id.type', '=', 'consu')])
    service_lines = fields.One2many('sale.order.line', 'order_id', domain=[('product_id.type', '=', 'service')])

    channel = fields.Char("Multichannel")

    def action_open_charges_wizard(self):
        self.ensure_one()
        return {
            'name': "Extra Charges",
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_sale_order_id': self.id},
        }

class CustomOrderLine(models.Model):
    _inherit = 'sale.order.line'

    charges = fields.Float("Extra Charges")
    


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    special_product = fields.Boolean(string="Special Product")
