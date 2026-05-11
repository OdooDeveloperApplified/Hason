{
    'name': 'Hason CRM',
    'version': '17.0.1.0',
    'category': 'CRM',
    'author': 'Applified CRM',
    'website': 'https://www.impel.com',
    'depends': ['base', 'mail','crm','web'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
        'views/industry_master_view.xml',
    ],
    'assets': {},
    'installable': True,
    'auto_install': False,
    'license':'LGPL-3',
}