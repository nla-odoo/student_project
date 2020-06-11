odoo.define('owl_society_managment.account_create', function (require) {
    "use strict";

    // require('web.dom_ready');
    // if (!$('.my_account_create_component').length) {
    //     return Promise.reject("DOM doesn't contain '.my_account_create_component'");
    // }
    const rpc = require('web.rpc');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlAccountCreate extends Component {
        constructor() {
        super(...arguments);
        this.state = useState({
            name: "",
            user_type_id:"",
            code:"",
        });
    }
        async willStart() {
            this.account = await this.getAccount();
        }

        async getAccount () {
            const accounts = await rpc.query({route: "/get_account_data"});
            return accounts;
        }
        get accounts ()  {
            debugger
            return this.account;
        }
        
        async _onClickLink(ev) {
            debugger        
            this.account = await rpc.query({ route: "/account/form", 
                params:{name: this.state.name,
                    user_type_id: this.state.user_type_id,
                    code: this.state.code,
                }});
            this.render(true);
          
        }


        static template = xml`<div>
        <div class="container py-5">
            <div class="card-body">
                <form method="post">
                    <div class="form-group">
                        <label>Name</label>
                        <input type="text" name='name' t-model="state.name" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>Type</label>
                        <select id="user_type_id" name="user_type_id" t-model="state.user_type_id" class="form-control">
                            <t t-foreach="accounts" t-as="acc">
                                <option t-key="acc" t-attf-value="{{acc.id}}"><t t-esc="acc.name"/></option>
                            </t>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Code</label>
                        <input type="text" name='code' t-model="state.code" class="form-control"/>
                    </div>
                <a class="btn btn-primary" t-on-click="_onClickLink">Submit</a>
                </form>
            </div>
        </div>
        </div>
        `;
    }

    // function setup() {
    //     const OwlAccountCreateInstance = new OwlAccountCreate();
    //     OwlAccountCreateInstance.mount($('.my_account_create_component')[0]);
    // }

    // whenReady(setup);

    return OwlAccountCreate;
});