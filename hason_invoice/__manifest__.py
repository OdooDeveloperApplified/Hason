{
    'name': 'Hason_invoice',
    'version': '17.0.1.0.0',
    'summary': 'Add Transport Name field in Sale Order',
    'category': 'Sales',
    'author': 'Applified',
    'depends': ['sale', 'l10n_in', 'stock','sale_stock', 'account','web'],
    'data': [
        'views/invoice_report_inherit.xml',
        'views/account_move_form_inherit.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}