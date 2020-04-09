# from datetime import datetime
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo import models, fields, api


class Registration(models.Model):
    _name = 'ahm.registration'
    _description = 'AHM Registration'

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    name = fields.Char()
    org_doc_name = fields.Many2one(comodel_name="ahm.organization.registration")
    image = fields.Binary()
    contact = fields.Char(string="Contact")
    email = fields.Char(string="Email")
    address = fields.Char(string="Address")
    specialization = fields.Char(string="Specialization")
    opening_time = fields.Many2one(comodel_name="ahm.time", string="Visiting From")
    closing_time = fields.Many2one(comodel_name="ahm.time", string="Visiting To")
    workingdays = fields.Many2many(comodel_name="ahm.working.days", string="Working Days")


class OrganizationRegistration(models.Model):
    _name = 'ahm.organization.registration'
    _description = "AHM Organization Registration"
    _rec_name = "org_name"

    doc_name = fields.One2many(comodel_name="ahm.registration", string="Doctor Name", inverse_name="org_doc_name")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    dept_name = fields.One2many(comodel_name="ahm.breed.type", inverse_name="org_name", string="Hospital Name")
    org_name = fields.Char(string="Organization Name")
    contact = fields.Integer(string="Mobile No.")
    helpline_number = fields.Integer(string="Helpline Number")
    email = fields.Char(string="Email")
    facility = fields.Text(string="Facility")
    address = fields.Text(string="Address")
    opening_time = fields.Many2one(comodel_name="ahm.time", string="Clinic Opening Time")
    closing_time = fields.Many2one(comodel_name="ahm.time", string="Clinic Closing Time")
    workingdays = fields.Many2many(comodel_name="ahm.working.days", string="Working Days")
    animal_name = fields.Many2many(comodel_name="ahm.animal.type", string="Animal Name")

    @api.model
    def create(self, vals):
        if not self.env['res.users'].search([('login', '=', vals.get('org_name'))]):
            groups_id_name = [(6, 0, [self.env.ref('AHM.group_manager').id]), (6, 0, [self.env.ref('base.group_user').id])]
            # currency_name = vals.get('currency')
            # currency = self.env['res.currency'].sudo().search([('name', '=', currency_name)], limit=1)
            # print("*****************************", currency.id)
            partner = self.env['res.partner'].sudo().create({'name': vals.get('org_name'),
                                                            'email': vals.get('email')})

            company = self.env['res.company'].sudo().create({
                'name': vals.get('org_name'),
                'partner_id': partner.id,
                'currency_id': 1})
            self.env['res.users'].sudo().create({
                'partner_id': partner.id,
                'login': vals.get('org_name'),
                'password': vals.get('org_name'),
                'company_id': company.id,
                'company_ids': [(4, company.id)],
                'groups_id': groups_id_name})
        return super(OrganizationRegistration, self).create(vals)


class WorkingDays(models.Model):
    _name = 'ahm.working.days'
    _description = "AHM Working Days"

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    name = fields.Char(string="Week Day")


class Time(models.Model):
    _name = 'ahm.time'
    _description = "AHM Time"

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    name = fields.Float(string="Time")


class AnimalType(models.Model):
    _name = 'ahm.animal.type'
    _description = "AHM Animal Type"

    name = fields.Char(string="Animal Type")
