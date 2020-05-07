odoo.define('owl_search_box.owl_search_box', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_dynamic_search_box').length) {
        return Promise.reject("DOM doesn't contain '.my_dynamic_search_box'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlSearchBox extends Component {

        async willStart() {
            this.productsData = await this.getProductData();
        }

        async getProductData () {
            const products = await rpc.query({route: "/get_product_data"});
            return products;
        }

        get products ()  {
            return this.productsData;
        }

        static template = xml`<div><table id="product"><t t-foreach="products" t-as="product"><tr><td><t t-esc="product"/></td></tr></t></table></div>`;
    }

    function setup() {
        const OwlSearchBoxInstance = new OwlSearchBox();
        OwlSearchBoxInstance.mount($('.my_dynamic_search_box')[0]);
    }

    whenReady(setup);

    return OwlSearchBox;
});