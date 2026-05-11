from odoo import api, fields, models,_
from odoo.exceptions import UserError
from num2words import num2words

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

    def action_post(self):
        if self.move_type == 'out_invoice':
            if not self.env.user.has_group('hason_sales.group_invoice_approver'):
                raise UserError(_("Invalid Operation: You are not allowed to confirm/post invoices. Contact your Administrator for the access."))

        return super().action_post()
    
    def amount_to_words_indian(self):
        self.ensure_one()

        amount = self.amount_total
        rupees = int(amount)
        paise = int(round((amount - rupees) * 100))

        words = num2words(rupees, lang='en_IN').title() + ' Rupees'

        if paise:
            words += ' and ' + num2words(paise, lang='en_IN').title() + ' Paise'

        return words