from odoo import models, fields, api

class ProductPackagingMaster(models.Model):
    _name = "product.packaging.master"
    _description = "Product Packaging Master"

    name = fields.Char(string="Packaging Name", required=True)

    contained_quantity = fields.Float(
        string="Quantity per Package",
        required=True,
        help="Example: 230 means 230 grams per package"
    )

    uom_id = fields.Many2one(
        'uom.uom',
        string="UoM",
        required=True
    )

    product_ids = fields.Many2many(
        'product.product',
        'product_packaging_master_rel',
        'packaging_id',
        'product_id',
        string="Applicable Products"
    )

    active = fields.Boolean(default=True)