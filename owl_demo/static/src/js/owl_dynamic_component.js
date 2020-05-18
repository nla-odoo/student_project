odoo.define('owl_demo.owl_dynamic_component', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_dynamic_component').length) {
        return Promise.reject("DOM doesn't contain '.my_dynamic_component'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlDynamicDemo extends Component {

        async willStart() {
            this.orderdetail = await this.getdetails(this.props);
        }

        async getdetails (order_id) {
            const details = await rpc.query({route: "/order_detail", params: {order_id: order_id}});
            return details;

        }
        get details ()  {
            return this.orderdetail;
            debugger;
        }

        async modelFunction(ev) {
            const instance = new OwlDetailComponent(null);
            instance.mount($('.my_dynamic_component')[0]);
            this.destroy();
        }

        static template = xml`
        <div class="container-fluid">
            <br/><br/>
            <div class="card">
                <t t-foreach="details.order" t-as="d" t-key="id">
                    <div class="card-header bg-secondary">
                        <h4><span t-esc="d.name"/><span class="pull-right fa fa-arrow-left" t-on-click="modelFunction()"/></h4>
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

    class OwlDetailComponent extends Component {

    
        async willStart() {
            this.partnersdata = await this.getPartners();
        }

        async getPartners () {
            var partners = await rpc.query({route: "/get_partner_data"}); 
            return partners;
        }

        get partners ()  {
            this.myFunction();
            return this.partnersdata;
        }

        async modelFunction(ev){
            const instance = new OwlDynamicDemo(null, ev.target.dataset.order_id);
            instance.mount($('.my_dynamic_component')[0]);
            this.destroy();
        }

    
        static template = xml`<div class="container-fluid">
        <br/><br/>
        <div class="col-md-4">
            <h3>Select Chart</h3><select class="form-control" id="Intrestin" t-on-change="myFunction()">
                <option  disabled="disabled">Choose Chart</option> 
                <option selected="true" value="line">line</option>
                <option value="bar">bar</option>
                <option value="pie">pie</option>
                <option value="doughnut">doughnut</option>
                <option value="polarArea">polarArea</option>
            </select>
        </div>
        <br/><br/>
        <table class="table table-striped table-bordered table-hover">
            <thead class="thead-dark"   >
                <tr>
                    <th>Name</th>
                    <th>date</th>
                    <th>Action</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
                <t t-set="summ" t-value="0.0"/>
                <t t-foreach="partners" t-as="d" t-key="id">
                    <tr>
                        <td><a role="button" href="#" t-on-click="modelFunction()" t-attf-data-order_id="{{d.id}}"><span t-esc="d.name"/></a></td>
                        <td><span t-esc="d.date_order"/></td>
                        <td>
                        <form action="#" method="POST">
                            <a role="button" href="#" t-on-click="modelFunction()" t-attf-data-order_id="{{d.id}}">details</a>
                        </form>
                        </td>
                        <td><span t-esc="d.amount_total"/></td>
                        <t t-set="summ" t-value="summ + d.amount_total" />
                    </tr>
                </t>
                    <tr>
                        <td class="text-right" colspan="3"><h5>SubTotal : </h5></td>
                        <td><h5><span t-esc="summ"/></h5></td>
                    </tr>
            </tbody>
        </table>
        </div>

        `;

    async myFunction() {  
        var data = await this.getPartners();
        var i;
        var a = [];
        var b = [];
        for (i = 0; i < data.length; i++) 
        {
            var values = data[i].amount_total;
            a.push(values); 
            var name = data[i].name;
            b.push(name);
        }
        var ctx = document.getElementById('myChart');
        var chart = new Chart(ctx, {
            type: document.getElementById("Intrestin").value,
            data: {
                labels: b,
                datasets: [{
                label: "Products",
                backgroundColor: ["orange","yellow","green","red","#3e95cd", "#8e5ea2","#3cba9f"],
                data: a
                }] },
            });

    }
}

    function setup() {
        const OwlDetailComponentInstance = new OwlDetailComponent();
        OwlDetailComponentInstance.mount($('.my_dynamic_component')[0]);
    }

    whenReady(setup);

    return OwlDetailComponent;
});
