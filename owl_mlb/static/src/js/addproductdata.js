odoo.define('owl_mlb.addproductdata', function(require) {
    "use strict";

    require("web.dom_ready");

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlProduct extends Component {

        async willStart() {
            this.product_attribute = await this.get_product_attribute();
            debugger
        }

        async get_product_attribute() {
            const product_attribute = await rpc.query({ route: "/get_product_attribute" });
            debugger
            return product_attribute
        }

        _onClickLink(ev) {
            var self = this;
            const form = document.querySelector('#add_product_form');

            let attribute_values = [];
            form.querySelectorAll('.attribute_type').forEach(function(input) {
                if (input.checked) {
                    attribute_values.push(parseInt(input.name));
                }
            });

            const params = {
                image_1920: form.querySelector('input[name="image_1920"]').value,
                name: form.querySelector('input[name="name"]').value,
                list_price: form.querySelector('input[name="list_price"]').value,
                attribute_id: this.product_attribute.attribute_id,
                value_ids: attribute_values,
            }

            console.log(">>>>>>>>>>>>>>>>>>", params)

            rpc.query({
                route: "/AddProduct_rpc",
                params: params
            })
        }

        get attributes() {
            debugger
            return this.product_attribute.values;
        }

        static template = xml `
            <div class="wrapper">
                <h2>Add Product</h2>
                <div class="form-conteniar">
                    <form id="add_product_form">
                        <div class="input-name">
                            <i class="fa fa-cutlery email"></i>
                            <input type="text" name="name" placeholder="Food Name" class="text-name" />
                        </div>
                        <div class="input-name">
                            <i class="fa fa-product-hunt email"></i>
                            <label class="text-name">Product Type</label>
                            <i class="fas fa-utensil-spoon"></i>
                            <div class="form-check" t-foreach="attributes" t-as="attribute">
                                <input type="checkbox" t-att-id="attribute.id" class="attribute_type" t-att-name="attribute.id" t-att-value="attribute.name"/>
                                <label for="attribute.id"> <t t-esc="attribute.name"/></label>
                            </div>
                        </div>
                        <div class="input-name">
                            <i class="fa fa-rupee email"></i>
                            <input type="text" name="list_price" placeholder="Price" class="text-name" />
                        </div>
                        <div class="input-name">
                            <i class="fa fa-camera email"></i>
                            <input name="image_1920" type="file" class="text-name" />
                            <img t-attf-src="" height="200" alt="Image preview..." />
                        </div>
                        <div class="input-name">
                            <input class="button" t-on-click="_onClickLink" type="button" value="Add Product" />
                        </div>
                    </form>
                </div>
            </div>
        `;
    }

    return OwlProduct;
});
