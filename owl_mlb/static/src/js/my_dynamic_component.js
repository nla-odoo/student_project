odoo.define('owl_mlb.my_dynamic_component', function(require) {
    "use strict";

    require('web.dom_ready');

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlDynamicDemo extends Component {
        static template = xml `
            <div>
                <div class="container">
                    <div id="main">
                        <section id="content">
                            <div id="left">
                                <ul id="ulcontent">
                                    <t t-log='partner_templates' />
                                    <t t-esc="console.log(partnersdata)"/>
                                    <t t-as="product" t-foreach="partnersdata.result">
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
                                                        <span><t t-esc="product.list_price" /></span>
                                                    </strong>
                                                </div>
                                                <div class="actions">
                                                    <a href="#!" t-on-click="addToCart()">Add to Cart</a>
                                                    <a href="#">Inquiry</a>
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
                                            <a t-att-offset="offset" t-on-click="_onClickLink" class="page-link" href="#!"><span t-esc="page" /></a>
                                            <t t-set="offset" t-value="offset + 6"/>
                                        </li>
                                    </t>
                                </ul>
                            </nav>
                        </div>
                    </div>
                </div>
            </div>
        `;

        offset = 1;
        limit = 6
        count = [];

        async willStart() {
            this.partnersdata = await this._getProducts(this.offset);
            for (let index = 1; index <= parseInt(this.partnersdata.count); index++) {
                this.count.push(index);
            }
        }
        
        async _onClickLink(ev) {
            ev.preventDefault();
            let offset = ev.currentTarget.getAttribute('offset');
            this.partnersdata = await this._getProducts(offset);
            this.render(true);
        }

        async _getProducts(offset) {
            this.Products = await rpc.query({
                route: "/get_partner_data",
                params: { offset: parseInt(offset), limit: this.limit }
            });
            return this.Products;
        }

        addToCart(ev) {
            return rpc.query({
                route: ev.target.action,
                params: {product_template_id: ev.target.querySelector('input[name="product_template_id"]').value}
            })
            // .then((count) => {
            //     this.cartCount = count;
            //     this.render(true);
            // });
        }
    }

    return OwlDynamicDemo;
});
