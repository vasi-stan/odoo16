{
    'name': "Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Vasi",
    'category': 'Real Estate',
    'description': """
    Description text
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_view.xml',
        'views/res_users.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
}