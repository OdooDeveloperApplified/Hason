from odoo import api, fields, models, _
from odoo.exceptions import UserError


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
    
    vehicle_ids = fields.Many2one('vehicle.master', string="Vehicle No")
    eway_bill_no = fields.Char(string="E-Way Bill No")

    def _prepare_invoice(self):
        vals = super()._prepare_invoice()
        vals.update({
            'billing_address_type': self.billing_address_type,
            'custom_billing_partner_id': self.custom_billing_partner_id.id,
            'vehicle_no': self.vehicle_ids.name if self.vehicle_ids else False,
            'eway_bill_no': self.eway_bill_no,
        })
        return vals

    is_enabled_roundoff = fields.Boolean(string="Apply Roundoff", default=True)
    amount_roundoff = fields.Monetary(string='Amount (Rounded)', compute='_compute_amount_roundoff', store=True)
    amount_total_rounded = fields.Monetary(string='Total (Rounded)', compute='_compute_amount_roundoff', store=True)

    @api.depends('amount_total', 'currency_id', 'is_enabled_roundoff')
    def _compute_amount_roundoff(self):
        for order in self:
            if order.is_enabled_roundoff:
                # Round using standard rounding (>=0.5 up, <0.5 down)
                rounded_total = round(order.amount_total)
                order.amount_roundoff = rounded_total - order.amount_total
                order.amount_total_rounded = rounded_total
            else:
                order.amount_roundoff = 0.0
                order.amount_total_rounded = order.amount_total

    def _create_invoices(self, grouped=False, final=False, date=None):
        if not self.env.user.has_group('hason_sales.group_invoice_approver'):
            raise UserError(_("Invalid Operation: Only Admin/Authorized users can create invoices."))

        return super()._create_invoices(grouped=grouped, final=final, date=date)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    packaging_id = fields.Many2one(
        'product.packaging.master',
        string="Packaging",
        domain="[('product_ids','in',product_id)]"
    )

    packaging_qty = fields.Float(
        string="No. of Packages(Bundle)",
        default=0
    )

    @api.onchange('packaging_id', 'packaging_qty')
    def _onchange_packaging(self):
        for line in self:
            if line.packaging_id and line.packaging_qty:
                qty = line.packaging_id.contained_quantity * line.packaging_qty
                line.product_uom_qty = qty

class VehicleMaster(models.Model):
    _name = 'vehicle.master'

    name = fields.Char(string='Vehicle Number')

class ProductTemplate(models.Model):
    _inherit = "product.template"

    def create(self, vals):
        if not self.env.user.has_group('hason_sales.group_product_creation'):
            raise UserError(_("Invalid Operation: You are not allowed to create products."))

        return super().create(vals)
    
    def write(self, vals):
        if not self.env.user.has_group('hason_sales.group_product_creation'):
            restricted_fields = {
                'name',
                'default_code',
                'list_price',
                'standard_price',
                'uom_id',
                'uom_po_id',
                'type',
            }

            if restricted_fields.intersection(vals.keys()):
                raise UserError(_("Invalid operation: You are not allowed to edit Product details."))

        return super().write(vals)

class CrmLead(models.Model):
    _inherit = "crm.lead"

    def action_new_quotation(self):
        if not self.env.user.has_group('hason_sales.group_quotation_creation'):
            raise UserError(_("Invalid Operation: You are not allowed to create quotations from CRM."))

        return super().action_new_quotation()


