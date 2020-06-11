odoo.define('owl_society_managment.society_create', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_society_create_component').length) {
        return Promise.reject("DOM doesn't contain '.my_society_create_component'");
    }
    const rpc = require('web.rpc');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlSocietyCreate extends Component {
        constructor() {
        super(...arguments);
        this.state = useState({
            name: "",
            email:"",
            currency:"",
            street:"",
            zip:"",
            city:"",
            code:"",
        });
    }
        async willStart() {
            this.member = await this.getMember();
        }

        async getMember () {
            const currencys = await rpc.query({route: "/society"});
            return currencys;
        }
        get currencys ()  {
            debugger
            return this.member;
        }
        
        async _onClickLink(ev) {
            debugger        
            this.member = await rpc.query({ route: "/society/form", 
                params:{name: this.state.name,
                    email: this.state.email,
                    currency: this.state.currency,
                    street: this.state.street,
                    zip: this.state.zip,
                    city: this.state.city,
                    code: this.state.code,
                }});
            window.location.href = "/web/login"
            // this.render(true);
          
        }


        static template = xml`<div>
            <div class="container py-5">
                <div class="card border-0 mx-auto bg-100 rounded-0 shadow-sm bg-white o_database_list w-50 p-3">
                    <h1 class="card-body text-warning" align='center'>Society Registration Form</h1>
                    <div class="card-body">
                    <form method="post">
                    <div class="form-group">
                        <label>Society Name</label>
                        <input type="text" name='name' t-model="state.name" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" name='name' t-model="state.email" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label for="Currency">Currency</label>
                        <select name="currency" t-model="state.currency" id="currency" class="form-control">
                            <t t-foreach="currencys" t-as="cur">
                                <option t-key="cur" t-attf-value="{{cur.id}}"><t t-esc="cur.name"/></option>
                            </t>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Short Code</label>
                        <input type="text" name='code' t-model="state.code" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>street</label>
                        <input type="text" name='street' t-model="state.street" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>zip</label>
                        <input type="text" name='zip' t-model="state.zip" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>city</label>
                        <input type="text" name='city' t-model="state.city" class="form-control"/>
                    </div>
                <a class="btn btn-primary" t-on-click="_onClickLink">Submit</a>
                </form>
            </div>
            </div>
        </div>
        </div>
        `;
    }

    function setup() {
        const OwlSocietyCreateInstance = new OwlSocietyCreate();
        OwlSocietyCreateInstance.mount($('.my_society_create_component')[0]);
    }

    whenReady(setup);

    return OwlSocietyCreate;
});