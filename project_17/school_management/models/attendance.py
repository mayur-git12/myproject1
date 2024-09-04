from odoo import models, fields, api

class Attendance(models.Model):
    _name = 'school.attendance'
    _description = 'Attendance Record'

    student_id = fields.Many2one('school.student', string='Student')
    date = fields.Date(string='Date', default=fields.Date.today)
    status = fields.Selection([('present', 'Present'), ('absent', 'Absent')], string='Status')

    def send_absence_notification(self):
        for record in self:
            if record.status == 'absent':
                template = self.env.ref('school_management.absence_notification_template')
                self.env['mail.template'].browse(template.id).send_mail(record.id, force_send=True)

    @api.model
    def create(self, vals):
        res = super(Attendance, self).create(vals)
        res.send_absence_notification()
        return res