odoo.define('owldemo.menu_component', function(require) {
    "use strict";

    require('web.dom_ready');

    if (!$('.menu_component').length) {
        return Promise.reject("DOM doesn't contain '.menu_component'");
    }

    const rpc = require('web.rpc');
    const session = require('web.session');
    
    const meal_register = require('owl_mlb.meal_register_component');
    const pager_cust = require('owl_mlb.my_dynamic_component');
    const customer_register = require('owl_mlb.customerRegi');
    const addproductdata = require('owl_mlb.addproductdata');
    const viewProduct = require('owl_mlb.viewProduct');
    // const add_to_cart = require('owl_mlb.add_to_cart');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class menu extends Component {
        isCustomer = false;

        async willStart() {
            this.toRegsiter = !session.user_id;
            this.isCustomer = await rpc.query({ route: '/is_customer' });
            this._renderMenuItem();
        }

        _renderMenuItem(mode) {
            if (this.toRegsiter) {
                mode = mode || 'home';
                if (mode === 'home') {
                    const homeInstance = new pager_cust();
                    homeInstance.mount($('.component_view')[0]);
                } else if (mode === 'registerAsCustomer') {
                    const customerRegisterInstance = new customer_register();
                    customerRegisterInstance.mount($('.component_view')[0]);
                } else if (mode === 'registerAsMeal') {
                    const mealRegisterInstance = new meal_register();
                    mealRegisterInstance.mount($('.component_view')[0]);
                }
                // else if (mode === 'add_to_cart') {
                //     const addtocartInstance = new add_to_cart();
                //     addtocartInstance.mount($('.component_view')[0]);
                // }
            } else {
                mode = mode || 'addProduct';
                if (mode === 'addProduct') {
                    const addProductInstance = new addproductdata();
                    addProductInstance.mount($('.component_view')[0]);
                } else if (mode === 'viewProduct') {
                    const viewProductInstance = new viewProduct();
                    viewProductInstance.mount($('.component_view')[0]);
                }
            }
        }

        get register () {
            return this.toRegsiter;
        }

        _onClickMenuItem(ev) {
            ev.preventDefault();
            const mode = ev.target.dataset.mode;
            $('.component_view').html('');
            this._renderMenuItem(mode);
            this.el.querySelector('.active').classList.remove('active');
            this.el.querySelector('a[data-mode="' + mode + '"]').classList.add('active');
        }

        static template = xml `
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav" t-on-click="_onClickMenuItem">
                    <t t-if="register">
                        <li class="nav-item">
                            <a class="nav-link active fa fa-home home" href="#" data-mode="home"></a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#" data-mode="registerAsCustomer">Register as Customer</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#" data-mode="registerAsMeal">Register as Meal</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link fa fa-shopping-basket cart" href="#" data-mode=""></a>
                        </li>
                    </t>
                    <t t-else="">
                        <li class="nav-item">
                            <a class="nav-link active" href="#" data-mode="addProduct">Add Product</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#" data-mode="viewProduct">View Product</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#" data-mode="studentList">Order</a>
                        </li>
                    </t>
                </ul>
            </div>
        </nav>`;
    }

    function setup() {
        const menuinstance = new menu();
        $('.o_portal.container').html('');
        menuinstance.mount($('.o_portal.container')[0]);
    }

    whenReady(setup);
    return menu;
});
