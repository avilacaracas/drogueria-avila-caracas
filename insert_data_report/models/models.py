# -*- coding: utf-8 -*-

from odoo import models, fields, api


class barcodeLot(models.Model):

    _inherit= 'stock.production.lot'

    barcodes  = fields.Char('Codigo de Barras', compute='_codigo_de_barra')

    def _codigo_de_barra(self):
        print(self)
        for prod_lot in self:
            prod_lot.barcodes = prod_lot.product_id.barcode


class typeClientEmpleyer(models.Model):
    _inherit= 'res.partner'

    is_employee  = fields.Boolean(string='Es Empleado')
    is_client = fields.Boolean(string='Es Cliente')
    is_provider  = fields.Boolean(string='Es Proveedor')
