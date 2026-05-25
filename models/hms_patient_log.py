from odoo import fields, models


class HmsPatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log'
    _rec_name = 'description'
    _order = 'date desc'

    patient_id = fields.Many2one('hms.patient', string='Patient', required=True, ondelete='cascade')
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user, readonly=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now, readonly=True)
    description = fields.Text(string='Description', required=True)
