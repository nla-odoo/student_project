odoo.define('owl_society_managment.balance_create', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_balance_create_component').length) {
        return Promise.reject("DOM doesn't contain '.my_balance_create_component'");
    }
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
            this.member = await this.getPartner();
        }

        async getPartner () {
            const partners = await rpc.query({route: "/get_Parnter_data"});
            console.log(partners[2])
            return partners;
        }

        get partners ()  {
            debugger
            return this.member;
        }
        
        async _onClickLink(ev) {
            debugger        
            this.member = await rpc.query({ route: "/balance/form", 
                params:{payment_type: this.state.payment_type,
                    partner_type: this.state.partner_type,
                    amount: this.state.amount,
                    partner_id: this.state.partner_id,
                    destination_account_id: this.state.destination_account_id,
                    journal_id: this.state.journal_id,
                }});
            this.render(true);
          
        }


        static template = xml`<div>
        <div>
            <div>
                <form method="post">
                    <div>
                        <label>Payment Type</label>
                        <select id="payment_type" name="payment_type" t-model="state.payment_type">
                            <option value="outbound">Send Money</option>
                            <option value="inbound">Receive Money</option>
                        </select>
                    </div>
                    <div>
                        <label>Partner Type</label>
                        <select id="partner_type" name="partner_type" t-model="state.partner_type">
                            <option value="customer">customer</option>
                            <option value="supplier">Vendor</option>
                        </select>
                    </div>
                    <div>
                        <label>Amount</label>
                        <input type="number" name='amount' t-model="state.amount"/>
                    </div>
                    <div>
                        <label>Customer/Vendor</label>
                        <select name="partner_id" t-model="state.partner_id" id="partner_id">
                            <t t-foreach="partners[0]" t-as="part">
                                <option t-key="part" t-attf-value="{{part.id}}"><t t-esc="part.name"/></option>
                            </t>
                        </select>
                    </div>
                    <div>
                        <label>Destination Account</label>
                        <select name="destination_account_id" t-model="state.destination_account_id" id="destination_account_id">
                            <t t-foreach="partners[1]" t-as="account">
                                <option t-key="account" t-attf-value="{{account.id}}"><t t-esc="account.name"/></option>
                            </t>
                        </select>
                    </div>
                    <div>
                        <label>Jounral</label>
                        <select name="journal_id" t-model="state.journal_id" id="journal_id">
                            <t t-foreach="partners[2]" t-as="jounral">
                                <option t-key="jounral" t-attf-value="{{jounral.id}}"><t t-esc="jounral.name"/></option>
                            </t>
                        </select>
                    </div>
                <a t-on-click="_onClickLink">Submit</a>
                </form>
            </div>
        </div>
        </div>
        `;
    }

    function setup() {
        const OwlBalanceCreateInstance = new OwlBalanceCreate();
        OwlBalanceCreateInstance.mount($('.my_balance_create_component')[0]);
    }

    whenReady(setup);

    return OwlBalanceCreate;
});