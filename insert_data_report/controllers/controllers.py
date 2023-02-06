# -*- coding: utf-8 -*-
# from odoo import http


# class InsertDataReport(http.Controller):
#     @http.route('/insert_data_report/insert_data_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/insert_data_report/insert_data_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('insert_data_report.listing', {
#             'root': '/insert_data_report/insert_data_report',
#             'objects': http.request.env['insert_data_report.insert_data_report'].search([]),
#         })

#     @http.route('/insert_data_report/insert_data_report/objects/<model("insert_data_report.insert_data_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('insert_data_report.object', {
#             'object': obj
#         })
