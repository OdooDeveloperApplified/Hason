from odoo import api, fields, models, _
from odoo.exceptions import UserError
from num2words import num2words


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    transport = fields.Char(string="Transport")

    # Code to auto populate the T&C saved in purchase > settings > default terms and conditions in RFQ/PO form view    
    @api.model
    def create(self, vals):
        if not vals.get('notes'):
            enable_terms = self.env['ir.config_parameter'].sudo().get_param('purchase.is_default_purchase_terms')
            if enable_terms == 'True':
                default_terms = self.env['ir.config_parameter'].sudo().get_param('purchase.default_terms_conditions')
                default_terms_html = default_terms.replace('\n', '<br/>').replace('\\n', '<br/>')
                vals['notes'] = default_terms_html
        return super(PurchaseOrder, self).create(vals)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_default_purchase_terms = fields.Boolean(
        string="Default Terms and Conditions",
        config_parameter='purchase.is_default_purchase_terms'
    )

    purchase_terms_conditions = fields.Char(
        string="Default Purchase Terms and Conditions",
        config_parameter='purchase.default_terms_conditions',
    )





