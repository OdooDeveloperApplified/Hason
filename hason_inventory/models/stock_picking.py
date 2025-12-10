from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    vehicle_no = fields.Char(string="Vehicle Number")