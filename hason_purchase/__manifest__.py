{
    'name': 'Hason Purchase',
    'version': '17.0.1.0.0',
    'summary': 'Add Transport Name field in Purchase',
    'category': 'Purchase',
    'author': 'Applified',
    'depends': ['base','web','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_template_views.xml',
        'reports/purchase_report.xml',
        ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}