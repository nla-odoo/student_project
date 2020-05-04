odoo.define('task_owl.menu', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.menu_component').length) {
        return Promise.reject("DOM doesn't contain '.menu_component'");
    }
    
    const rpc = require('web.rpc');
    const product_list = require('task_owl.product_list_component');
    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class menu extends Component {
        async willStart() {
            debugger
            this.total_item = await this.get_total_item_in_cart();
        }

        async get_total_item_in_cart() {
            debugger
            const item_in_cart = await rpc.query({route: "/get_total_item"});
            console.log(item_in_cart)
            return item_in_cart
        }
        get item_in_cart ()  {
            debugger
            return this.total_item;
        }

        static components = {product_list};

        static template = xml`<div><div class="topnav" id="myTopnav">
  <a href="/display_cart"><i class="fa fa-shopping-cart"> <t t-esc="item_in_cart"/></i></a>
</div><product_list/></div>
`;
    }

    menu.components = {product_list};

    function setup() {
        const OwlmenuInstance = new menu();
        OwlmenuInstance.mount($('.menu_component')[0]);
    }

    whenReady(setup);

    return menu;
});