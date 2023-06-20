from odoo import api, fields, models, exceptions


class SaleOrder(models.Model):
    _inherit = "sale.order"

    guia_movilizacion = fields.Boolean(default=False, readonly=False)
    journal_id = fields.Many2one('account.journal', string='Journal', required=True,)
      


    def action_confirm_automatic(self):

        res = super(SaleOrder, self).action_confirm()
        
        for order in self:

            warehouse = order.warehouse_id
            
            if warehouse.is_delivery_set_to_done and order.picking_ids:
                for picking in self.picking_ids:
                   
                    picking.action_assign()
                    picking.action_set_quantities_to_reservation()
                    
                    picking.action_confirm()
                    rest = picking.button_validate_automatic()
                    # picking.button_validate()
                    # self.picking_ids.button_validate()
            if rest != True:
   
                return rest
            if warehouse.create_invoice and not order.invoice_ids:
                fact = order._create_invoices()
                
                if self.guia_movilizacion:
                    fact.write({
                        'generarGuia': True,
                        'journal_id' : self.journal_id
                    })

        #
        # generarGuia
            if warehouse.validate_invoice and order.invoice_ids:
                for invoice in order.invoice_ids:
                    invoice.action_post()
                return res
                
                    



class saleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    lot_name = fields.Char(string='lot_name')

    # @api.model
    def _prepare_invoice_line(self, **optional_values):
        
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        :param optional_values: any parameter that should be added to the returned invoice line
        """
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
            'lot_name': self.lot_name
        }
        if self.order_id.analytic_account_id:
            res['analytic_account_id'] = self.order_id.analytic_account_id.id
        if optional_values:
            res.update(optional_values)
        if self.display_type:
            res['account_id'] = False
        return res



class salemoveLine(models.Model):
    _inherit = 'account.move.line'

    lot_name = fields.Char(string='lot_name')


class relacionarLotFact(models.Model):
    _inherit = 'stock.picking'

    tag_modif = fields.Boolean(default=False, readonly=False)

    # def _action_done(self):
    #  

    def button_validate_automatic(self):
        if self.tag_modif == True:
            pass
        else:
            # self.do_unreserve()
            delivery_order_items = self.move_lines
            # se hace yb recorrido a la tabla stock_move
            for item in delivery_order_items:
                if item.move_line_ids:
                    # se recorre stock.move.line
                    for sline in item.move_line_ids:
                        if item.sale_line_id:
                            order_id = self.sale_id.id
                            product_id = item.product_id.id
                            product_uom_qty = sline.product_uom_qty
                            price_unit = item.sale_line_id.price_unit
                            lot_name = sline.lot_id.name
                            # self.do_unreserve()
                            sline.sudo().unlink()
                            new_order_line = {
                                'order_id': order_id,
                                'product_id': product_id,
                                'product_uom_qty': product_uom_qty,
                                'price_unit': price_unit,
                                'lot_name': lot_name,
                            }
                        self.env['sale.order.line'].create(new_order_line)

                    item.sale_line_id.write({'state': 'draft',
                                            'invoice_lines': False,
                                            })
                    item.sale_line_id.sudo().unlink()
                else:
                    item.write({'state': 'draft', })
                    # item.sudo().unlink()
            rests = self.env['stock.move'].search([('picking_id', '=', self.id)])
            self.write({'tag_modif': True})
            self.action_assign()
            self.action_set_quantities_to_reservation()
            for rest in rests:
                if not rest.sale_line_id:
                    rest.write({'state': 'draft', })
                    rest.sudo().unlink()
       
        res = super().button_validate()
        return res  

class Invoice(models.Model):
  _inherit = 'account.move'

#   @api.multi
  def action_print_invoice(self):
    self.ensure_one()
#     # return self.env.ref('sale_order_automation.report_invoice').report_action(self)      


