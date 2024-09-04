
{
    # Module information
    'name': 'MySchool Management',
    'version': '17.0.1.0.1',
    'category': 'Education',
    'license': 'LGPL-3',
    'summary': """
        A module to manage school operations including students, teachers, classes, attendance, exams, and more.
    """,

    # Author
    'author': 'Chetan Dewasi',
    'website': 'http://www.dewasi.com',

    # Dependancies
    'depends': ['base', 'mail'],

    # Views
    "data": [
        # 'security/security.xml',
        
        'security/ir.model.access.csv',
        
        'report/student_report_card.xml',

        'views/academic_year_view.xml',
        'views/student_view.xml',
        'views/teacher_view.xml',
        'views/class_view.xml',
        'views/subject_view.xml',
        'views/attendance_view.xml',
        'views/exam_view.xml',
        'views/fee_view.xml',
        'views/performance.xml',
        'views/extracurricular_activities_view.xml',
        'views/school_management_menu.xml',
    ],

    # Technical
    'installable': True,
    'auto_install': False,
}

