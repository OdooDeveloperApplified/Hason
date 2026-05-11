from odoo import api, fields, models, _
from odoo.exceptions import UserError
from num2words import num2words


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    transport = fields.Char(string="Transport")





