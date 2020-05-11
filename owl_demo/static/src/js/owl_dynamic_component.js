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
            const rr = rpc.query({ route: "/get_order_detail", params:{order_id: ev.target.dataset.order_id}});
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
                            <a role="button" href="/get_data" t-on-click="modelFunction()" t-attf-data-order_id="{{d.id}}">details</a>
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
        const OwlDynamicDemoInstance = new OwlDynamicDemo();
        OwlDynamicDemoInstance.mount($('.my_dynamic_component')[0]);
    }

    whenReady(setup);

    return OwlDynamicDemo;
});
