odoo.define('owl_mlb.add_to_cart', function(require) {
    "use strict";

    require("web.dom_ready");

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class AddToCart extends Component {
        
        static template = xml `
            <div>
                Cart
            </div>
        `;
    }

    return AddToCart;
});