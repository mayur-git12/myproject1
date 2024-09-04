from odoo import models, fields, api

class SaleOrderWizard(models.TransientModel):
    _name = 'sale.order.wizard'
    _description = 'sale order wizard'

    sale_order_id = fields.Many2one('sale.order', string="Sale Order", required=True)
    product_id = fields.Many2one('product.product', string="Product", required=True)
    other_amount = fields.Float(string="Other Amount", required=True)

    def apply_extra_charges(self):
        sale_order = self.sale_order_id
        if sale_order:
            value={
                'order_id' :sale_order.id,
                'product_id':self.product_id.id,
                'price_unit':self.other_amount,

                }
            self.env['sale.order.line'].create(value)
            return{'type':'ir.actions.act_window_close'}







