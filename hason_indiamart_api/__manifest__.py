{
    'name': 'Hason Indiamart API',
    'version': '17.0.1.0',
    'category': 'HR',
    'author': 'Applified contacts',
    'website': 'https://www.impel.com',
    'depends': ['base', 'mail','contacts','crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/indiamart_settings_view.xml',
        'views/tradeindia_settings_view.xml',
    ],
    
    'assets': {},
    'installable': True,
    'auto_install': False,
    'license':'LGPL-3',
}