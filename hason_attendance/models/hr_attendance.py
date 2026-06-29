# -*- coding: utf-8 -*-
from odoo import models, fields, api
import pytz
from odoo.addons.resource.models.utils import Intervals


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    applied_shift_id = fields.Many2one('resource.calendar', string='Applied Shift', help='The shift applied for this attendance based on dynamic shift rules.')
    employee_calendar_id = fields.Many2one('resource.calendar', related='employee_id.resource_calendar_id', string='Assigned Working Schedule', store=True, help='The actual working schedule assigned to the employee at the time of check-in.')
    is_half_day = fields.Boolean(string='Half Day', default=False, help='Automatically marked if the employee punches in late by 10 minutes or more.')

    @api.model_create_multi
    def create(self, vals_list):
        from datetime import timedelta
        for vals in vals_list:
            if 'employee_id' in vals and 'check_in' in vals:
                employee = self.env['hr.employee'].browse(vals['employee_id'])
                calendar = employee.resource_calendar_id
                
                if calendar:
                    tz = pytz.timezone(employee.tz or self.env.user.tz or 'UTC')
                    check_in_dt = fields.Datetime.to_datetime(vals['check_in'])
                    check_in_time = check_in_dt.replace(tzinfo=pytz.utc).astimezone(tz)
                    check_in_hour = check_in_time.hour + check_in_time.minute / 60.0
                    
                    applied_calendar = calendar
                    if calendar.shift_type == 'dynamic':
                        # Logic for day/night determination
                        is_night = False
                        if check_in_hour >= calendar.night_shift_start_hour:
                            is_night = True
                        elif check_in_hour < (calendar.night_shift_start_hour - 12) % 24:
                            is_night = True
                        
                        new_calendar = calendar.dynamic_night_shift_id if is_night else calendar.dynamic_day_shift_id
                        
                        if new_calendar:
                            vals['applied_shift_id'] = new_calendar.id
                            applied_calendar = new_calendar
                    
                    # Static 10 minute late check
                    check_in_tz = check_in_time
                    
                    day_of_week = str(check_in_tz.weekday())
                    day_attendances = applied_calendar.attendance_ids.filtered(lambda a: a.dayofweek == day_of_week)
                    if day_attendances:
                        # Find the expected start time closest to the actual check-in hour in LOCAL time
                        check_in_hour = check_in_tz.hour + check_in_tz.minute / 60.0 + check_in_tz.second / 3600.0
                        expected_hour_from = min(day_attendances.mapped('hour_from'), key=lambda x: abs(x - check_in_hour))
                        
                        expected_start_tz = check_in_tz.replace(
                            hour=int(expected_hour_from), 
                            minute=int(round((expected_hour_from % 1) * 60)), 
                            second=0,
                            microsecond=0
                        )
                        # Mark half-day if 10 minutes late OR MORE (using >=)
                        max_allowed_tz = expected_start_tz + timedelta(minutes=10)
                        
                        if check_in_tz >= max_allowed_tz:
                            vals['is_half_day'] = True
                        
        return super(HrAttendance, self).create(vals_list)

    @api.depends('check_in', 'check_out', 'applied_shift_id')
    def _compute_worked_hours(self):
        super(HrAttendance, self)._compute_worked_hours()
        
        for attendance in self:
            if attendance.check_in and attendance.check_out:
                calendar = attendance.applied_shift_id or attendance.employee_calendar_id or attendance.employee_id.resource_calendar_id
                if calendar:
                    resource = attendance.employee_id.resource_id
                    tz = pytz.timezone(calendar.tz or 'UTC')
                    check_in_tz = attendance.check_in.astimezone(tz)
                    check_out_tz = attendance.check_out.astimezone(tz)
                    
                    # 1. Total actual duration
                    delta = (attendance.check_out - attendance.check_in).total_seconds() / 3600.0
                    
                    # 2. Try Odoo's standard lunch intervals (works for day shifts with explicit gaps)
                    lunch_intervals_dict = calendar._attendance_intervals_batch(
                        check_in_tz, check_out_tz, resources=None, lunch=True
                    )
                    lunch_duration = 0
                    if False in lunch_intervals_dict:
                        lunch_duration = sum((i[1] - i[0]).total_seconds() for i in lunch_intervals_dict[False]) / 3600.0
                    
                    if lunch_duration > 0:
                        delta -= lunch_duration
                    else:
                        # 3. Foolproof fallback for continuous shifts (like Night Shifts) without explicit gaps
                        # Extract shift duration directly from calendar configuration
                        day_of_week = str(check_in_tz.weekday())
                        day_attendances = calendar.attendance_ids.filtered(lambda a: a.dayofweek == day_of_week)
                        
                        if day_attendances:
                            expected_start = min(day_attendances.mapped('hour_from'))
                            
                            if expected_start >= 12:
                                # Night shift spanning to the next day
                                next_day = str((check_in_tz.weekday() + 1) % 7)
                                next_day_attendances = calendar.attendance_ids.filtered(lambda a: a.dayofweek == next_day)
                                
                                day_hrs = sum(a.hour_to - a.hour_from for a in day_attendances if a.hour_from >= expected_start)
                                next_hrs = sum(a.hour_to - a.hour_from for a in next_day_attendances if a.hour_to <= 12)
                                full_shift_duration = day_hrs + next_hrs
                            else:
                                # Day shift
                                full_shift_duration = sum(a.hour_to - a.hour_from for a in day_attendances)
                                
                            if full_shift_duration > 0:
                                implicit_break = max(0, full_shift_duration - calendar.hours_per_day)
                                
                                if implicit_break > 0 and delta > (full_shift_duration / 2):
                                    delta -= implicit_break
                            
                    attendance.worked_hours = max(0.0, delta)
