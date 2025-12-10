from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    transport = fields.Char(string="Transport")
    subject = fields.Char(string="Subject")
    po_no = fields.Char(string="PO No.")
    batch_no = fields.Char(string="Batch No.")
    bill_no = fields.Char(string="Bill No.")
    lr_no = fields.Char(string="LR no.")

     # Selection Field
    billing_address_type = fields.Selection([
        ('hason', 'Hason'),
        ('other', 'Other')
    ], string='Billing Address Type', default='hason')

    # Contact Field (Only shows when 'Other' is selected)
    custom_billing_partner_id = fields.Many2one('res.partner', string='Billing Contact')

    # Invoice create thay tyare aa data pass karava mate
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['billing_address_type'] = self.billing_address_type
        invoice_vals['custom_billing_partner_id'] = self.custom_billing_partner_id.id
        return invoice_vals
    
class AccountMove(models.Model):
    _inherit = 'account.move'

    billing_address_type = fields.Selection([
        ('hason', 'Hason'),
        ('other', 'Other')
    ], string='Billing Address Type', default='hason')

    custom_billing_partner_id = fields.Many2one('res.partner', string='Billing Contact')
    
