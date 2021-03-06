odoo.define('loading_transportation_system.owl_dynamic_component', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_dynamic_component').length) {
        return Promise.reject("DOM doesn't contain '.my_dynamic_component'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlSubDemo extends Component {

        static template = xml`<div><t t-esc="props.name"/></div>`;
    }

    OwlSubDemo.props = ["name"];

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

        static template = xml`<div><div t-foreach="partners" t-as="partner"><OwlSubDemo name="partner"/></div></div>`;

        static components = {OwlSubDemo};
    }

    function setup() {
        const OwlDynamicDemoInstance = new OwlDynamicDemo();
        OwlDynamicDemoInstance.mount($('.my_dynamic_component')[0]);
    }

    whenReady(setup);

    return OwlDynamicDemo;
});
// odoo.define('loading_transportation_system.owl_dynamic_component', function (require) {
//     "use strict";

//     require('web.dom_ready');
//     if (!$('.my_dynamic_component').length) {
//         return Promise.reject("DOM doesn't contain '.my_dynamic_component'");
//     }

//     const rpc = require('web.rpc');

//     const { Component, hooks } = owl;
//     const { xml } = owl.tags;
//     const { whenReady } = owl.utils;

//     class OwlDynamicDemo extends Component {

//         async willStart() {
//             this.productdata = await this.getProducts();
//         }

//         async getProducts () {
//             const products = await rpc.query({route: "/product"});
//             return products;
//         }
//         get products ()  {
//             return this.productdata;
//         }

//         static template = xml`<div><div t-foreach="products" t-as="product"><t t-esc="product"/></div></div>`;
//     }

//     function setup() {
//         const OwlDynamicDemoInstance = new OwlDynamicDemo();
//         OwlDynamicDemoInstance.mount($('.my_dynamic_component')[0]);
//     }

//     whenReady(setup);

//     return OwlDynamicDemo;
// });