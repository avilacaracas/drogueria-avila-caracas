# -*- coding: utf-8 -*-
# from odoo import http


# class RateCurrencyStatic(http.Controller):
#     @http.route('/rate_currency_static/rate_currency_static', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rate_currency_static/rate_currency_static/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rate_currency_static.listing', {
#             'root': '/rate_currency_static/rate_currency_static',
#             'objects': http.request.env['rate_currency_static.rate_currency_static'].search([]),
#         })

#     @http.route('/rate_currency_static/rate_currency_static/objects/<model("rate_currency_static.rate_currency_static"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rate_currency_static.object', {
#             'object': obj
#         })
