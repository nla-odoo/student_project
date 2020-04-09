# from datetime import datetime
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo import models, fields, api


class AnimalRegistration(models.Model):
    _name = 'ahm.animal.registration'
    _description = "AHM Animal Registration"

    breed_name = fields.Char(string="Breed Name", required=True)
    breed_type = fields.Char(string="Breed Type", required=True)
    image = fields.Binary(string="Upload Image of the Breed")
    onwer_contact = fields.Integer(string="Mobile No.", required=True)
    email = fields.Char(string="Email", required=True)
    address = fields.Text(string="Address", required=True)


class Appointment(models.Model):
    _name = 'ahm.appointment'
    _inherit = ['mail.thread']
    _description = 'AHM Appointment'

    b_type = fields.Many2one(comodel_name="ahm.animal.type", string="Animal Type")
    hospital_name = fields.Many2many(comodel_name="ahm.organization.registration", compute="_compute_hospital")
    org_name = fields.Many2one(comodel_name="ahm.organization.registration", domain="[('id', 'in', hospital_name)]", string="Department Name")
    add_doc_name = fields.Many2many(comodel_name="ahm.registration", compute="_compute_doctor")
    doc_name = fields.Many2one(comodel_name="ahm.registration", domain="[('id', 'in', add_doc_name)]", string="Doctor Name")
    patient_id = fields.Many2one(comodel_name="ahm.patient.detail", string="Visitor's Name")
    name = fields.Char(string="Pet Name")
    contact = fields.Char(string="Mobile No.")
    visiting_date = fields.Date(string="Appointment Date")
    visiting_time = fields.Many2one(comodel_name="ahm.time", string='Appointment Time')
    visit_charges = fields.Integer(string="Visiting Charges", default=450)

    address = fields.Char(string="Address", required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('confirm', 'Appointment Confirm'),
        ('done', 'Done')], default='confirm')

    def pending(self):
        self.write({"status": "pending"})

    def confirm(self):
        self.write({"status": "confirm"})

    def done(self):
        self.write({"status": "done"})

    @api.onchange("visiting_date")
    def visitingtime(self):
        # time_env = self.env['ahm.time'].search([])
        appointment = self.env['ahm.appointment'].search([])
        # var = appointment.mapped('hospital_name')
        # print("-----------------", var)
        appointment = self.env['ahm.appointment'].search([])
        var1 = appointment.filtered('hospital_name')
        print("-----------------------------", var1)
        appointment_env = self.env['ahm.appointment'].search([('visiting_date', '=', self.visiting_date)])
        return {'domain': {'visiting_time': [('id', 'not in', appointment_env.visiting_time.ids)]}}

    @api.depends("b_type")
    def _compute_hospital(self):
        hospital_name_env = self.env['ahm.organization.registration'].search([])
        org_list = []
        for i in hospital_name_env:
            if self.b_type.id in list(i.animal_name.ids):
                org_list.append(i.id)
        self.hospital_name = self.env['ahm.organization.registration'].search([('id', 'in', org_list)])

    @api.depends("org_name")
    def _compute_doctor(self):
        # doc_name_env = self.env['ahm.registration'].search([])
        hospital_name_env = self.env['ahm.organization.registration'].search([])
        doc_list = []
        for i in hospital_name_env:
            if self.org_name.id == i.id:
                doc_list = i.doc_name.ids
        self.add_doc_name = self.env['ahm.registration'].search([('id', 'in', doc_list)])


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


class BreedType(models.Model):
    _name = 'ahm.breed.type'
    _description = "AHM Breed Type"

    b_type = fields.Many2one(comodel_name="ahm.animal.type", string="Animal Type")
    org_name = fields.Many2one(comodel_name="ahm.organization.registration", context="{'org_name': True}", string="Department Name", required=True)
    name = fields.Many2one(comodel_name="ahm.registration", required=True)
    visit_charges = fields.Integer("Visiting Charges", default=450)
    opening_time = fields.Many2one(comodel_name="ahm.time", string="Visiting Hour From")
    closing_time = fields.Many2one(comodel_name="ahm.time", string="Visiting Hour To")
    workingdays = fields.Many2many(comodel_name="ahm.working.days", string="Visiting Days")
