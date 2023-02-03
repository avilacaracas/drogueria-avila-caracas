# -*- coding: utf-8 -*-

from odoo import models, fields, api




class account_edit_report(models.Model):
    _name = 'account_edit_report.notas_pagar'
   

    numero = fields.Char(string='NNuemero de cuenta',required=True)
    banco = fields.Many2one('res.bank', string='Selecion de Bancos',required=True)
    cuenta = fields.Selection([('Ahorro', 'Ahorro'), ('Corriente', 'Corriente'),('Cuenta Verde', 'Cuenta Verde')], string='Cuentas', required=True) 
    status = fields.Boolean(default=True)
    

  

class datos_computados_convercion(models.Model):
    _inherit = 'account.move'


    usd = fields.Float(compute="_compute_usd")
    totalusd = fields.Float(compute="_compute_usd")
    advisor  = fields.Many2one(comodel_name='res.partner',inverse_name='id',domain="[('is_advisor','=','1')]" ,string='Asesor de venta')

    def action_post(self):
        rec = super().action_post()
        
        
        
        if self.invoice_origin:

            orders = self.env['sale.order'].search([('name','=',self.invoice_origin)])
            for order in orders:
                self.write({'advisor': order.advisor,})
        
        return rec
    



    def _compute_usd(self):
        uds= self.env['res.currency'].sudo().search([('name','=','USD')])
        rates=  self.env['res.currency.rate'].sudo().search([('currency_id','=',int(uds.id)),('name','=',self.invoice_date)])
        self.usd = rates.inverse_company_rate
        
        self.totalusd = round(self.amount_residual * rates.rate, 2)
      
       


class clientAcesorVenta(models.Model):
    _inherit= 'res.partner'

    is_advisor  = fields.Boolean(string='Es asesor de venta')
    is_laboratory  = fields.Boolean(string='Es laboratorio')

class orderAcesorVenta(models.Model):
    _inherit= 'sale.order'

    advisor  = fields.Many2one(comodel_name='res.partner',inverse_name='id',domain="[('is_advisor','=','1')]" ,string='Asesor de venta')
    



class laboratory(models.Model):
    _inherit= 'product.template'

    laboratory = fields.Many2one(comodel_name='res.partner',inverse_name='id',domain="[('is_laboratory','=','1')]" ,string='Laboratorios')

class bankReference(models.Model):

    _inherit= 'account.bank.statement'

    _sql_constraints = [('name', 'unique(name)', 'El Numero de Referencia debe ser unico'),]

class laboratoryQuant(models.Model):

    _inherit= 'stock.quant'

    laboratory = fields.Many2one(related='product_tmpl_id.laboratory')

class laboratorioStockMove(models.Model):
    _inherit="stock.move"

    laboratory = fields.Many2one(related='product_tmpl_id.laboratory')

class laboratorioStockMove(models.Model):
    _inherit="stock.move.line" 

    product_tmpl_id = fields.Many2one(
        'product.template', 'Product Template',
        related='product_id.product_tmpl_id',
        help="Technical: used in views")

    laboratory = fields.Many2one(related='product_tmpl_id.laboratory')




