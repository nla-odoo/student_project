odoo.define('task_owl.sub_component', function (require) {
    "use strict";

    // const rpc = require('web.rpc');
    const { Component, hooks } = owl;
    const { xml } = owl.tags;

    class sub_component extends Component {
        static template = xml`<div class="topnav" id="myTopnav">
  <a href="/display_cart"><i class="fa fa-shopping-cart"> <t t-esc="props.item_in_cart"/></i></a>
  <a href="/product_list">Home</a>
</div>`;
    }
    return sub_component;
});
