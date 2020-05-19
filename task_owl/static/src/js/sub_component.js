odoo.define('task_owl.sub_component', function (require) {
    "use strict";

    // const rpc = require('web.rpc');
    const { Component, hooks } = owl;
    const { xml } = owl.tags;

    class sub_component extends Component {

        get count() {
            return this.props.count;
        }


        static template = xml`<div class="topnav" id="myTopnav">
              <a href="#" class="fa fa-shopping-cart" data-mode='showCart'> <t t-esc="count"/></a>
              <a href="#">Home</a>
            </div>`;
    }
    return sub_component;
});
