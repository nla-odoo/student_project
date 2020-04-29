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
console.log("asdddd");

            const products = await rpc.query({route: "/get_product_data"});
            console.log(JSON.parse(products));
            const abc =JSON.parse(products);
            console.log(abc)
            console.log("awfssdv"+products[5])
            // return products;
        }
        get products ()  {
            return this.product_data;
        }
         static template = xml`     
         <div>
hjbkbkbjkbkjb
</div>
                                `;

//          static template = xml`     
//          <div>
//                             <div  t-foreach="products" t-as="product">
//                                                 <img t-attf-src="data:image/png;base64, {{product}}"/>

// </div>
// </div>
//                                 `;
    }

    function setup() {
        const OwlDemoInstance = new OwlDemo();
        OwlDemoInstance.mount($('.product_list_component')[0]);
    }

    whenReady(setup);

    return OwlDemo;
});