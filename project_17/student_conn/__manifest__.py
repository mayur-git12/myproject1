{
    'name': 'Student Connection',
    'version': '1.0',
    'depends': ['base','account','students'],

    'data': [
    'views/student_cron.xml',
    'views/fees.xml',
    # 'data/student_data.xml',
    'security/ir.model.access.csv',
    'views/activity.xml',
    # 'views/job_form.xml',
    'views/button.xml',
    'views/join_menu.xml',
    'views/student_views.xml',
],

    'installable': True,
    'application': True,
}
