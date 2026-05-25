{
    'author': 'George Sadek',
    'name': 'Hospital Management System',
    'version': '1.0',
    'category': 'Healthcare',
    'summary': 'Manage patients in a hospital',
    'depends': ['base', 'contacts'],
    'data': [
        'security/hms_security.xml',
        'views/hms_patient_views.xml',
        'views/hms_department_views.xml',
        'views/hms_doctor_views.xml',
        'views/hms_res_partner_views.xml',
        'views/hms_patient_report_views.xml',
        'reports/hms_patient_report.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
