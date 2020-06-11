odoo.define('owl_society_managment.balance_create', function (require) {
    "use strict";

    // require('web.dom_ready');
    // if (!$('.my_balance_create_component').length) {
    //     return Promise.reject("DOM doesn't contain '.my_balance_create_component'");
    // }
    const rpc = require('web.rpc');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlBalanceCreate extends Component {
        constructor() {
        super(...arguments);
        this.state = useState({
            payment_type: "",
            partner_type:"",
            amount:"",
            partner_id:"",
            destination_account_id:"",
            journal_id:"",
        });
    }
        async willStart() {
            debugger
            this.payment = await this.getPartner();
        }

        async getPartner () {

            const partners = await rpc.query({route: "/get_Parnter_data"});
            console.log(partners[2])
            return partners;
        }

        get partners ()  {
            debugger
            console.log(this.payment)
            return this.payment;
        }
        
        async _onClickLink(ev) {
            debugger        
            this.payment = await rpc.query({ route: "/balance/form", 
                params:{payment_type: this.state.payment_type,
                    partner_type: this.state.partner_type,
                    amount: this.state.amount,
                    partner_id: this.state.partner_id,
                    destination_account_id: this.state.destination_account_id,
                    journal_id: this.state.journal_id,
                }});
            console.log(this.payment)
            this.payNow(this.payment)
            this.render(true);
          
        }
        async payNow(payment) {
            debugger
            // let partner_id = ev.currentTarget.getAttribute('partner_id');
            let data_dict = await this._getPaymentDetails(this.payment)
            console.log(this.payment)
            let form = document.createElement('form');
            form.setAttribute('action', data_dict['redirection_url']);
            delete data_dict['redirection_url'];
            for(const key in data_dict){
                let new_element = document.createElement('input');
                new_element.setAttribute('name', key)
                new_element.setAttribute('value', data_dict[key])
                form.append(new_element)
            }
            document.getElementsByTagName('body')[0].append(form);
            form.submit()
        }

        _getPaymentDetails(payment) {
            debugger
            console.log(this.payment)
            return rpc.query({route: "/paytm/payment", params: {'payment': parseInt(payment)}});
        }



        static template = xml`<div>
        <div class="container py-5">
            <div class="card-body">
                <form method="post">
                    <t t-if="partners[3] == 'secretary' || partners[3] == 'treasurer'">
                        <div class="form-group">
                            <label>Payment Type</label>
                            <select id="payment_type" name="payment_type" t-model="state.payment_type" class="form-control">
                                <option value="outbound">Send Money</option>
                                <option value="inbound">Receive Money</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Partner Type</label>
                            <select id="partner_type" name="partner_type" t-model="state.partner_type" class="form-control">
                                <option value="customer">customer</option>
                                <option value="supplier">Vendor</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Customer/Vendor</label>
                            <select name="partner_id" t-model="state.partner_id" id="partner_id" class="form-control">
                                <t t-foreach="partners[0]" t-as="part">
                                    <option t-key="part" t-attf-value="{{part.id}}"><t t-esc="part.name"/></option>
                                </t>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Jounral</label>
                            <select name="journal_id" t-model="state.journal_id" id="journal_id" class="form-control">
                                <t t-foreach="partners[2]" t-as="jounral">
                                    <option t-key="jounral" t-attf-value="{{jounral.id}}"><t t-esc="jounral.name"/></option>
                                </t>
                            </select>
                        </div>
                    </t>
                    <div class="form-group">
                        <label>Amount</label>
                        <input type="text" name='amount' t-model="state.amount" id="amount" class="form-control"/>
                    </div>
                    
                    <div class="form-group">
                        <label>Destination Account</label>
                        <select name="destination_account_id" t-model="state.destination_account_id" id="destination_account_id" class="form-control">
                            <t t-foreach="partners[1]" t-as="account">
                                <option t-key="account" t-attf-value="{{account.id}}"><t t-esc="account.name"/></option>
                            </t>
                        </select>
                    </div>
                <a class="btn btn-primary" t-on-click="_onClickLink">Pay</a>
                </form>
            </div>
        </div>
        </div>
        `;
    }

    // function setup() {
    //     const OwlBalanceCreateInstance = new OwlBalanceCreate();
    //     OwlBalanceCreateInstance.mount($('.my_balance_create_component')[0]);
    // }

    // whenReady(setup);

    return OwlBalanceCreate;
});