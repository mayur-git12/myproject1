from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import base64
from datetime import datetime, timedelta
import json

class Student(models.Model):
    _name = 'wb.student'
    _description = "This is student profile"

    name = fields.Char("Name", required=True)
    email = fields.Text("Email")

    school_id_domain = fields.Char(string='School id Domain', compute='_compute_school_id_domain', store=False)
    school_id = fields.Many2one('wb.school', string='School')

    student_photo = fields.Binary("Image")
    roll_number = fields.Integer("Roll Number")
    School_type = fields.Selection([
        ('primary', 'Primary'),
        ('secondary', 'Secondary')
    ], string="Select Type", required=True)
    habit = fields.Selection([
         ('music','Music'),
         ('cricket','Cricket'),
    ],string="Habbit")
    height = fields.Float("Height")
    # @api.constrains('height')
    # def _check_height(self):
    #     for record in self:
    #         if record.height <= 3:
    #             raise ValidationError("Height must be greater than 3")
    is_enrolled = fields.Boolean("Enrolled", default=True)
    enroll_date = fields.Date("Enrollment Date")
    join_datetime = fields.Datetime("Joining Datetime")


    
    state = fields.Selection([
        ('draft', 'draft'),
        ('mail_sent', 'Mail sent')
    ], string="Status", default="draft")
    status = fields.Selection([
        ('junior', 'Junior'),
        ('senior', 'Senior')
    ], string="Status")
    course_ids = fields.Many2many('wb.course', string="Courses")
    student_status = fields.Char(string="Student Status", compute='_compute_student_status' , default=False)
    @api.depends('roll_number')
    def _compute_student_status(self):
            for record in self:
                    if record.roll_number <= 100:
                        record.student_status = 'Regular Student'
                    else:
                        record.student_status = 'New Student'

    @api.depends('School_type')
    def _compute_school_id_domain(self):
        for rec in self:
            if rec.School_type:
                school_ids = self.env['wb.school'].search([('School_type', '=', rec.School_type)], limit=1)
                # print("<<<<<<<<<<<<<<<<",school_ids)
                rec.school_id_domain = "[('id', 'in', %s)]" % json.dumps(school_ids.ids)
                # print("<<<<<<<<<<<<<<<<<<<<",rec.school_id_domain)
            else:
                rec.school_id_domain = "[('id', 'in', %s)]" % json.dumps([])
    
    # @api.onchange('School_type')
    # def _onchange_school_type(self):
    #      for rec in self:
    #           if rec.School_type:
    #                rec.School_type_domain = [('school_id', '=', rec.school_id.id)]

    # @api.onchange('School_type')
    # def _onchange_school_type(self):
    #     school_type = self.School_type
    #     if school_type:
    #         domain = [('school_type', '=', school_type)]
    #         schools = self.env['wb.school'].search(domain)
    #         if schools:
    #             self.school_id = schools[0].id
    #             return {'domain': {'school_id': domain}}
    #     else:
    #         return {'domain': {'school_id': []}}
    # @api.onchange('School_type')
    # def _onchange_school_type(self):
    #     if self.School_type:
    #         for school in self.schooll_id:
    #              school.schools_ids = False
    #         matching_schools = self.env['wb.school'].search([('School_type', '=', self.School_type)])
    #         if self.id:
    #             for school in matching_schools:
    #                 school.schools_ids = self.id
    #         else:
    #             self.schooll_id = [(6,0,matching_schools.ids)]
    #     else:
    #         self.schooll_id = [(5, 0, 0)]
    
    
    # @api.onchange('School_type')
    # def _onchange_school_type(self):

    #     if self.School_type:
    #         self.schooll_id = self.env['wb.school'].search([('School_type', '=', self.School_type)])
    #     else:
    #         self.schooll_id = False
    # school_count = fields.Integer(string='School Count', compute='_compute_school_count')

    # school_info_count = fields.Integer(string='School Info Count', compute='_compute_school_info_count')

    # @api.depends('schooll_id')
    # def _compute_school_info_count(self):
    #     for record in self:
    #         record.school_info_count = len(record.schooll_id)





    #         sale_order_count = fields.Integer(string='Sale Order Count', compute='_compute_sale_order_count')

    # def _compute_sale_order_count(self):
    #     for order in self:
    #         order.sale_order_count = self.env['sale.order'].search_count([('partner_id', '=', order.partner_id.id)])

       
    def action_send_email(self):
        # import pdb;pdb.set
        pdf = self.env.ref('student_report_action')._render_qweb_pdf(self.id)[0]

        report_base64 = base64.b64encode(pdf)

        
                
        attachment = self.env['ir.attachment'].create({
            'name': 'Student Report - %s.pdf' % self.name,
            'type': 'binary',
            'datas': report_base64,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf'
        })

       
        template_id = self.env.ref('students.student_email_template').id
        email_template = self.env['mail.template'].browse(template_id)
        email_template.attachment_ids = [(6, 0, [attachment.id])]
        email_template.send_mail(self.id, force_send=True)
        
        self.state = 'mail_sent'

    @api.model
    def create(self, vals):
        student = super(Student, self).create(vals)
        self._create_res_partner(student)
        return student

    def _create_res_partner(self, student):
        partner_vals = {
            'name': student.name,
            'email': student.email,
            'image_1920': student.student_photo,
            'comment': _("Student Profile"),
            'type': 'contact',
        }
        self.env['res.partner'].create(partner_vals)
