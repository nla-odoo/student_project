odoo.define('task_owl.menu_component', function (require) {
    "use strict";

    const { Component } = owl;
    const { xml } = owl.tags;

    class Menu extends Component {

        get count() {
            return this.props.count;
        }

        static template = xml`
            <div class="topnav" id="myTopnav">
                <a href="#" class="fa fa-shopping-cart" data-mode='showCart'> <t t-esc="count"/></a>
                <a href="#">Home</a>
            </div>`;
    }
    return Menu;
});
