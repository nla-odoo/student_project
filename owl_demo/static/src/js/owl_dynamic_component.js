odoo.define('owl_demo.owl_dynamic_component', function(require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_dynamic_component').length) {
        return Promise.reject("DOM doesn't contain '.my_dynamic_component'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlDynamicDemo extends Component {

        async willStart() {
            this.partnersdata = await this.getPartners();
        }

        async getPartners() {
            const partners = await rpc.query({ route: "/get_partner_data" });
            return partners;
        }
        get partners() {
            debugger;
            return this.partnersdata;
        }

        static template = xml `
        <div>
            <div t-foreach="partners" t-as="partner">
            <t t-esc="partner"/>
                <t t-esc="partner.name"/>
                <li>
                    <div class="img">
                        <a href="#">
                        <img t-attf-src="data:image/png;base64, {{partner.image_1920}}"/>
                        </a>
                    </div>
                    <div class="info">
                        <a class="title" href="#">
                        <t t-esc="partner.name" />
                        </a>
                        <p><b>Type : </b>
                        <t t-if="partner.type == 'consu'">
                        Consumable
                        </t>
                        <t t-else="">
                        <t t-esc="partner.type" />
                        </t>
                        </p>
                    <div class="price1">
                        <span class="st">price:</span>
                        <strong>
                        <t t-esc="partner.list_price" />
                        </strong>
                    </div>
                    <div class="actions">
                        <a href="#">Add to cart
                        </a>
                        <a href="#">Inqury
                        </a>
                    </div>
                </div>
            </li>               
            </div>
        </div>`;
    }

    function setup() {
        const OwlDynamicDemoInstance = new OwlDynamicDemo();
        OwlDynamicDemoInstance.mount($('.my_dynamic_component')[0]);
    }

    whenReady(setup);

    return OwlDynamicDemo;
});