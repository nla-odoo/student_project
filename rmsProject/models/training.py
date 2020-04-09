import uuid
from odoo import models, fields, api


class propertyregi(models.Model):
    _name = "training.propertyregi"
    _description = "training property registration"

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    name = fields.Char(string="Name", help="Name of your Hostel/Apartment/Flate")
    property_type = fields.Selection([('apartment', 'Apartment'), ('flate', 'Flate')], string="Property Type", required=True)
    pgfor = fields.Selection([('girls', 'Girls'), ('boys', 'Boys')], string="PG is available for", required=True)
    share = fields.Selection([('shared', 'Shared'), ('private', 'Private')], string="PG is", required=True)
    state = fields.Char(string="State", required=True)
    address = fields.Char(string="Current Address", required=True)
    city = fields.Char(string="City", required=True)
    rent = fields.Integer(string="Rent Per Bed")
    maintance = fields.Integer(string="Maintenance Charges")
    maintance_type = fields.Selection([('monthly', 'Monthly'), ('annually', 'Annually'), ('one_time', 'One Time')], string="Maintenance Type")
    deposite = fields.Integer(string="Deposite")
    feature_type_ids = fields.Many2many('training.features', string="Which included in rent", domain=[('ftype', '=', 'common')])
    hide = fields.Boolean(string="hide", default=False)
    weekday_ids = fields.Many2many('training.food', string="WeekDay")
    food_type = fields.Selection([('veg', 'Veg'), ('nonVeg', 'Veg and NonVeg')], string="Food Type")
    bedrooms = fields.Integer(string="Total Room")
    furnish_type = fields.Selection([('unfurnished', 'UnFurnished'), ('semifurnished', 'SemiFurnished'), ('fullyfurnished', 'FullyFurnished')], string="Room Furnishing")
    property_floor = fields.Selection([('ground', 'Ground'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], string="Property Floor")
    total_floor = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], string="Total Floor")
    avialble_from = fields.Date(string="Avialble From")
    rules = fields.Text(string="House Rules")
    late_entry = fields.Char(string="Last Entry Time")
    image = fields.Binary(string="Image", attachment=True)
    room_count = fields.Integer(compute="_compute_room")
    inquiry_count = fields.Integer(compute="_compute_inquiry")
    tenant_count = fields.Integer(compute="_compute_tenant")

    def _compute_tenant(self):
        self.tenant_count = self.env['training.tenants'].search_count([])

    def _compute_inquiry(self):
        self.inquiry_count = self.env['training.inquiry'].search_count([])

    def _compute_room(self):
        self.room_count = self.env['training.rooms'].search_count([])

    @api.onchange('feature_type_ids')
    def _onchange_feature_type_ids(self):
        for i in self.feature_type_ids:
            if i.name == 'Food':
                self.hide = True

    def room(self):
        return {
            'view_mode': 'form',
            'res_model': 'training.rooms',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'context': {'current_id': self.id}
        }


class inquiry(models.Model):
    _name = "training.inquiry"
    _description = "tenant training inquiry"

    def inquirystatus(self):
        self.status = 'conformed'

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="E-mail")
    phone = fields.Char(string="Contact Number", size=10, required=True)
    check_in = fields.Date(string="CheckIn Date")
    intrest_in = fields.Selection([('site_visit', 'site visit'), ('direct_rent', 'Direct Rent')], string="Intrest in")
    status = fields.Selection([('pending', 'Pending'), ('conformed', 'Conformed')], string="Status", default="pending")


class features(models.Model):
    _name = "training.features"
    _description = "training features"

    name = fields.Char(string="name", required=True)
    ftype = fields.Selection([('room', 'Room Facility'), ('common', 'Common Facility')], string="Facility Type")


class food(models.Model):
    _name = "training.food"
    _description = "training food"

    name = fields.Char(string="name", copy=False, required=True)


class tenant(models.Model):
    _name = "training.tenants"
    _description = "tenant registration"

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    name = fields.Char(string="tenant Name", required=True)
    dob = fields.Date(string="date of birth")
    phone = fields.Char(string="Contact Number", size=10, required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="gender", required=True)
    email = fields.Char(string="tenant_email")
    occupation = fields.Selection([('study', 'Study'), ('job', 'Job')], string="Occupation")
    home_address = fields.Text(string="Parmanet Address", required=True)
    father_name = fields.Text(string="Father's Name")
    father_phone = fields.Char(string="Father's Contact", size=10, required=True)
    rent_type = fields.Selection([('monthly', 'Monthly'), ('annually', 'Annually')], string="rent type")

    def allotroom(self):
        return {
            'view_mode': 'tree',
            'res_model': 'training.rooms',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'context': {'current_id': self.id, }
        }


class bill(models.Model):
    _name = "training.bill"
    _description = "tenant total bill"

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    bill_type = fields.Selection([('electricity', 'Electricity Bill'), ('food', 'Food Bill'), ('water', 'Water Bill'), ('internet', 'Internet Bill'), ('maintenance', 'Maintenance')], string="Select Bill Type", default="Electricity", required=True)
    bill_date = fields.Date(string="date of bill", required=True)
    payment = fields.Float(string="Total Amount", required=True)


class rooms(models.Model):
    _name = "training.rooms"
    _description = "add rooms of property"
    _rec_name = 'room_number'

    def addtenant(self):
        tid = self.env.context.get('current_id')
        if self.status != 'booked':
            self.status = 'remaining'
            a = self.room_capacity
            allot = self.env['training.allot'].search([('room_number_id', '=', self.id)])
            print("\n\n\n", allot)
            c = 1
            for j in allot:
                c = c + 1
            if a == c:
                self.status = 'booked'

        return {
                    'view_mode': 'form',
                    'res_model': 'training.allot',
                    'target': 'current',
                    'type': 'ir.actions.act_window',
                    'context': {'current_id': tid}
                }

    def vacant(self):
        roomnumber = self.room_number
        if self.status == 'booked':
            self.write({'status': 'vacant'})
            return {
                    'view_mode': 'tree',
                    'res_model': 'training.allot',
                    'target': 'current',
                    'type': 'ir.actions.act_window',
                    'domain': [('room_number_id', '=', [roomnumber])]
                }

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    room_number = fields.Char(string="Room Number")
    room_capacity = fields.Integer(string="Sharing persons")
    room_facility = fields.Many2many("training.features", string="Room Facility", domain=[('ftype', '=', 'room')])
    per_bed_rent = fields.Integer(string="Rent per bed")
    # image = fields.Many2many('training.imagestore', string="Image")
    status = fields.Selection([('booked', 'Booked'), ('vacant', 'Vacant'), ('remaining', 'Remaining')], string='Status', default="vacant")


class allot(models.Model):
    _name = "training.allot"
    _description = "room allotment"

    @api.onchange('company_id')
    def getData(self):
        tenant = self.env.context.get('current_id')
        self.tenant_id = tenant
        res = self.env['training.tenants'].search([]).filtered(lambda res: res.id == tenant)
        self.tenant_name = res.name

    def _default_order_id(self):
        return uuid.uuid4()

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    tenant_id = fields.Integer(string="Tenant Id")
    room_number_id = fields.Many2one('training.rooms', string="Room Number")
    tenant_name = fields.Char(string="Tenant Name")
    rent = fields.Integer(string="Rent per bed", related="room_number_id.per_bed_rent", store=True)
    capacity = fields.Integer(string="Sharing persons", related="room_number_id.room_capacity", store=True)
    payment_date = fields.Datetime(string=" Payment Date")
    status = fields.Selection([('success', 'success'), ('failure', 'Failure')], string="Status")
    order_ref = fields.Char(string="order_id", default=_default_order_id, store=True)
    acquirer_ref = fields.Char(string="acquirer_ref")
