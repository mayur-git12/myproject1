from odoo import models, fields

class Teacher(models.Model):
    _name = 'school.teacher'
    _description = 'Teacher Information'

    name = fields.Char(string='Name', required=False)
    employee_id = fields.Char(string='Employee ID', required=False)
    subject_ids = fields.Many2many('school.subject', string='Subjects')
    contact_number = fields.Char(string='Contact Number')
    email = fields.Char(string='Email')
    hire_date = fields.Date(string='Hire Date', default=fields.Date.today)
    active = fields.Boolean(string='Active', default=True)

    class_ids = fields.One2many('school.class', 'teacher_id', string='Classes')
