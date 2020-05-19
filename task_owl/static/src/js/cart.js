odoo.define('task_owl.cart_component', function (require) {
    "use strict";

    const OwlSubDemo = require('task_owl.sub_component');
    const rpc = require('web.rpc');
    const { Component, hooks } = owl;
    const { xml } = owl.tags; 
    const { whenReady } = owl.utils;

    class Cart extends Component {
        async willStart() {
            this.cart = await this.get_cart_data();
            this.order = await this.get_order_data();
        }

        async get_cart_data () {
            console.log("asfkjabfkk------------")
            const sale_order_lines = await rpc.query({route: "/get_cart_detail"});
            console.log(sale_order_lines);
            return sale_order_lines;
        }

        async get_order_data(){
            console.log("asfkjabfkk")
            const order_line = await rpc.query({route: "/order"});
            console.log(order_line);
            return order_line;
        }

        get sale_order_lines ()  {
            return this.cart;
        }
        get order_line(){
            return this.order;
        }

        get item_in_cart () {
            return this.props
        }
         static template = xml`
        <div>
         <OwlSubDemo count="item_in_cart"  t-on-click="homePage()"/>

        <main>
                <div class="basket">
                    <div class="basket-labels">
                        <ul class="ul">
                            <li class="li item item-heading">Item</li>
                            <li class="li price">Price</li>
                            <li class="li quantity">Quantity</li>
                            <li class="li subtotal">Subtotal</li>
                        </ul>
                    </div>
                    <t t-foreach="sale_order_lines" t-as="sale_order_line">
                        
                    <div class="basket-product">
                        <div class="item">
                            <div class="product-image">
                            </div>
                            <div class="product-details">
                                <h1 class="h1">
                                    <strong>
                                        <t t-esc="sale_order_line.name"/></strong></h1>
                                <p>
                                </p>
                            </div>
                        </div>
                        <div class="price"><t t-esc="sale_order_line.price_unit"/></div>
                        <div class="quantity">
                            <input class="quantity-field input-button" name="quantity" min="1" type="number" value="1"/>
                        </div>
                        <div class="subtotal"><t t-esc="sale_order_line.price_unit"/></div>
                        <div class="remove">
                            <button class="input-button">Remove</button>
                        </div>
                    </div>
                </t>
                </div>
                <aside>
        <t t-foreach="order_line" t-as="order">

                    <div class="summary">
                        <div class="summary-total-items">
                            <span class="total-items"/>Items in your Bag</div>
                        <div class="summary-subtotal">
                            <div class="subtotal-title">Subtotal</div>
                            <div class="subtotal-value final-value" id="basket-subtotal">
                               <t t-if="order"><t t-esc="order.amount_total"/></t><t t-else="">0</t>
                            </div>
                        </div>
                        <div class="summary-total">
                            <div class="total-title">Total</div>
                            <div class="total-value final-value" id="basket-total">
                                <t t-if="order">
                                    <t t-esc="order.amount_total"/>
                                    <input type="hidden" name="contract_id" t-att-value="sale_order_lines.sale_order_id"/>                                        
                                    <input type="hidden" name="amount" t-att-value="order.amount_total"/>                                        
                                </t>
                                <t t-else="">0</t>
                            </div>
                        </div>
                        <div class="summary-checkout">
                            <button class="checkout-cta input-button" id="pay_now" t-on-click="paynow()">Checkout</button>
                        </div>                       
                    </div>
                    </t>
                    </aside>
            </main>
        </div>
        `;
    paynow(){
        console.log("asdadsAAAS")
        const payment_detail = rpc.query({route: "/get_cart_detail"});
    }
        static components = {OwlSubDemo};

    }

    // function setup() {
    //     const OwlCartInstance = new Cart();
    //     OwlCartInstance.mount($('.cart_component')[0]);
    // }

    // whenReady(setup);

    return Cart;
});