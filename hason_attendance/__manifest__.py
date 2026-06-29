# -*- coding: utf-8 -*-
{
    'name': 'Hason Chemtech Attendance',
    'version': '17.0',
    'category': 'Human Resources/Attendance',
    'summary': 'Custom attendance and shift rules for Hason Chemtech',
    'description': """
        Adds custom fields to Employees and Working Schedules to manage
        location, manpower types, custom break rules, and punch-in policies.
    """,
    'depends': ['hr', 'hr_attendance', 'resource'],
    'data': [
        'views/hr_employee_views.xml',
        'views/resource_calendar_views.xml',
        'views/hr_attendance_views.xml',
        'data/resource_calendar_data.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
