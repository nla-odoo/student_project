odoo.define('owl_society_managment.owl_dynamic_component', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_dynamic_component').length) {
        return Promise.reject("DOM doesn't contain '.my_dynamic_component'");
    }

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
        <div>
            <div>
                <form method="post">
                    
                    <div>
                        <label>Product name&#127980;</label>
                    </div>
                    <div>
                        <input type="text" name='name' t-model="state.name"/>
                    </div>
                    <div>
                        <label>Purchase</label>
                    </div>
                    <div>
                        <input type="checkbox" name='purchase_ok' t-model="state.purchase_ok"/>
                    </div>
                    <div>
                        <label>Sale</label>
                    </div>
                    <div>
                        <input type="checkbox" name='sale_ok' t-model="state.sale_ok"/>
                    </div>
                    <div>
                        <label>Rent</label>
                    </div>
                    <div>    
                        <input type="checkbox" name='rent_ok' t-model="state.rent_ok"/>
                    </div>
                
                    <div>
                        <label>Type</label>
                    </div>
                    <div>                 
                        <select id="Type" name="type" t-model="state.type">
                            <option value="consu">Consumable</option>
                            <option value="service">Service</option>
                        </select>
                    </div>
                    <div>
                        <label>Cost</label>
                        <input type="text" name='standard_price' t-model="state.standard_price"/>
                    </div>
                    <div>
                        <label>Sale price</label>
                        <input type="text" name='list_price' t-model="state.list_price"/>
                    </div>
                    <div>
                        <label>Subscription Product</label>
                        <input type="checkbox" id='recurring_invoice' name='recurring_invoice' t-model="state.recurring_invoice"/>    
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
                    </div>
                    <div>
                        <label for="Subscription Template">Subscription Template</label>
                        <select name="subscription_template_id" t-model="state.subscription_template_id" id="subscription_template_id" disabled="disabled">
                            <t t-foreach="subscriptions" t-as="subscription">
                                <option t-key="subscription" t-attf-value="{{subscription.id}}""><t t-esc="subscription.name"/></option>
                            </t>
                        </select>
                    
                    </div>
                    <div>
                        <label>Duration</label>
                        <input type="number" name='duration' t-model="state.duration"/>
                    </div>
                     <div>
                        <label>Unit</label>
                        <select id="unit" name="unit" t-model="state.unit">
                            <option value="hour">Hours</option>
                            <option value="day">Days</option>
                            <option value="week">Weeks</option>
                            <option value="month">Months</option>
                        </select>
                    </div>
                    <div>
                        <label>Price</label>
                        <input type="number" name='price' t-model="state.price"/>
                    </div>
                    <div>
                    <input id="file-upload" type="file" accept=".gif,.jpg,.jpeg,.png" name='image_1920' t-model="state.image_1920"/>
                    <script type="text/javascript" src="/owl_society_managment/static/src/js/img.js"/>
                    </div>
                <a t-on-click="_onClickLink">Submit</a>
                </form>
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