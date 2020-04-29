odoo.define('owl_demo.owl_component', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.product_list_component').length) {
        return Promise.reject("DOM doesn't contain '.my_component'");
    }
    
    const rpc = require('web.rpc');
    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlDemo extends Component {
        async willStart() {
            this.product_data = await this.get_product_data();
        }

        async get_product_data () {
            const products = await rpc.query({route: "/get_product_data"});
            console.log(products)
            return products
        }
        get products ()  {
            return this.product_data;
        }
         static template = xml`
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
                        <strong>
                            <t t-esc="product.list_price"/>
                        </strong>
                    </div>
                    <div class="actions">
                        <form action="/shop/cart/update" method="POST" t-if="product.active">
                            <a role="button" href="#" onclick="this.parentNode.submit();">Add to cart</a>
                            <a role="button" href="#">Inqury</a>
                            <input class="product_template_id" name="product_template_id" t-att-value="product.id" type="hidden"/>
                        </form>
                    </div>
                </div>
            </li>
        </t>
        `;
    }

    function setup() {
        const OwlDemoInstance = new OwlDemo();
        OwlDemoInstance.mount($('.product_list_component')[0]);
    }

    whenReady(setup);

    return OwlDemo;
});