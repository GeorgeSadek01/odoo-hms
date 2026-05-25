from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date
import re


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'
    _order = 'id DESC'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    name = fields.Char(string='Name', compute='_compute_name', store=True)
    email = fields.Char(string='Email')
    birthdate = fields.Date(string='Birthdate')
    history = fields.Html(string='History', sanitize=False)
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ], string='Blood Type')
    pcr = fields.Boolean(string='PCR')
    image = fields.Image(string='Image', max_width=1920, max_height=1920)
    address = fields.Text(string='Address')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)

    department_id = fields.Many2one('hms.department', string='Department')
    department_capacity = fields.Integer(string='Department Capacity', related='department_id.capacity', readonly=True)
    doctor_ids = fields.Many2many('hms.doctor', string='Doctors')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], string='State', default='undetermined')
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string='Log History')

    _unique_email = models.Constraint(
        'UNIQUE(email)',
        'A patient with this email address already exists.',
    )

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.first_name} {rec.last_name}"

    @api.depends('birthdate')
    def _compute_age(self):
        for rec in self:
            if rec.birthdate:
                today = date.today()
                rec.age = today.year - rec.birthdate.year - (
                    (today.month, today.day) < (rec.birthdate.month, rec.birthdate.day)
                )
            else:
                rec.age = 0

    @api.onchange('birthdate')
    def _onchange_birthdate(self):
        if self.birthdate:
            today = date.today()
            age = today.year - self.birthdate.year - (
                (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
            )
            if age < 30 and not self.pcr:
                self.pcr = True
                return {
                    'warning': {
                        'title': 'PCR Auto-checked',
                        'message': 'PCR field has been automatically checked because the patient is under 30 years old.',
                    }
                }

    def write(self, vals):
        if 'state' in vals:
            state_labels = dict(self._fields['state']._description_selection(self.env))
            for rec in self:
                if rec.state != vals['state']:
                    rec.env['hms.patient.log'].create({
                        'patient_id': rec.id,
                        'description': f'State changed to {state_labels.get(vals["state"], vals["state"])}',
                    })
        return super(HmsPatient, self).write(vals)

    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if rec.email:
                if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', rec.email):
                    raise ValidationError(_('Please enter a valid email address.'))
