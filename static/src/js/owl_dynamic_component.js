odoo.define('owl_search_component.owl_dynamic_component', function(require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_dynamic_component').length) {
        return Promise.reject("DOM doesn't contain '.my_dynamic_component'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlDynamicDemo extends Component {

        offset = 1;
        limit = 6
        count = [];
        order = {
            "name_asc": "name asc",
            "name_desc": "name desc",
            "list_price_asc": "list_price asc",
            "list_price_desc": "list_price desc"
        }

        async willStart() {
            this.partnersdata = await this._getProducts(this.offset);
            for (let index = 1; index <= parseInt(this.partnersdata.count); index++) {
                this.count.push(index);
            }
        }

        async _onClickLink(ev) {
            ev.preventDefault();
            let offset = ev.currentTarget.getAttribute('offset');
            let order = ev.currentTarget.getAttribute('order');
            this.partnersdata = await this._getProducts(offset, order);
            this.render(true);

        }

        async _getProducts(offset, order) {
            this.Products = await rpc.query({
                route: "/get_product_data",
                params: { offset: parseInt(offset), limit: this.limit, order: order }
            });
            return this.Products;
        }

        async _onButtonKeyup(ev) {
            var input, filter, ulcontent, li, i, txtValue;
            input = document.getElementById("search");
            filter = input.value.toUpperCase();
            ulcontent = document.getElementById("ulcontent")
            li = ulcontent.getElementsByTagName("li");
            txtValue = document.getElementsByClassName('text-lowercase');
            for (i = 0; i < li.length; i++) {
                if (!txtValue[i].innerHTML.toUpperCase().includes(filter)) { 
                    li[i].style.display="none"; 
                } 
                else { 
                    li[i].style.display="";                  
                }
            }
            this.render(true);
        }

        static template = xml `
            <div>
                <div class="container">
                    <div id="main">
                        <section id="content">
                            <div>
                                <input type="text" id="search" name="search" class="search" t-on-keyup="_onButtonKeyup" placeholder="Search..."/>
                                Sort By : 
                                <div class="dropdown">
                                    <span>--select--</span>
                                    <div class="dropdown-content">
                                        <a t-att-offset="offset" t-att-order="order['name_asc']" t-on-click="_onClickLink" href="#!">Name : A to Z</a><br/>
                                        <a t-att-offset="offset" t-att-order="order['name_desc']" t-on-click="_onClickLink" href="#!">Name : Z to A</a><br/>
                                        <a t-att-offset="offset" t-att-order="order['list_price_asc']" t-on-click="_onClickLink" href="#!">Price : Low to High</a><br/>
                                        <a t-att-offset="offset" t-att-order="order['list_price_desc']" t-on-click="_onClickLink" href="#!">Price : High to Low</a><br/>
                                    </div>
                                </div>
                            </div>
                            <div id="left">
                                <ul id="ulcontent">
                                    <t t-log='partner_templates' />
                                    <t t-as="product" t-foreach="partnersdata.results">
                                        <li>
                                            <div class="img">
                                               
                                                    <img t-att-src="'data:image/jpg;base64,' + product.image_1920" />
                                                
                                            </div>
                                            <div class="info text-wrap">
                                                <a class="title" href="#">
                                                <p class="text-lowercase">
                                                    <t t-esc="product.name" />
                                                </p>
                                                </a>
                                                <p><b>Type : </b>
                                                    <t t-if="product.type == 'consu'">Consumable</t>
                                                    <t t-else="">
                                                        <t t-esc="product.type" />
                                                    </t>
                                                </p>
                                                <div class="price1">
                                                    <span class="st">price:</span>
                                                    <strong>
                                                            <span>
                                                                <t t-esc="product.list_price" />
                                                                </span></strong>
                                                </div>
                                                <div class="actions">
                                                    <a href="#">Add to cart</a>
                                                    <a href="#">Inqury</a>
                                                </div>
                                            </div>
                                        </li>
                                    </t>
                                </ul>
                            </div>
                        </section>
                    <div class="d-flex justify-content-center">
                        <nav aria-label="Page navigation example">
                            <ul class="pagination">
                                <t t-set="offset" t-value="0"/>
                                <t t-as="page" t-foreach="count">
                                    <li class="page-item">
                                        <a t-att-offset="offset" t-att-order="partnersdata.order" t-on-click="_onClickLink" class="page-link" href="#!"><span t-esc="page" /></a>
                                        <t t-set="offset" t-value="offset + 6"/>
                                    </li>
                                </t>
                            </ul>
                        </nav>
                        <t t-esc="partnersdata.order" />
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    function setup() {
        const OwlDynamicDemoInstance = new OwlDynamicDemo();
        OwlDynamicDemoInstance.mount($('.my_dynamic_component')[0]);
    }

    whenReady(setup);

    return OwlDynamicDemo;
});