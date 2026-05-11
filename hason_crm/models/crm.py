from odoo import api, fields, models
import logging
import math

_logger = logging.getLogger(__name__)

class CrmTemplate(models.Model):
    _inherit = 'crm.lead'

    industry_ids = fields.Many2one('commercial.industry', string="Industry")

class CommercialIndustry(models.Model):

    _name = 'commercial.industry'
    _description = 'Link commercial industry records to crm lead'

    name = fields.Char(string="Industry Name")

   