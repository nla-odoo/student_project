odoo.define('loading_transportation_system.createvehicle', function (require) {
    "use strict";

    // require('web.dom_ready');
    // if (!$('.create_vehicle').length) {
    //     return Promise.reject("DOM doesn't contain '.create_vehicle'");
    // }
    const rpc = require('web.rpc');
    const vehicle = require('loading_transportation_system.vehicle');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class CreateVehicle extends Component {

            async willStart() {
            this.product_attribute = await this.get_product_attribute();
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
                name: form.querySelector('input[name="name"]').value,
                list_price: form.querySelector('input[name="list_price"]').value,
                description: form.querySelector('input[name="description"]').value,
                attribute_id: this.product_attribute.attribute_id,
                value_ids: attribute_values,
            }

            rpc.query({
                route: "/AddProduct_rpc",
                params: params
            })

            // window.location.href = "/web/login"
        }

        get attributes() {
            debugger
            return this.product_attribute.values;
        }

        async modelFunction(ev){
        const instance = new VehiclesDisplay(null);
        instance.mount($('.vehicle_create')[0]);
        this.destroy();
        }

        static template = xml `
            <div class="wrapper">
                <h2 style="color: #00A09D;"><u>Add Product</u></h2>
                <div class="col-md-6">
                    <form id="add_product_form">
                        <div class="form-group">
                        
                            <input type="text" name="name" placeholder="Vehicle Name" class="form-control" />
                        </div>

                        <div class="form-group">
                            <input type="text" name="description" placeholder="description" class="form-control" />
                        </div>

                        <div class="form-group">
                            
                            <label class="form-control">Product Type</label>
                        
                            <div class="form-check" t-foreach="attributes" t-as="attribute">
                                <input type="checkbox" t-att-id="attribute.id" class="attribute_type" t-att-name="attribute.id" t-att-value="attribute.name"/>
                                <label for="attribute.id"> <t t-esc="attribute.name"/></label>
                            </div>
                        </div>

                        <div class="form-group">
                            
                            <input type="text" name="list_price" placeholder="Price" class="form-control" />
                        </div>
                        <div class="form-group">
                            <input class="btn btn-primary" t-on-click="_onClickLink" type="button" value="Add Product" />
                        </div>


                    </form>
                </div>
            </div>
        `;
    }



    //     constructor() {
    //         super(...arguments);
    //         this.state = useState({
    //             description: "",
    //             name:"",
    //         });
    //     }

    //     async _onClickLink(ev) {
    //         const self = this;
    //         rpc.query({ route: "/vehicle/form",
    //             params:{name: this.state.name,
    //             description: this.state.description
    //         }}).then(function (result) {
    //             self.render(true);
    //             self.env.qweb.forceUpdate();
    //         });
    //     }


    //     static template = xml`<div>
    //     <div>
    //         <div>
    //             <form method="post">
    //                 <center><h1>Create Vehicle</h1></center>
    //                 <div class="form-group">
    //                     <label>Name</label>
    //                     <input type="text" name='name' t-model="state.name" class="form-control"/>
    //                 </div>
    //                 <div class="form-group">
    //                     <label>Description</label>
    //                     <input type="text" name='description' t-model="state.description" class="form-control"/>
    //                 </div>
    //             <a t-on-click="_onClickLink" class="btn btn-primary">Submit</a>
    //             </form>
    //         </div>
    //     </div>
    //     </div>
    //     `;

    //     static components = {vehicle};
    // }

    // // function setup() {
    // //     const CreateVehicleInstance = new CreateVehicle();
    // //     CreateVehicleInstance.mount($('.create_vehicle')[0]);
    // // }

    // // whenReady(setup);

    return CreateVehicle;
});