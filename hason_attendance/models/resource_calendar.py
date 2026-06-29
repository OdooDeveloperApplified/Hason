# -*- coding: utf-8 -*-
from odoo import models, fields

class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'
    
    allowed_location_ids = fields.Many2many('hr.work.location',string='Allowed Locations')
    applicable_job_ids = fields.Many2many('hr.job', string='Applicable To')
    
    shift_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('dynamic', 'Dynamic (Day/Night)')
    ], string='Shift Type', default='fixed')
    dynamic_day_shift_id = fields.Many2one('resource.calendar', string="Day Shift Calendar")
    dynamic_night_shift_id = fields.Many2one('resource.calendar', string="Night Shift Calendar")
    night_shift_start_hour = fields.Float(string='Night Shift Start Hour', default=18.0, help='Hour (0-24) after which a check-in is considered night shift (e.g., 18.0 for 6 PM)')

class ResourceCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'

    day_period = fields.Selection(
        selection_add=[
            ('evening', 'Evening'),
            ('night', 'Night'),
        ],
        ondelete={
            'evening': 'set default',
            'night': 'set default',
        }
    )
