odoo.define('owl_society_managment.account', function (require) {
    "use strict";

    // require('web.dom_ready');
    // if (!$('.account').length) {
    //     return Promise.reject("DOM doesn't contain '.account'");
    // }
    const rpc = require('web.rpc');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlAccount extends Component {
    //     constructor() {
    //     super(...arguments);
    //     this.state = useState({
    //         name: "",
    //         email:"",
    //         member_type:"",
    //         street2:"",
    //     });
    // }

        async willStart() {
            debugger
            this.sheet = await this.getSheet();
        }

        async getSheet () {
            const accounts = await rpc.query({ route: "/get_account_line_data"})
            return accounts;
        }
        get accounts ()  {
            debugger
            return this.sheet;
        }
        
        // async _onClickLink(ev) {
        //     debugger        
        //     this.member = await rpc.query({ route: "/member/form", 
        //         params:{name: this.state.name,
        //             email: this.state.email,
        //             member_type: this.state.member_type,
        //             street2: this.state.street2,
        //         }});
        //     this.render(true);
          
        // }

        static template = xml`<div>
            <div class="container py-5">
                <div class="card border-0 mx-auto bg-100 rounded-0 shadow-sm bg-white o_database_list w-100 p-3">       
                   <div class="card-body">
                        <table class="table">
                            <thead class="bg-primary">
                                <tr>
                                  <th scope="col">Name</th>
                                  <th scope="col">Credit</th>
                                  <th scope="col">Debit</th>
                                  <th scope="col">balance</th>
                                </tr>
                            </thead> 
                            <t t-set="summ" t-value="0.0"/> 
                            <t t-set="cred" t-value="0.0"/> 
                            <t t-set="remaing" t-value="0.0"/> 
                            <t t-foreach="accounts" t-as="account" t-key='id'>
                                <tr>
                                    <td><t t-esc="account.name"/></td>
                                    <td class="card-body text-success"><t t-esc="account.credit"/></td>
                                    <td class="card-body text-danger"><t t-esc="account.debit"/></td>
                                    <td><t t-esc="account.balance"/></td>
                                    <t t-set="summ" t-value="summ + account.debit" />
                                    <t t-set="cred" t-value="cred + account.credit" />
                                    <t t-set="remaing" t-value="cred - summ" />
                                </tr>
                            </t>
                            <tr>
                                <td class="text-right" colspan="3"><h5>Total Credit : </h5></td>
                                <td><h5><span t-esc="cred"/></h5></td>
                            </tr>
                            <tr>
                                <td class="text-right" colspan="3"><h5>Total Debit : </h5></td>
                                <td><h5><span t-esc="summ"/></h5></td>
                            </tr>
                            <tr>
                                <td class="text-right" colspan="3"><h5>Total: </h5></td>
                                <td><h5><span t-esc="remaing"/></h5></td>
                            </tr>
                        </table>
                   </div>
                </div>
            </div>
        </div>
        `;
    }

    // function setup() {
    //     const OwlAccountInstance = new OwlAccount();
    //     OwlAccountInstance.mount($('.account')[0]);
    // }

    // whenReady(setup);

    return OwlAccount;
});