{
    'name': 'Restaurant Food Costing & Full Accounting Pro',
    'version': '2.0',
    'category': 'Point of Sale',
    'summary': 'نظام تكاليف وتفريغ مخزني ومحاسبة مطاعم متكامل بالكامل',
    'depends': ['base', 'point_of_sale', 'account', 'stock', 'uom'],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/accounting_views.xml',
        'reports/recipe_report_template.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
