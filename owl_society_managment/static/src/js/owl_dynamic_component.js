odoo.define('owl_society_managment.owl_dynamic_component', function (require) {
    "use strict";

    // require('web.dom_ready');
    // if (!$('.my_dynamic_component').length) {
    //     return Promise.reject("DOM doesn't contain '.my_dynamic_component'");
    // }

    const rpc = require('web.rpc');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlDynamicDemo extends Component {
        constructor() {
        super(...arguments);
        this.state = useState({
            name: "",
            purchase_ok:"",
            sale_ok:"",
            type:"",
            standard_price:"",
            list_price:"",
            recurring_invoice:"",
            subscription_template_id:"",
            image_1920:"",
            rent_ok:"",
            duration:"",
            unit:"",
            price:"",
        });
    }

        async willStart() {

            this.product = await this.getProduct();
        }

        async getProduct () {
            const subscriptions = await rpc.query({route: "/get_Product_data"});
            console.log(subscriptions)
            return subscriptions;
        }
        get subscriptions ()  {
            return this.product;
        }
        
        async _onClickLink(ev) {
            var imgdata = localStorage.getItem("imgcontent");
            debugger
            console.log(imgdata);
            this.product = await rpc.query({ route: "/services/form", 
                params:{name: this.state.name , 
                    purchase_ok: this.state.purchase_ok ,
                    sale_ok: this.state.sale_ok ,
                    type: this.state.type ,
                    standard_price: this.state.standard_price ,
                    list_price:this.state.list_price,
                    image_1920:imgdata,
                    recurring_invoice:this.state.recurring_invoice,
                    subscription_template_id:this.state.subscription_template_id,
                    rent_ok:this.state.rent_ok,
                    duration:this.state.duration,
                    unit:this.state.unit,
                    price:this.state.price,

                }});
            this.render(true);   
        }


        static template = xml`<div>
        <div class="container py-5">
            <div class="card-body">
                <div>
                    <form method="post">
                        <div class="form-group">
                            <label>Product name</label>
                            <input type="text" name='name' t-model="state.name" class="form-control"/>
                        </div>
                        <div class="form-row">
                            <div class="form-group col-md-6">
                            <div class="form-check form-check-inline">
                                <label class="form-check-label" for="sale">Sale</label>
                                <input type="checkbox" name='sale_ok' t-model="state.sale_ok" class="form-check-input"/>
                            </div>
                            <div class="form-group">
                                <label>Type</label>                
                                <select id="Type" name="type" t-model="state.type" class="form-control">
                                    <option value="consu">Consumable</option>
                                    <option value="service">Service</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group col-md-6">
                            <label>Cost</label>
                            <input type="text" name='standard_price' t-model="state.standard_price" class="form-control"/>
                        </div>
                        <div class="form-group col-md-6">
                            <label>Sale price</label>
                            <input type="text" name='list_price' t-model="state.list_price" class="form-control"/>
                        </div>
                    </div>
                     <div class="form-check">
                            <input type="checkbox" id='recurring_invoice' name='recurring_invoice' t-model="state.recurring_invoice" class="form-check-input"/>     
                            <label  class="form-check-label">Subscription Product</label>
                    </div>
                    <script>
                        document.getElementById('recurring_invoice').onchange = function () {
                        if(("recurring_invoice")==(":checked")) {
                            document.getElementById("subscription_template_id").disabled = true;
                        }

                        else {
                            document.getElementById("subscription_template_id").disabled = false;
                        }
                        }   
                    </script>
                        <div class="form-group">
                            <label for="Subscription Template">Subscription Template</label>
                            <select name="subscription_template_id" t-model="state.subscription_template_id" id="subscription_template_id" disabled="disabled" class="form-control">
                                <t t-foreach="subscriptions" t-as="subscription">
                                    <option t-key="subscription" t-attf-value="{{subscription.id}}"><t t-esc="subscription.name"/></option>
                                </t>
                            </select>
                        </div>
                    <a class="btn btn-primary" t-on-click="_onClickLink">Submit</a>
                </form>
            </div>
        </div>
    </div>
</div>
        `;
    }

    // function setup() {
    //     const OwlDynamicDemoInstance = new OwlDynamicDemo();
    //     OwlDynamicDemoInstance.mount($('.my_dynamic_component')[0]);
    // }

    // whenReady(setup);

    return OwlDynamicDemo;
});