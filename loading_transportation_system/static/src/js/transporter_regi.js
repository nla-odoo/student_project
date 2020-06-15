odoo.define('loading_transportation_system.transporter_regi', function(require) {
    "use strict";

    require('web.dom_ready');

    if (!$('.transporter_registrationform').length) {
        debugger;
        return Promise.reject("DOM doesn't contain '.transporter_registrationform'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class Transporter_Registration extends Component {

        async willStart(){
            this.Regist = await rpc.query({
                route: '/Transporter_Register_rpc'
            });
            debugger;
        }
        
        async _onClickLink(ev) {
            debugger
            const form = document.querySelector('#registration_form');
            let formData = new FormData(form);
            formData = Object.fromEntries(formData);
            
            this.registartion = await rpc.query({
                route: "/Transporter_Register_rpc", 
                params: {'form_data': formData}
            });
            
            window.location.href = "/web/login"
        }

        static template = xml `
            <div class="wrapper">
                <h2>Transporter_Registration</h2>
                <br/>
                <div class="col-md-6">
                    <form id="registration_form">
                        <div class="form-group">
                            <label>Company Name</label>
                            <input type="text" name='name' placeholder="Company Name" class="form-control" />
                        </div>
                        <div id="currncy_id" class="input-name">
                        <label>Currency</label>
                        <select name="currency_id" class="form-control currency_id">
                            <t t-foreach="Regist.result" t-as="currency"  t-key="'row_' + row_index">
                                <option t-att-value="currency.id">
                                    <t t-esc="currency.name" />                                   
                              </option>
                            </t>
                        </select>
                        </div>
                        <div class="form-group">
                            <label>Contact No </label>
                            <input type="text" name="contact_no" placeholder="Contact No" class="form-control" />
                        </div>
                        <div class="form-group">
                            <label>Address</label>
                            <input type="text" name="address" placeholder="Address" class="form-control" />
                        </div>
                        <div class="form-group">
                            <label>Email</label>
                            <input type="email" name="email" placeholder="Email" class="form-control" />
                        </div>
                        <div class="form-group">
                            <label>Password</label>
                            <input type="password" name="password" placeholder="Password" class="form-control" />
                        </div>
                        <div class="form-group">
                            <input class="button" type="submit" t-on-click="_onClickLink" value="Register" />
                        </div>
                    </form>
                </div>
            </div>
        `;
    }

    function setup() {
        const RegiInstance = new Transporter_Registration();
        RegiInstance.mount($('.transporter_registrationform')[0]);
    }

    whenReady(setup);

    return Transporter_Registration;
});
