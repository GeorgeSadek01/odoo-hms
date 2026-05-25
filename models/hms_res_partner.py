from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string='Related Patient')

    @api.constrains('email', 'related_patient_id')
    def _check_email_patient_link(self):
        for rec in self:
            if rec.related_patient_id and rec.email:
                existing_patient = self.env['hms.patient'].search([
                    ('email', '=', rec.email),
                ], limit=1)
                if existing_patient:
                    raise ValidationError(_(
                        'Cannot link this customer to a patient because the email '
                        'address already exists in the patient model.'
                    ))

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise UserError(_(
                    'You cannot delete a customer that is linked to a patient.'
                ))
        return super(ResPartner, self).unlink()
