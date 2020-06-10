odoo.define('owl_mlb.viewProduct', function(require) {
    "use strict";

    require("web.dom_ready");

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class ViewProduct extends Component {
        async willStart(){
            debugger
            this.product_data = await rpc.query({route: '/get_products'});
            // console.log('>>>>>>>>>>>', product_data)
        }

        get products() {
            debugger
            return this.product_data;
        }

        static template = xml `
            <div>
                <table class="table">
                    <tr>
                        <th>Product Name</th>
                        <th>Product Type</th>
                        <th>Price</th>
                    </tr>
                    <tr t-foreach="products.getpro" t-as="product">
                        <td><t t-esc="product.name"/></td>
                        <td>
                            <t t-set="pro_data" t-value="product_data.data[product.id + '_' + product.name]"/>
                            <t t-foreach="pro_data" t-as="data">
                                <span t-esc="data.name"/><p></p>
                            </t>
                        </td>
                        <td><t t-esc="product.list_price"/></td>
                    </tr>                    
                </table>
            </div>
        `;
    }

    return ViewProduct;
});