from odoo import fields, models, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class Student(models.Model):
    _inherit = 'wb.student'

    newfield1 = fields.Char("Blood group")
    newfield2 = fields.Char("Religion")
    fatherjobtype = fields.Selection([
        ('job', 'Job'),
        ('business', 'Business')
        ], string="Father Occupation")
    job_id = fields.Many2one('wb.job', string="Job Profile")
    dob = fields.Date("Date of Birth")
    activity_ids = fields.One2many('wb.activity','student_id',string="Activity")
    fees_id = fields.Many2one('product.product', string="fees", required=True)
    


    @api.model
    def create(self, vals):
        vals['dob'] = vals.get('dob') or fields.date.today() 
        return super().create(vals)
    
    def write(self, vals):
        
        if 'dob' in vals and not vals['dob']:
            vals['dob'] = fields.Date.today()
        return super(Student, self).write(vals)
    
   
    @api.model
    def create(self, vals):
        if not vals.get('dob'):
            vals['dob'] = fields.Date.today()  
        return super().create(vals)
    
    # @api.constrains('join_datetime')
    # def _check_join_datetime(self):
    #     for record in self:
    #         join_days = int(self.env['ir.config_parameter'].sudo().get_param('students.join_days', default=0))
            
    #         min_valid_date = datetime.now() + timedelta(days=join_days)
        
    #         if record.join_datetime and record.join_datetime < min_valid_date:
    #             raise ValidationError(f"Joining Datetime INVALID")



    school_info_count = fields.Integer(string='School Info Count', compute='_compute_school_info_count')

    @api.depends('activity_ids')
    def _compute_school_info_count(self):
        for record in self:
           
            record.school_info_count = len(record.activity_ids)

    def action_view_account(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Student Activity',
            'view_mode': 'tree,form',
            'res_model': 'wb.activity',
            'domain': [('id', 'in', self.activity_ids.ids)],
           
        }
    def action_view_job(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Job Details',
            'view_mode': 'form',
            'res_model': 'wb.job',
            'res_id':self.job_id.id,
           
        }
    
    
    def unlink(self):
        for record in self:
            if record.roll_number>1:
                raise ValidationError('You Cannot Delete the Record')
            return  super().unlink()
        
    def default_get(self,fields_list):
        dflt=super(Student,self).default_get(fields_list)
        dflt['roll_number']="01"
        dflt['newfield2']="Hindu"
        return dflt
    
  
    partner_id = fields.Many2one('res.partner', string="Partner")

    def genrate_partner(self, student):
        if not student.partner_id:
            partner = self.env['res.partner'].create({
                'name': student.name,
            })
            student.partner_id = partner.id
        return student.partner_id
    
    def genrate_invoice(self, student):
        today = fields.Date.today()
        existing_invoice = self.env['account.move'].search([
            ('partner_id', '=', student.partner_id.id),
            ('invoice_date', '=', today),
            ('move_type', '=', 'out_invoice'),
        ], limit=1)
        
        if existing_invoice:
            return
        partner = self.genrate_partner(student)
        
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'invoice_date': today,
        }
        invoice = self.env['account.move'].create(invoice_vals)
        
        if invoice:
            invoice_line_vals = {
                'product_id': student.fees_id.id,
                'name': student.fees_id.name,
                'move_id': invoice.id,
            }
            self.env['account.move.line'].create(invoice_line_vals)
    
    @api.model
    def _cron_student_fees(self):
        today = fields.Date.today()
        students = self.search([])
        for student in students:
            if student.join_datetime:
                join_date = student.join_datetime.date()
                if today.day == join_date.day:
                    self.genrate_invoice(student)





class Job(models.Model):
    _name = 'wb.job'
    _description = "This is a job profile"
    _rec_name = "address"


    company = fields.Char("Workplace Name")
    address = fields.Char("Address")
    mobile = fields.Char("Contact No") 

    @api.depends('company', 'address', 'mobile')
    def _compute_display_name(self):
        for record in self:
            name = record.address
            record.display_name = name



class activity(models.Model):
    _name = 'wb.activity'
    _decription = "this is a activity"
    
    gamename = fields.Char("Activity Name")
    gametype = fields.Char("Type")
    student_id = fields.Many2one('wb.student',string="Student Name")

    


    

class Joining(models.TransientModel):
    _inherit = 'res.config.settings'

    join_days = fields.Integer(string="Join in Days", default=0, config_parameter='students.join_days')


class School(models.Model):
    _inherit = 'wb.school'



class ProductTemplate(models.Model):
    _inherit = 'product.template'

    fees = fields.Boolean("Student Fees")
