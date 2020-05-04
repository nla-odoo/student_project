odoo.define('owl_demo.owl_dynamic_component', function (require) {
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

        async willStart() {
            this.partnersdata = await rpc.query({ route: "/get_partner_data", params:{ 
                offset: this.offset, limit: this.limit}});
            for (let index = 1; index <= parseInt(this.partnersdata.count); index++) {
                this.count.push(index);
            }
        }
        async _onClickLink(ev) {
            ev.preventDefault();
            let offset = ev.target.getAttribute('offset');
            if (offset == 0) { offset = 1; }
            this.partnersdata = await rpc.query({ route: "/get_partner_data", params:{ 
                offset: parseInt(offset), limit: this.limit}});
                this.render(true);
            debugger;
          
        }

        static template = xml`
            <div>
                <link rel="stylesheet" type="text/scss" href="/owl_demo/static/src/csss/app.css"/>
                <div class="container">
                    <div id="main">
                        <section id="content">
                            <div id="left">
                                <ul id="ulcontent">
                                    <t t-log='partner_templates' />
                                    <t t-as="partner" t-foreach="partnersdata.product_list">
                                        <li>
                                            <div class="img">
                                                <t t-if="partner.image">
                                                    <img t-att-src="'data:image/jpg;base64,' + partner.image" />
                                                </t>
                                            </div>
                                            <div class="info">
                                                <a class="title" href="#">
                                                    <t t-esc="partner.name" />
                                                </a>
                                                <p><b>Type : </b>
                                                    <t t-if="partner.type == 'consu'">Consumable</t>
                                                    <t t-else="">
                                                        <t t-esc="partner.type" />
                                                    </t>
                                                </p>
                                                <div class="price1">
                                                    <span class="st">price:</span>
                                                    <strong>
                                                            <span>
                                                                <t t-esc="partner.price" />
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
    }

    function setup() {
        const OwlDynamicDemoInstance = new OwlDynamicDemo();
        OwlDynamicDemoInstance.mount($('.my_dynamic_component')[0]);
    }

    whenReady(setup);

    return OwlDynamicDemo;
});
