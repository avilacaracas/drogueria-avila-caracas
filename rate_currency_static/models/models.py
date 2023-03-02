# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rate_currency_static(models.Model):
#     _name = 'rate_currency_static.rate_currency_static'
#     _description = 'rate_currency_static.rate_currency_static'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
