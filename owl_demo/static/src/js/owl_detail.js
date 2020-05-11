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
            this.orderdetail = await this.getdetails();
        }

        async getdetails () {
            const details = await rpc.query({route: "/order_detail"});
            console.log("part",details.details);
            return details;

        }
        get details ()  {
            return this.orderdetail;
            debugger;
        }

        static template = xml`
        <div class="container-fluid">
            <br/><br/>
            <div class="card">
                <t t-foreach="details.order" t-as="d" t-key="id">
                    <div class="card-header bg-secondary">
                        <h4><span t-esc="d.name"/></h4>
                    </div>
                    <div class="card-body">
                        <h5>Order Date : <span t-esc="d.date_order"/></h5>
                        <t t-foreach="details.partner" t-as="d" t-key="id">
                            <h5>Shipping Address : </h5>
                            <h6> <span t-esc="d.name" /> , </h6>
                            <h6> <span t-esc="d.street" /> , </h6>
                            <h6><span t-esc="d.city"/> - <span t-esc="d.zip"/></h6>
                            <br/><br/>
                        </t>
                <br/><br/>
                <h4>Price :</h4>
                    <table class="table table-striped  table-hover">
                    <thead class="thead-dark">
                        <th>Name</th>
                        <th>Quantity</th>
                        <th>Unit Price</th>
                        <th>Taxes</th>
                        <th>Amount</th>
                    </thead>
                    <t t-set="summ" t-value="0.0"/>
                    <t t-foreach="details.details" t-as="d">
                    <tr class="value">
                        <td><span t-esc="d.name" /></td>
                        <td><span t-esc="d.product_uom_qty" /></td>
                        <td><span t-esc="d.price_unit" /></td>
                        <td class="sum"><span t-esc="d.price_tax" /></td>
                        <td class="sum"><span t-esc="d.price_total" /></td>
                        <t t-set="summ" t-value="summ + d.price_total + d.price_tax" />
                    </tr>
                    </t>
                    <tr>
                        <td class="text-right" colspan="4"><h5>SubTotal : </h5></td>
                        <td><h5><span t-esc="summ"/></h5></td>
                    </tr>
                    </table>
                </div> 
                </t>       
            </div>
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
