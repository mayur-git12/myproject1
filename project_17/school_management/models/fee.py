from odoo import models, fields, api

class SchoolFee(models.Model):
    _name = 'school.fee'
    _description = 'Student Fee Management'

    student_id = fields.Many2one('school.student', string='Student', required=False)
    class_id = fields.Many2one('school.class', string='Class', required=False)
    amount = fields.Float(string='Amount', required=False)
    due_date = fields.Date(string='Due Date', required=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('invoiced', 'Invoiced'),
        ('paid', 'Paid')
    ], string='Status', default='draft')

    def create_invoice(self):
        invoice_vals = {
            'partner_id': self.student_id.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [(0, 0, {
                'name': 'School Fees for %s' % self.student_id.name,
                'quantity': 1,
                'price_unit': self.amount,
            })],
        }
        invoice = self.env['account.move'].create(invoice_vals)
        self.state = 'invoiced'
        return invoice
