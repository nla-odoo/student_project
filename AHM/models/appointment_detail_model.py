# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import uuid
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class AnimalRegistration(models.Model):
    _name = 'ahm.animal.registration'
    _description = "AHM Animal Registration"

    breed_name = fields.Char(string="Breed Name")
    breed_type = fields.Char(string="Breed Type")
    image = fields.Binary(string="Upload Image of the Breed")
    onwer_contact = fields.Char(string="Mobile No.")
    email = fields.Char(string="Email")
    address = fields.Text(string="Address")

    _sql_constraints = [('email_uniq', 'unique (email)', 'Email Should Be Unique!')]

    @api.constrains('onwer_contact')
    def _validate_contact(self):
        for record in self:
            if record.onwer_contact and len(record.onwer_contact) != 10:
                raise ValidationError('Enter Valid Number')


class Appointment(models.Model):
    _name = 'ahm.appointment'
    _description = 'AHM Appointment'

    breed_type_id = fields.Many2one(comodel_name="ahm.animal.type", string="Animal Type")
    hospital_ids = fields.Many2many(comodel_name="ahm.organization.registration", compute="_compute_hospital")
    org_id = fields.Many2one(comodel_name="ahm.organization.registration", domain="[('id', 'in', hospital_ids)]", string="Hospital Name")
    add_doc_ids = fields.Many2many(comodel_name="ahm.registration", compute="_compute_doctor")
    doc_id = fields.Many2one(comodel_name="ahm.registration", domain="[('id', 'in', add_doc_ids)]", string="Doctor Name")
    patient_id = fields.Many2one(comodel_name="ahm.patient.detail", string="Visitor's Name")
    name = fields.Char(string="Pet Name")
    contact = fields.Char(string="Mobile No.")
    visiting_date = fields.Date(string="Appointment Date")
    visiting_time = fields.Many2one(comodel_name="ahm.time", string='Appointment Time')
    visit_charges = fields.Char(string="Visiting Charges", default=450)
    address = fields.Char(string="Address")
    status = fields.Selection([
        ('pending', 'Pending'),
        ('confirm', 'Appointment Confirm'),
        ('done', 'Done')], default='confirm')
    order_id = fields.Char("Order Id", default=str(uuid.uuid4()))
    acquirer_ref = fields.Char("Acquirer Ref")
    payment_status = fields.Char()
    payment_date = fields.Date()

    def pending(self):
        self.write({"status": "pending"})

    def confirm(self):
        self.write({"status": "confirm"})

    def done(self):
        self.write({"status": "done"})

    @api.onchange("visiting_date")
    def visitingtime(self):
        appointment_env = self.env['ahm.appointment'].search([('visiting_date', '=', self.visiting_date)])
        return {'domain': {'visiting_time': [('id', 'not in', appointment_env.visiting_time.ids)]}}

    @api.depends("breed_type_id")
    def _compute_hospital(self):
        hospital_ids_env = self.env['ahm.organization.registration'].search([])
        org_list = []
        for breed in hospital_ids_env:
            if self.breed_type_id.id in list(breed.animal_name.ids):
                org_list.append(breed.id)
        self.hospital_ids = self.env['ahm.organization.registration'].search([('id', 'in', org_list)])

    @api.depends("org_id")
    def _compute_doctor(self):
        hospital_ids_env = self.env['ahm.organization.registration'].search([])
        self.add_doc_ids = hospital_ids_env.filtered(lambda org: org.id == self.org_id.id).mapped('doc_id')

    @api.constrains('contact')
    def _validate_contact(self):
        for record in self:
            if record.contact and len(record.contact) != 10:
                raise ValidationError('Enter Valid Number')


class PatientDetail(models.Model):
    _name = 'ahm.patient.detail'
    _description = "AHM Patient Detail"

    name = fields.Char(string="Visitor's Name")
    contact = fields.Char(string="Mobile No.")
    email = fields.Char(string="Email")
    medicine = fields.Text(String="Medicine")
    prescription = fields.Char(string="Prescription")
    image = fields.Binary(attachment=True)

    @api.model
    def create(self, vals):
        if not self.env['res.users'].search([('login', '=', vals.get('name'))]):
            groups_id_name = [(6, 0, [self.env.ref('base.group_portal').id])]

            partner = self.env['res.partner'].create({
                'name': vals.get('name'),
                'email': vals.get('email')})
            self.env['res.users'].create({
                'partner_id': partner.id,
                'login': vals.get('name'),
                'password': vals.get('name'),
                'groups_id': groups_id_name})
        return super(PatientDetail, self).create(vals)

    _sql_constraints = [('email_uniq', 'unique (email)', 'Email Should Be Unique!')]

    @api.constrains('contact')
    def _validate_contact(self):
        for record in self:
            if record.contact and len(record.contact) != 10:
                raise ValidationError('Enter Valid Number')


class BreedType(models.Model):
    _name = 'ahm.breed.type'
    _description = "AHM Breed Type"

    breed_type_id = fields.Many2one(comodel_name="ahm.animal.type", string="Animal Type")
    org_id = fields.Many2one(comodel_name="ahm.organization.registration", context="{'org_id': True}", string="Department Name", required=True)
    name = fields.Many2one(comodel_name="ahm.registration", required=True)
    visit_charges = fields.Integer("Visiting Charges", default=450)
    opening_time = fields.Many2one(comodel_name="ahm.time", string="Visiting Hour From")
    closing_time = fields.Many2one(comodel_name="ahm.time", string="Visiting Hour To")
    workingdays = fields.Many2many(comodel_name="ahm.working.days", string="Visiting Days")
