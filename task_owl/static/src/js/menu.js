odoo.define('task_owl.menu', function (require) {
    "use strict";

    // require('web.dom_ready');
    // if (!$('.menu_component').length) {
    //     return Promise.reject("DOM doesn't contain '.menu_component'");
    // }
    
    // const rpc = require('web.rpc');
    const { Component} = owl;
    const { xml } = owl.tags;
    // const { whenReady } = owl.utils;

    class menu extends Component {
        // async willStart() {
        //     console.log("2");
        //     this.total_item = await this.get_total_item_in_cart();
        // }

        // async get_total_item_in_cart() {
        //     console.log("3");
        //     const item_in_cart = await rpc.query({route: "/get_total_item"});
        //     console.log(item_in_cart)
        //     return item_in_cart
        // }
        // get item_in_cart ()  {
        //     return this.total_item;
        // }

         static template = xml`
         <div class="topnav" id="myTopnav">
          <a href="/display_cart"><i class="fa fa-shopping-cart"> </i></a>
          <a href="/product_list" class="active">Home</a>
        </div>`;
    }

    // function setup() {
    //     console.log("4");

    //     const OwlmenuInstance = new menu();
    //     OwlmenuInstance.mount($('.menu_component')[0]);
    // }

    // whenReady(setup);

    return menu;
});