from odoo import models, fields

class Exam(models.Model):
    _name = 'school.exam'
    _description = 'Exam Information'

    name = fields.Char(string='Exam Name', required=False)
    exam_date = fields.Date(string='Exam Date', required=False)
    class_id = fields.Many2one('school.class', string='Class', required=False)
    subject_ids = fields.Many2many('school.subject', string='Subjects')

class ExamResult(models.Model):
    _name = 'school.exam.result'
    _description = 'Exam Result'

    student_id = fields.Many2one('school.student', string='Student', required=False)
    exam_id = fields.Many2one('school.exam', string='Exam', required=False)
    subject_id = fields.Many2one('school.subject', string='Subject', required=False)
    marks = fields.Float(string='Marks Obtained')
