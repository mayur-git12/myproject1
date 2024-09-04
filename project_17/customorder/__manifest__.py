{
    'name': 'myorder',
    'version': '1.0',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        # 'views/check_product.xml',
        # 'views/charges.xml',
        'views/sale_line.xml',
        # 'wizard/wizard_view.xml'
    ],
    'installable': True,
    'application': True,
}