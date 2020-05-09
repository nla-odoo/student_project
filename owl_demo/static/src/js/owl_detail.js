odoo.define('owl_demo.owl_detail', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.detail_component').length) {
        return Promise.reject("DOM doesn't contain '.detail_component'");
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
            const partners = await rpc.query({route: "/get_order_detail"});
            console.log("part",partners);
            return partners;

        }
        get partners ()  {
            return this.partnersdata;
            debugger;
        }

        static template = xml`
        <div class="container-fluid">
                            <table class="table table-condensed">
                                <th>Name</th>
                                <th>Quantity</th>
                                <th>Unit Price</th>
                                <th>Taxes</th>
                                <th>Amount</th>

                                <t t-foreach="partners" t-as="d">
                                <tr>
                                <td><span t-esc="d.name" /></td>
                                    <td><span t-esc="d.product_uom_qty" /></td>
                                    <td><span t-esc="d.price_unit" /></td>
                                    <td class="sum"><span t-esc="d.price_tax" /></td>
                                    <td class="sum"><span t-esc="d.price_total" /></td>
                                </tr>
                                </t>
                            </table>
            </div>
        `;
    }

    function setup() {
        const OwlDynamicDemoInstance = new OwlDynamicDemo();
        OwlDynamicDemoInstance.mount($('.detail_component')[0]);
    }

    whenReady(setup);

    return OwlDynamicDemo;
});
