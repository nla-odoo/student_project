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
            var i;
            var a = [];
            var b = [];
            for (i = 0; i < partners.length; i++) 
            {
                var td = partners[i].amount_total;
                a.push(td); 
                var name = partners[i].name;
                b.push(name);
            }
            console.log("a",a);
            var ctx = document.getElementById('myChart');
            var chart = new Chart(ctx, 
            {
                type: 'bar',
                data: {
                  labels: b,
                  datasets: [
                    {
                      label: "order details",
                      backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f"],
                      data: a
                    }
                  ]
                },
            });
        
            return partners;
        }

        get partners ()  {
            return this.partnersdata;
        }

        static template = xml`<div>
        <table class="table" border="2">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>date</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
                    <t t-set="summ" t-value="0.0"/>
                        <t t-foreach="partners" t-as="d" t-key="id">
                            <tr>
                                <td><a t-attf-href="/get_data/{{d.id}}"><span t-esc="d.name"/></a></td>
                                <td><span t-esc="d.date_order"/></td>
                                <td><span t-esc="d.amount_total"/></td>
                                <t t-set="summ" t-value="summ + d.amount_total" />
                            </tr>
                        </t>
                        <tr>
                            <td class="text-right" colspan="2"><h5>SubTotal : </h5></td>
                            <td><h5><span t-esc="summ"/></h5></td>
                        </tr>
            </tbody>
        </table>
        </div>
        `;
    }

    function setup() {
        const OwlDynamicDemoInstance = new OwlDynamicDemo();
        OwlDynamicDemoInstance.mount($('.my_dynamic_component')[0]);
    }

    whenReady(setup);

    return OwlDynamicDemo;
});
