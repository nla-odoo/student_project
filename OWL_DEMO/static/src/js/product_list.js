odoo.define('OWL_DEMO.product_component', function (require) {
    "use strict";

    require('web.dom_ready');    
    const rpc = require('web.rpc');
    const Menu = require('OWL_DEMO.menu_component');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class Cart extends Component {

        async willStart() {
            this.cart = await this.get_cart_data();
            this.order = await this.get_order_data();
        }

        async get_cart_data () {
            const sale_order_lines = await rpc.query({route: "/get_cart_detail"});
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

        get order_line (){
            return this.order;
        }

        get item_in_cart () {
            return this.props;
        }

        paynow (){
            const payment_detail = rpc.query({route: "/get_cart_detail"});
        }

        homePage (ev) {
            if (ev.target.dataset.mode == 'showCart') {
                this.render(true);
            } else {
                const ProductListInstance = new Products(null);
                ProductListInstance.mount($('.product_list_component')[0]);
                this.destroy();
            }
        }

        static template = xml`
            <div>
                <Menu count="item_in_cart"  t-on-click="homePage()"/>
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
            </div>`;

        static components = {Menu};
    }

    class Products extends Component {
        async willStart() {
            this.product_data = await this.get_product_data();
            this.cartCount = await this.get_total_item_in_cart();
        }

        async get_product_data () {
            const products = await rpc.query({route: "/get_product_data"});
            return products;
        }
        get products ()  {
            return this.product_data;
        }

        async get_total_item_in_cart() {
            const cartCount = await rpc.query({route: "/get_total_item"});
            return cartCount
        }

        get item_in_cart ()  {
            return this.cartCount;
        }

        homePage (ev) {
            if (ev.target.dataset.mode == 'showCart') {
                const cartInstance = new Cart(null, this.cartCount);
                cartInstance.mount($('.product_list_component')[0]);
                this.destroy();
            } else {
                this.render(true);
            }
        }

        addToCart (ev) {
            return rpc.query({
                route: ev.target.action,
                params: {product_template_id: ev.target.querySelector('input[name="product_template_id"]').value}
            }).then((count) => {
                this.cartCount = count;
                this.render(true);
            });
        }

        static template = xml`
            <div>
            <Menu count="item_in_cart"  t-on-click="homePage()"/>
            <div class="container">
                <div id="main">
                    <section id="content">
                        <div id="left" >
                            <ul>
                                <t t-foreach="products" t-as="product" >
                                    <li>
                                        <div class="img">
                                            <a href="#">
                                                <img t-attf-src="data:image/png;base64, {{product.image_1920}}"/>
                                            </a>
                                        </div>
                                        <div class="info">
                                            <a class="title" href="#">
                                                <t t-esc="product.name"/>
                                            </a>
                                            <p>
                                                <b>Type : </b>
                                                <t t-if="product.type == 'consu'">Consumable</t>
                                                <t t-else="">
                                                    <t t-esc="product.type"/>
                                                </t>
                                            </p>
                                            <div class="price1">
                                                <span class="st">price:</span>
                                                    <t t-esc="product.list_price"/>
                                            </div>
                                            <div class="actions" t-if="product.active">
                                                <form action="/shop/cart/update" method="POST" t-on-submit.prevent="addToCart()">
                                                    <button type="submit" class="btn btn-success">Add to cart</button>
                                                    <a role="button" href="#">Inqury</a>
                                                    <input class="product_template_id" name="product_template_id" t-att-value="product.id" type="hidden"/>
                                                </form>
                                            </div>
                                        </div>
                                    </li>
                                </t>
                            </ul>
                        </div>
                    </section>
                </div>
            </div>
        </div>`;

        static components = {Menu};
    }


    function setup() {
        const ProductListInstance = new Products();
        ProductListInstance.mount($('.product_list_component')[0]);
    }

    if ($('.product_list_component').length) {
        whenReady(setup);
    }

    return {Products: Products, Cart: Cart};
});
