odoo.define('owl_mlb.addproductdata', function(require) {
	"use strict";

	require("web.dom_ready");

    if (!$('.addproductdata').length) {
        debugger;
        return Promise.reject("DOM doesn't contain '.addproductdata'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlProduct extends Component {

    	 // async willStart(){
      //       console.log('hhhhhhhhhhhhhhhh')
      //       this.Regist = await rpc.query({
      //           route: '/Meal_Register_rpc'
      //       });
      //       debugger;
      //   }
        
        async _onClickLink(ev) {
            debugger
            const form = document.querySelector('#add_product_form');
            let formData = new FormData(form);
            formData = Object.fromEntries(formData);
            
            this.product = await rpc.query({
                route: "/AddProduct_rpc", 
                params: {'form_data': formData}
            });
            debugger
            
            // window.location.href = "/web/login"
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
                            <i class="fa fa-rupee email"></i>
                            <input type="text" name="list_price" placeholder="Price" class="text-name" />
                        </div>
                        <div class="input-name">
                            <input class="button" t-on-click="_onClickLink" type="button" value="Add Product" />
                        </div>
                    </form>
                </div>
            </div>
        `;
    }

    function setup() {
        const productInstance = new OwlProduct();
        productInstance.mount($('.addproductdata')[0]);
    }

    whenReady(setup);

    return OwlProduct;
});
