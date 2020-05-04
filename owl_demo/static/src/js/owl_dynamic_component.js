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
            debugger;
            const ulContent = this.el.querySelector('#ulcontent');
            ulContent.innerHTML = '';
            for (const partner of this.partnersdata.product_list) {
                const li = document.createElement("li");
                // image
                const imgDiv = document.createElement('div');
                imgDiv.setAttribute("class", 'img');
               
                    const image = document.createElement('img');
                    image.setAttribute('src', `data:image/jpg;base64, ${partner.image}`);
                    imgDiv.appendChild(image);
               
                li.appendChild(imgDiv);

                // info div
                const infoDiv = document.createElement('div');
                infoDiv.setAttribute("class", "info");

                // a tag
                const linkTitle = document.createElement('a');
                linkTitle.setAttribute('class', 'title');
                linkTitle.setAttribute('href', '#!');
                linkTitle.textContent = partner.name;
                infoDiv.appendChild(linkTitle);

                // p tag
                const pTag = document.createElement('p');
                const bTag = document.createElement('b');
                bTag.textContent = 'Type :';
                pTag.appendChild(bTag);
                if (partner.type == 'consu') {
                    pTag.textContent = 'Consumable';
                } else {
                    pTag.textContent = partner.type;
                }
                infoDiv.appendChild(pTag);

                // div price
                const priceDiv = document.createElement('div');
                priceDiv.setAttribute("class", "price1");

                const stSpan = document.createElement('span');
                stSpan.setAttribute('class', 'st');
                stSpan.textContent = 'price:';
                priceDiv.appendChild(stSpan);

                const strong = document.createElement('strong');
                strong.textContent = partner.price;
                priceDiv.appendChild(strong);
                infoDiv.appendChild(priceDiv);

                // div action
                const divAction = document.createElement('div');
                divAction.setAttribute("class", "actions");

                const addToCartLink = document.createElement('a');
                addToCartLink.setAttribute('href', "#!");
                addToCartLink.textContent = "Add to cart";
                divAction.appendChild(addToCartLink);

                const inquryLink = document.createElement('a');
                inquryLink.setAttribute('href', "#!");
                inquryLink.textContent = "Add to cart";
                divAction.appendChild(inquryLink);
                infoDiv.appendChild(divAction);

                li.appendChild(infoDiv);
                ulContent.appendChild(li);
            }
        }

        static template = xml`
            <div>
                <style type="text/css">
                    .container {
                        margin: 30px auto 0;
                        position: relative;
                        text-align: left;
                        width: 1000px;
                        padding-left: 20px;
                        padding-right: 20px;
                    }
                    /* main section */
                    
                    #main {
                        background-color: #fff;
                        padding: 20px 0;
                    }
                    
                    #content {
                        overflow: hidden;
                    }
                    
                    #content ul {
                        list-style: none outside none;
                        margin: 0;
                        padding: 0;
                    }
                    
                    #content #left ul li {
                        float: left;
                        padding-bottom: 21px;
                        width: 33%;
                    }
                    
                    #content #left ul li .img {
                        text-align: center;
                    }
                    
                    #content #left ul li .img img {
                        height: 128px;
                        width: 128px;
                    }
                    
                    #content #left ul li .info {
                        padding: 17px 20px 0 19px;
                    }
                    
                    #content ul li .info .title {
                        color: #4B4B4B;
                        display: inline-block;
                        font-size: 11px;
                        font-weight: bold;
                        line-height: 16px;
                        text-decoration: none;
                        text-transform: uppercase;
                        width: 150px;
                    }
                    
                    #content #left ul li .info p {
                        color: #7F7F7F;
                        font-size: 11px;
                        line-height: 16px;
                        padding-top: 3px;
                    }
                    
                    #content #left ul li .info .price1 {
                        background: none repeat scroll 0 0 #F7F7F7;
                        color: #383838;
                        font-size: 12px;
                        font-weight: bold;
                        line-height: 16px;
                        margin: 17px 0 10px;
                        padding: 6px 0 6px 8px;
                    }
                    
                    #content #left ul li .info .price1 .st {
                        color: #7F7F7F;
                        font-size: 11px;
                        line-height: 16px;
                        margin-right: 3px;
                    }
                    
                    #content #left ul li .info .actions a {
                        border: 1px solid #E0E0E0;
                        color: #fd7a01;
                        display: block;
                        float: right;
                        font-size: 11px;
                        font-weight: bold;
                        line-height: 16px;
                        padding: 5px;
                        text-decoration: none;
                    }
                    
                    #content #left ul li .info .actions a:first-child {
                        color: #009832;
                        float: left;
                    }
                </style>
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
