from odoo import api, fields, models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_id = fields.Many2one('sale.order', string="")
    related_sale_service_id = fields.Many2one('services.fleet', string='service', readonly=True,
                                              related='sale_id.service_id', store=True)
    services_id = fields.Many2one('services.fleet', string='service')
    srv_id = fields.Many2one('services.fleet', string='service')

    # def action_assign(self):
    #     res = super(StockPicking, self).action_assign()
    #     for picking in self:
    #         sale_order = picking.sale_id
    #         if sale_order:
    #             picking.services_id = picking.sale_id.service_id'

    def action_confirm(self):
        res = super(StockPicking, self).action_confirm()
        print("fgbdvnvcwrv\n", res)
        for picking in self:
            print("picking::::::::::::", picking)
            sale_order = picking.sale_id
            print("sale_order/////////////////", sale_order)
            if sale_order:
                print("sale_order///////////////////", sale_order)
                picking.services_id = picking.sale_id.service_id
                print("picking.srv_id,,,,,,,,,,,,,,,,,,,,,,,,,", picking.services_id)


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_new_picking_values(self):
        vals = super(StockMove, self)._get_new_picking_values()
        print("vals", vals)
        vals['srv_id'] = self.sale_line_id.order_id.service_id.id
        print("vals['srv_id'] ", vals['srv_id'])
        return vals

    # def _prepare_invoice_line(self, order_line):
    #     name = order_line.product_id.get_product_multiline_description_sale()
    #     return {
    #         'product_id': order_line.product_id.id,
    #         'quantity': order_line.qty if self.amount_total >= 0 else -order_line.qty,
    #         'discount': order_line.discount,
    #         'price_unit': order_line.price_unit,
    #         'name': name,
    #         'tax_ids': [(6, 0, order_line.tax_ids_after_fiscal_position.ids)],
    #         'product_uom_id': order_line.product_uom_id.id,
    #     }

