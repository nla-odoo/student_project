odoo.define('loading_transportation_system.customer_regi', function(require) {
    "use strict";

    require('web.dom_ready');

    if (!$('.customer_registrationform').length) {
        debugger;
        return Promise.reject("DOM doesn't contain '.customer_registrationform'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class Customer_Registration extends Component {

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
                <div class="col-md-6">
                    <form id="cust_form_data">
                        <div class="form-group">
                            <label>Customer Name</label>
                            <input type="text" name="name" placeholder="Customer Name" class="form-control" />
                        </div>
                        <div class="form-group">
                            <label>Contact Number</label>
                            <input type="text" name="mobile" placeholder="Contact No" class="form-control" />
                        </div>
                        <div class="form-group">
                            <label>Address</label>
                            <input type="text" name="address" placeholder="Address" class="form-control"/>
                        </div>
                        <div class="form-group">
                            <label>Email</label>
                            <input type="email" name="email" placeholder="Email" class="form-control" />
                        </div>
                        <div class="form-group">
                            <label>Password</label>
                            <input type="password" name="password" placeholder="Password" class="form-control"/>
                        </div>
                        <div class="form-group">
                            <input class="button" t-on-click="_onClickLink" type="button" value="Register" />
                        </div>
                    </form>
                </div>
            </div>
        `;
    }

    function setup() {
        const customerregiinst = new Customer_Registration();
        customerregiinst.mount($('.customer_registrationform')[0]);
    }

    whenReady(setup);

    return Customer_Registration;
});
