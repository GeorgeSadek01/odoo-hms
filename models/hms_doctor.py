from odoo import api, fields, models


class HmsDoctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Doctor'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    name = fields.Char(string='Name', compute='_compute_name', store=True)
    image = fields.Image(string='Image', max_width=1920, max_height=1920)
    department_id = fields.Many2one('hms.department', string='Department')

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.first_name} {rec.last_name}"
