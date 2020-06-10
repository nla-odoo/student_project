odoo.define('owl_mlb.customerRegi', function(require) {
    "use strict";

    require('web.dom_ready');

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class owlCustomer extends Component {

         async _onClickLink(ev) {
            debugger
            const form = document.querySelector('#cust_form_data');
            let formData = new FormData(form);
            formData = Object.fromEntries(formData);
            
            this.custregistartion = await rpc.query({
                route: "/Cust_Register_rpc", 
                params: {'form_data': formData}
            });
            
            window.location.href = "/web/login"
        }

        static template = xml `
            <div class="wrapper">
                <h2>Customer Registration</h2>
                <div class="form-conteniar">
                    <form id="cust_form_data">
                        <div class="input-name">
                            <i class="fa fa-user email"></i>
                            <input type="text" name="name" placeholder="Customer Name" class="text-name" />
                        </div>
                        <div class="input-name">
                            <i class="fa fa-phone email"></i>
                            <input type="text" name="mobile" placeholder="Contact No" class="text-name" />
                        </div>
                        <div class="input-name">
                            <i class="fa fa-address-book email"></i>
                            <input type="text" name="address" placeholder="Address" class="text-name" />
                        </div>
                        <div class="input-name">
                            <i class="fa fa-envelope email"></i>
                            <input type="email" name="email" placeholder="Email" class="text-name" />
                        </div>
                        <div class="input-name">
                            <i class="fa fa-lock lock"></i>
                            <input type="password" name="password" placeholder="Password" class="text-name" />
                        </div>
                        <div class="input-name">
                            <input class="button" t-on-click="_onClickLink" type="button" value="Register" />
                        </div>
                    </form>
                </div>
            </div>
        `;
    }

    return owlCustomer;
});