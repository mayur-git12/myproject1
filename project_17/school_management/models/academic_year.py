from odoo import models, fields, api, _

class AcademicYear(models.Model):
    _name = 'academic.year'
    _description = 'Academic Year'

    name = fields.Char(string='Year', required=True, copy=False, default="New")
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    active = fields.Boolean(string='Active', default=True)
    current = fields.Boolean(string='Current Year', copy=False, default=False, help="Check this box to set the current academic year.")
    
    classes_ids = fields.One2many('school.class', 'academic_year_id', string='classes')

    _sql_constraints = [
        ('unique_year', 'unique(name)', 'Academic Year must be unique.')
    ]

    
    @api.constrains('current')
    def _check_current(self):
        for record in self:
            if record.current:
                # Find all other records and set `current` to False
                other_years = self.search([('id', '!=', record.id)])
                other_years.write({'current': False})