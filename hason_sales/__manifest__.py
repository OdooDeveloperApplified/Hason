{
    'name': 'Hason Sales',
    'version': '17.0.1.0.0',
    'summary': 'Add Transport Name field in Sale Order',
    'category': 'Sales',
    'author': 'Applified',
    'depends': ['sale', 'l10n_in', 'stock','sale_stock', 'account',],
    'data': [
        'views/sale_order_view.xml',
        'reports/report_saleorder_inherit.xml',
            ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}