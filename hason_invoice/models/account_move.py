from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    billing_address_type = fields.Selection([
        ('hason', 'Hason'),
        ('other', 'Other')
    ], string='Billing Address Type', default='hason')

    custom_billing_partner_id = fields.Many2one('res.partner', string='Billing Contact')
    vehicle_no = fields.Char(string="Vehicle No")
    acknowledgement_name = fields.Char(string='Acknowledgement Name')
    eway_bill_no = fields.Char(string="E-Way Bill No")