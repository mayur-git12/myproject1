from odoo import models, fields

class Subject(models.Model):
    _name = 'school.subject'
    _description = 'Subject Information'

    name = fields.Char(string='Subject Name')
    code = fields.Char(string='Subject Code')
    teacher_ids = fields.Many2many('school.teacher', string='Teachers')


    student_ids=fields.One2many('school.student','school_id',string='subject')

    classes_ids = fields.One2many('school.class', 'academic_year_id', string='classes')

