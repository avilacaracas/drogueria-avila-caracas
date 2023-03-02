
from odoo import models, fields, api

# class rate_currency_static(models.Model):
class datos_computados_convercion_(models.Model):
    _inherit = 'account.move'

    usd_rate = fields.Float(string='USD Rate', default=lambda self: self._get_usd_rate())
    total_rate = fields.Float(string='Total Rate', compute='_compute_total_rate', store=True)
    total_rate_literal = fields.Float(string='Total Rate', compute='_compute_total_rate_lateral', store=True)
    
    @api.depends('amount_untaxed_signed', 'usd_rate')
    def _compute_total_rate(self):
        for record in self:
            print(record.amount_untaxed_signed)
            if record.usd_rate > 0:
                record.total_rate = round(record.amount_untaxed_signed / record.usd_rate,2)
            else:
                record.total_rate = 0


    @api.depends('amount_residual', 'usd_rate')
    def _compute_total_rate_lateral(self):
        for record in self:
            if record.usd_rate > 0:
                record.total_rate_literal = round(record.amount_residual / record.usd_rate,2)
            else:
                record.total_rate_literal = 0
    

    def _get_usd_rate(self):
        
        currency_usd = self.env['res.currency'].sudo().search([('name', '=', 'USD')], limit=1)
        if currency_usd:
            rate = self.env['res.currency.rate'].sudo().search([
                ('currency_id', '=', currency_usd.id),
                ('name', '<=', fields.Date.today())
            ], order='name DESC', limit=1)
            if rate:
                return rate.inverse_company_rate
        return 0.0