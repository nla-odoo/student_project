odoo.define('owl_demo.owl_dynamic_component', function (require) {
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

        async getPartners () {
            const partners = await rpc.query({route: "/get_partner_data"});
            return partners;
        }
        get partners ()  {
            return this.partnersdata;
        }

        static template = xml`<div><div t-foreach="partners" t-as="partner"><t t-esc="partner"/></div></div>`;
    }

    function setup() {
        const OwlDynamicDemoInstance = new OwlDynamicDemo();
        OwlDynamicDemoInstance.mount($('.my_dynamic_component')[0]);
    }

    whenReady(setup);

    return OwlDynamicDemo;
});
