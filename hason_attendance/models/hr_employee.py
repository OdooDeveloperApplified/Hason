# -*- coding: utf-8 -*-
from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # manpower_type = fields.Selection([
    #     ('worker', 'Worker'),
    #     ('staff', 'Staff'),
    #     ('employee', 'Employee')
    # ], string='Manpower Type', default='employee', help='Type of manpower as per shift configuration')
