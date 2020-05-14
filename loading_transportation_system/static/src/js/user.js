odoo.define('loading_transportation_system.user', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_user_component').length) {
        return Promise.reject("DOM doesn't contain '.my_user_component'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;


    class OwlUser extends Component {

        async willStart() {
            this.partnersdata = await this.getPartners();
        }

        async getPartners () {
            const partners = await rpc.query({route: "/get_partner_data"});
            return partners;
        }
        get partners ()  {
            return this.partnersdata;
        }

        static template = xml`
        <div class="card mr16" style="width: 18rem;">
            <div t-foreach="partners" t-as="partner">
                            <div class="card-body">
                                <p class="card-text">
                                    <strong>Name: </strong>
                                    <t t-esc="partner.name"/>
                                </p>
                                <p class="card-text">
                                    <strong>Address: </strong>
                                    <t t-esc="partner.street"/>
                                </p>
                                 <p class="card-text">
                                    <strong>Pin Code: </strong>
                                    <t t-esc="partner.zip"/>
                                </p>
                                <p class="card-text">
                                    <strong>City: </strong>
                                    <t t-esc="partner.city"/>
                                </p>
                                <p class="card-text">
                                    <strong>Email: </strong>
                                    <t t-esc="partner.email"/>
                                </p>
                                <p class="card-text">
                                    <strong>Phone: </strong>
                                    <t t-esc="partner.phone"/>
                                </p>
                                <p class="card-text">
                                    <strong>Type: </strong>
                                    <t t-esc="partner.type"/>
                                </p>
                            </div>
            </div>
            </div>`;

        
    }

    function setup() {
        const OwlUserInstance = new OwlUser();
        OwlUserInstance.mount($('.my_user_component')[0]);
    }

    whenReady(setup);

    return OwlUser;
});
