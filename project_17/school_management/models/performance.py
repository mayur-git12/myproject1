from odoo import models, fields, api

class SchoolPerformance(models.Model):
    _name = 'school.performance'
    _description = 'Student Performance Analytics'

    student_id = fields.Many2one('school.student', string='Student')
    subject_id = fields.Many2one('school.subject', string='Subject')
    exam_id = fields.Many2one('school.exam', string='Exam')
    marks_obtained = fields.Float(string='Marks Obtained')
    total_marks = fields.Float(string='Total Marks')
    percentage = fields.Float(string='Percentage', compute='_compute_percentage', store=True)

    @api.depends('marks_obtained', 'total_marks')
    def _compute_percentage(self):
        for record in self:
            if record.total_marks > 0:
                record.percentage = (record.marks_obtained / record.total_marks) * 100
            else:
                record.percentage = 0
