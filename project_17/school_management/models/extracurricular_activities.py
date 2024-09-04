from odoo import models, fields

class SchoolActivity(models.Model):
    _name = 'school.activity'
    _description = 'Extracurricular Activity'

    student_id = fields.Many2one('school.student', string='Student', required=False)
    activity_name = fields.Char(string='Activity Name', required=False)
    date = fields.Date(string='Date', required=False)
    description = fields.Text(string='Description')
