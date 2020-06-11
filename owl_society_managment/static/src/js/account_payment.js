odoo.define('owl_society_managment.account_payment', function (require) {
    "use strict";

    // require('web.dom_ready');
    // if (!$('.account_payment').length) {
    //     return Promise.reject("DOM doesn't contain '.account_payment'");
    // }   

    const rpc = require('web.rpc');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OrderDetails extends Component {

        async willStart() {
            this.orderdetail = await this.getdetails(this.props);
            debugger;
        }

        async getdetails (order_id) {
            const details = await rpc.query({route: "/order_details", params: {order_id: order_id}});
            return details;

        }
        get details ()  {
            return this.orderdetail;
        }

        async modelFunction(ev) {
            const instance = new OrderList(null);
            instance.mount($('.component_view')[0]);
            this.destroy();
        }

        static template = xml`
        <div class="container-fluid">
            <br/><br/>
            <div class="card">
                <t t-foreach="details.order" t-as="order" t-key="id">
                    <div class="card-header bg-secondary">
                        <h4><span t-esc="order.name"/><span class="pull-right fa fa-arrow-left" t-on-click="modelFunction()"/></h4>
                    </div>
                    <div class="card-body">
                        <h5>Date : <span t-esc="order.date"/></h5>
                        <t t-foreach="details.partner" t-as="partner" t-key="id">
                            <h5>Name : </h5>
                            <h6> <span t-esc="partner.name" /> , </h6>
                            <h6> <span t-esc="partner.street" /> , </h6>
                            <h6><span t-esc="partner.city"/> - <span t-esc="partner.zip"/></h6>
                            <br/><br/>
                        </t>
                <br/><br/>
                <h4>Price :</h4>
                    <table class="table table-striped  table-hover">
                    <thead class="bg-primary">
                        <th>Name</th>
                        <th>Taxes</th>
                        <th>Amount</th>
                    </thead>
                    <t t-set="summ" t-value="0.0"/>
                    
                        <t t-foreach="details.order" t-as="d">
                            
                            <tr class="value">
                                <td><span t-esc="d.name" /></td>
                                <td class="sum"><span t-esc="d.amount_tax" /></td>
                                <td class="sum"><span t-esc="d.amount_total" /></td>
                                <t t-set="summ" t-value="summ + d.amount_total + d.amount_tax" />
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

    class OrderList extends Component {

    
        async willStart() {
            debugger
            this.Listdata = await this.getOrderList();
        }

        async getOrderList () {
            var orderList = await rpc.query({route: "/gets_order_details"}); 
            return orderList;
        }

        get orderList ()  {
            this.myFunction();
            return this.Listdata;
        }

        async modelFunction(ev){
            const instance = new OrderDetails(null, ev.target.dataset.order_id);
            instance.mount($('.component_view')[0]);
            this.destroy();
        }

    
        static template = xml`<div class="container-fluid">
        <br/><br/>
        <div class="container">
            <div class='col-md-6 border border-light rounded mx-auto'>
                <canvas id="myChart" style="width: 80%; height: 80%;"></canvas>    
            </div>
            <div class="col-md-6  mx-auto">
            <h3>Select Chart</h3><select class="form-control" id="Intrestin" t-on-change="myFunction()">
                <option  disabled="disabled">Choose Chart</option> 
                <option selected="true" value="line">line</option>
                <option value="bar">bar</option>
                <option value="pie">pie</option>
                <option value="doughnut">doughnut</option>
                <option value="polarArea">polarArea</option>
            </select>
            </div>
        </div>
        <br/><br/>
        <table class="table table-striped table-bordered table-hover">
            <thead class="bg-primary">
                <tr>
                    <th>Name</th>
                    <th>date</th>
                    <th>Action</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
                <t t-set="summ" t-value="0.0"/>
                <t t-foreach="orderList" t-as="d" t-key="id">
                    <tr>
                        <td><span t-esc="d.name"/></td>
                        <td><span t-esc="d.date"/></td>
                        <td><a role="button" href="#" t-on-click="modelFunction()" t-attf-data-order_id="{{d.id}}">details</a></td>
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
        var data = await this.getOrderList();
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

    // function setup() {
    //     const OrderListInstance = new OrderList();
    //     OrderListInstance.mount($('.account_payment')[0]);
    // }

    // whenReady(setup);

    return OrderList;
});