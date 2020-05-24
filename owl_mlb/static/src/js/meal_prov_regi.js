odoo.define('owl_mlb.meal_prov_regi', function(require) {
    "use strict";

    require('web.dom_ready');

    if (!$('.meal_register_component').length) {
        debugger;
        return Promise.reject("DOM doesn't contain '.meal_register_component'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class owlRegistration extends Component {

        async willStart(){
            this.Regist = await rpc.query({
                route: '/Meal_Register_rpc'
            });
            debugger;
        }
        
        async _onClickLink(ev) {
            debugger
            const form = document.querySelector('#registration_form');
            let formData = new FormData(form);
            formData = Object.fromEntries(formData);
            
            this.registartion = await rpc.query({
                route: "/Meal_Register_rpc", 
                params: {'form_data': formData}
            });
            
            window.location.href = "/web/login"
        }

        static template = xml `
            <div class="wrapper">
                <h2>Meal Provider Registration</h2>
                <div class="form-conteniar">
                    <form id="registration_form">
                        <div class="input-name">
                            <i class="fa fa-building email"></i>
                            <input type="text" name='name' placeholder="Company Name" class="text-name" />
                        </div>
                        <div id="currncy_id" class="input-name">
                        <select name="currency_id" class="form-control currency_id">
                            <t t-foreach="Regist.result" t-as="currency"  t-key="'row_' + row_index">
                                <option t-att-value="currency.id">
                                    <t t-esc="currency.name" />                                   
                              </option>
                            </t>
                        </select>
                        </div>
                        <div class="input-name">
                            <i class="fa fa-phone email"></i>
                            <input type="text" name="contact_no" placeholder="Contact No" class="text-name" />
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
                            <input class="button" type="submit" t-on-click="_onClickLink" value="Register" />
                        </div>
                    </form>
                </div>
            </div>
        `;
    }

    function setup() {
        const RegiInstance = new owlRegistration();
        RegiInstance.mount($('.meal_register_component')[0]);
    }

    whenReady(setup);

    return owlRegistration;
});