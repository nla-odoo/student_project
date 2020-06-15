odoo.define('loading_transportation_system.order', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.create_order').length) {
        return Promise.reject("DOM doesn't contain '.create_order'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { useState } = owl.hooks;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OrdersDisplay extends Component {

        async willStart() {
            this.orderdata = await this.getOrder();
        }


        async getOrder () {
            const orders = await rpc.query({route: "/get_order"});
            return orders;
        }

        get orders ()  {
            return this.orderdata;
        }

        async modelFunction(ev) {
            const instance = new Order(null);
            instance.mount($('.create_order')[0]);
            this.destroy();
        }

        
        static template = xml`<div>
        <center><h1>Orders</h1></center>
        <a role="button" href="#" t-on-click="modelFunction()" class="btn btn-primary">Create</a>
        <table class="table table-stripded">
        <tr>
            <th>date_order</th>
            <th>amount_total</th>
            <th>amount_tax</th>
            <th>name</th>
            <th>price_total</th>
            <th>price_unit</th>
            <th>price_tax</th>
            <th>product_uom_qty</th>

        </tr>
        <tr t-foreach="orders" t-as="o">
        <td><t t-esc="o.amount_total"/></td>
        <td><t t-esc="o.amount_tax"/></td>
        <td><t t-esc="o.name"/></td>
        <td><t t-esc="o.price_total"/></td>
        <td><t t-esc="o.price_unit"/></td>
        <td><t t-esc="o.price_tax"/></td>
        <td><t t-esc="o.product_uom_qty"/></td>
        </tr>
        </table>
        </div>`
    };
    class Order extends Component {

        constructor() {
            super(...arguments);
            this.state = useState({
                amount_tax:"",
                amount_total:"",
                name:"",
                price_total:"",
                price_unit:"",
                price_tax:"",
                product_uom_qty:"",
            });
        }

        async _onClickLink(ev) {
            const self = this;
            rpc.query({ route: "/order/form",
                params:{
                amount_tax: this.amount_tax,
                amount_total: this.state.amount_total,
                name: this.state.name,
                price_total: this.state.price_total,
                price_unit: this.state.price_unit,
                price_tax: this.state.price_tax,
                product_uom_qty: this.state.product_uom_qty


            }}).then(function (result) {
                const instance = new OrdersDisplay(null);
                instance.mount($('.create_order')[0]);
                self.destroy();
            });
        }

        async modelFunction(ev){
            const instance = new OrdersDisplay(null);
            instance.mount($('.order_create')[0]);
            this.destroy();
        }



        static template = xml`<div>
        <div>
            <div>
                <form method="post">
                    <center><h1>Order</h1></center>
                    <div class="form-group">
                        <label>Date</label>
                        <input type="datetime" name='date_order' t-model="state.date_order" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>Amount</label>
                        <input type="number" name='amount_total' t-model="state.amount_total" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>Amount_Tax</label>
                        <input type="number" name='amount_tax' t-model="state.amount_tax" class="form-control"/>
                    </div>
                     <div class="form-group">
                        <label>name</label>
                        <input type="text" name='name' t-model="state.name" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>price_total</label>
                        <input type="number" name='price_total' t-model="state.price_total" class="form-control"/>
                    </div>
                     <div class="form-group">
                        <label>price_unit</label>
                        <input type="number" name='price_unit' t-model="state.price_unit" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>price_tax</label>
                        <input type="number" name='price_tax' t-model="state.price_tax" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>product_uom_qty</label>
                        <input type="number" name='product_uom_qty' t-model="state.product_uom_qty" class="form-control"/>
                    </div>
                <a t-on-click="_onClickLink" class="btn btn-primary">Submit</a>
                </form>
            </div>
        </div>
        </div>
        `;
    }


    function setup() {
        const OrdersDisplayInstance = new OrdersDisplay();
        OrdersDisplayInstance.mount($('.create_order')[0]);
    }

    whenReady(setup);

    return OrdersDisplay;


});

