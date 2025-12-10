{
    'name': 'Hason Inventory',
    'version': '17.0.1.0.0',
    'summary': 'Add Transport Name field in Sale Order',
    'category': 'Inventory',
    'author': 'Applified',
    'depends': ['sale', 'l10n_in', 'stock','sale_stock', 'account',],
    'data': [
        
        'reports/report_delivery_slip.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}