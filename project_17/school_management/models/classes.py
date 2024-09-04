from odoo import models, fields

class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'Class Information'

    name = fields.Char(string='Class Name', required=False)
    teacher_id = fields.Many2one('school.teacher', string='Class Teacher')
    academic_year_id = fields.Many2one('academic.year', string='Academic Year', required=False)
    next_class = fields.Many2one('school.class', string='Next Class', required=False)
    subject_ids = fields.Many2many('school.subject', string='Subjects')
    student_ids = fields.One2many('school.student', 'class_id', string='Students')
