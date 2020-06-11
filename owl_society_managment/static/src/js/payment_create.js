odoo.define('owl_society_managment.payment_create', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_society_payment_component').length) {
        return Promise.reject("DOM doesn't contain '.my_society_payment_component'");
    }
    const rpc = require('web.rpc');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlPaymentCreate extends Component {
        constructor() {
        super(...arguments);
        this.state = useState({
            name: "",
            email:"",
            currency:"",
        });
    }
        async willStart() {
            this.member = await this.getMember();
        }

        async getMember () {
            const orders = await rpc.query({route: "/get_payment_data"});
            return orders;
        }
        get orders ()  {
            debugger
            return this.member;
        }
        
        async _onClickLink(ev) {
            debugger        
            this.member = await rpc.query({ route: "/payment/form", 
                params:{name: this.state.name,
                    email: this.state.email,
                    currency: this.state.currency,
                }});
            this.render(true);
          
        }


        static template = xml`<div>
            <div class="container py-5">
                <div class="card border-0 mx-auto bg-100 rounded-0 shadow-sm bg-white o_database_list w-50 p-3">
                    <t t-set="summ" t-value="0.0"/>
                    <t t-foreach="orders[0]" t-as="order">
                    <div class="card-body">
                    <form method="post">
                    <div class="form-group">
                        <label>Name</label>
                        <input type="text" name='name' t-model="state.name"/>
                    </div>
                    <div class="form-group">
                        <label>code</label>
                        <input type="text" name='name' t-value="order.id" t-model="state.name"><t t-esc='order.name'/></input>
                    </div>
                    <table>
                    <th>name</th>
                    <th>amount</th>
                    <td><span t-esc="order.name" /></td>
                    <td><span t-esc="order.amount_total" /></td>
                    </table>

                <a class="btn btn-primary" t-on-click="_onClickLink">Submit</a>
                </form>
            </div>
            </t>
            </div>
        </div>
        </div>
        `;
    }

    function setup() {
        const OwlPaymentCreateInstance = new OwlPaymentCreate();
        OwlPaymentCreateInstance.mount($('.my_society_payment_component')[0]);
    }

    whenReady(setup);

    return OwlPaymentCreate;
});