odoo.define('loading_transportation_system.sub_component', function (require) {
    "use strict";

    const { Component } = owl;
    const { xml } = owl.tags;

    class Menu extends Component {

        get count() {
            return this.props.count;
        }

        static template = xml`
            <div class="topnav" id="myTopnav">
                <a href="#" class="nav-left">Home</a>
                <a href="#" class="nav-left">mymenu</a>
            </div>`;
    }
    return Menu;
});
