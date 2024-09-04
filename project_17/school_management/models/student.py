from odoo import models, fields, api, _
from datetime import datetime

class SchoolStudent(models.Model):
    _name = 'school.student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Student'

    # Basic Information
    name = fields.Char(string='Student Name', required=False, tracking=True)
    roll_number = fields.Char(string='Roll Number', readonly=True, copy=False, tracking=True)
    school_id=fields.Many2one('school.subject',string="subject")
    
    date_of_birth = fields.Date(string='Date of Birth', required=False)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', required=False)
    contact_number = fields.Char(string='Contact Number')
    email = fields.Char(string='Email')

    # Academic Information
    class_id = fields.Many2one('school.class', string='Class', required=False)
    admission_date = fields.Date(string='Admission Date', default=fields.Date.today)
    status = fields.Selection([('active', 'Active'), ('promoted', 'Promoted'), ('dropped', 'Dropped')],
                              string='Status', default='active', tracking=True)

    # Attendance and Progress
    attendance_percentage = fields.Float(string='Attendance Percentage', compute='_compute_attendance_percentage')
    progress = fields.Float(string='Progress (%)', compute='_compute_progress')

    # Health Information
    blood_group = fields.Selection([('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), 
                                    ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
                                   string='Blood Group')
    allergies = fields.Text(string='Allergies')
    emergency_contact_name = fields.Char(string='Emergency Contact Name')
    emergency_contact_number = fields.Char(string='Emergency Contact Number')

    # Extracurricular Activities
    activities = fields.One2many('school.activity', 'student_id', string='Extracurricular Activities')
    
    # Academic Year
    academic_year_id = fields.Many2one('academic.year', string='Academic Year', required=False)

    # Promotion History
    promotion_history_ids = fields.One2many('student.promotion.history', 'student_id', string='Promotion History')

    # Automatic Unique Roll Number Generation
    @api.model
    def create(self, vals):
        vals['roll_number'] = self.env['ir.sequence'].next_by_code('school.student') or _('New')
        return super(SchoolStudent, self).create(vals)

    # Automatic Age Calculation
    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                record.age = (datetime.today().date() - record.date_of_birth).days // 365
            else:
                record.age = 0

    # Attendance Percentage Calculation
    def _compute_attendance_percentage(self):
        for record in self:
            total_classes = self.env['school.attendance'].search_count([('student_id', '=', record.id)])
            attended_classes = self.env['school.attendance'].search_count([('student_id', '=', record.id), ('status', '=', 'present')])
            if total_classes > 0:
                record.attendance_percentage = (attended_classes / total_classes) * 100
            else:
                record.attendance_percentage = 0

    # Progress Calculation
    def _compute_progress(self):
        for record in self:
            exams = self.env['school.performance'].search([('student_id', '=', record.id)])
            total_percentage = sum(exam.percentage for exam in exams)
            record.progress = total_percentage / len(exams) if exams else 0

    # Drop Student
    def action_drop(self):
        for record in self:
            record.status = 'dropped'

    # Generate Student Report Card
    def action_generate_report_card(self):
        self.ensure_one()
        report_card_lines = []
        exams = self.env['school.performance'].search([('student_id', '=', self.id)])
        for exam in exams:
            report_card_lines.append({
                'subject': exam.subject_id.name,
                'marks_obtained': exam.marks_obtained,
                'total_marks': exam.total_marks,
                'percentage': exam.percentage,
            })
        return self.env.ref('school_management.student_report_card_action').report_action(self, data={
            'report_card_lines': report_card_lines,
            'name': self.name,
            'class_id': self.class_id.name,
            'roll_number': self.roll_number,
            'date_of_birth': self.date_of_birth,
            'status': self.status,
            'teacher': self.class_id.teacher_id.name,
        })

    def promote_student(self):
        """Promote the student to the next class."""
        for student in self:
            current_class = student.class_id
            next_class = self.env['school.class'].search([('id', '>', current_class.id)], limit=1)
            if next_class:
                student.write({'class_id': next_class.id})
                self.env['student.promotion.history'].create({
                    'student_id': student.id,
                    'from_class_id': current_class.id,
                    'to_class_id': next_class.id,
                    'date': fields.Date.today()
                })

    def demote_student(self):
        """Demote the student to the previous class."""
        for student in self:
            current_class = student.class_id
            previous_class = self.env['school.class'].search([('id', '<', current_class.id)], limit=1)
            if previous_class:
                student.write({'class_id': previous_class.id})
                self.env['student.promotion.history'].create({
                    'student_id': student.id,
                    'from_class_id': current_class.id,
                    'to_class_id': previous_class.id,
                    'date': fields.Date.today()
                })




class StudentPromotionHistory(models.Model):
    _name = 'student.promotion.history'
    _description = 'Student Promotion History'

    student_id = fields.Many2one('school.student', string='Student', required=False)
    from_class_id = fields.Many2one('school.class', string='From Class')
    to_class_id = fields.Many2one('school.class', string='To Class')
    date = fields.Date(string='Date', required=False)



    