odoo.define('loading_transportation_system.order_display', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.orderdisplay').length) {
        return Promise.reject("DOM doesn't contain '.orderdisplay'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { useState } = owl.hooks;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OrdersDisplay extends Component {

        async willStart() {
            this.orderdata = await this.getOrders();
            
        }


        async getVehicle () {
            const orders = await rpc.query({route: "/get_order"});
            return orders;
        }

        


        get orders ()  {
            return this.orderdata;
        }




        // async modelFunction(ev) {
        //     const instance = new OwlProduct(null);
        //     instance.mount($('.create_vehicle')[0]);
        //     this.destroy();
        // }

        
        static template = xml`<div>
        <center><h1>Vehicles</h1></center>
        
        <table class="table table-stripded">
        <tr>
            <th>Name</th>
            <th>Description</th>
    
        </tr>
        <tr t-foreach="vehicles" t-as="v">
        <td><t t-esc="v.amount_total"/></td>
        </tr>
        </table>
        </div>`
    }


    return VehiclesDisplay;

    
});

