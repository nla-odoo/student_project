odoo.define('loading_transportation_system.cust_vehicle', function (require) {
    "use strict";

    // require('web.dom_ready');
    // if (!$('.create_vehicle').length) {
    //     return Promise.reject("DOM doesn't contain '.create_vehicle'");
    // }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { useState } = owl.hooks;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class Vehicles_cust_Display extends Component {

        async willStart() {
            this.vehicledata = await this.getVehicle();
            this.att = await this.getatt();
            debugger
        }


        async getVehicle () {
            const vehicles = await rpc.query({route: "/cust_vehicle"});
            return vehicles;
        }

        async getatt () {
            const atts = await rpc.query({route:"/get_p_att"})
            return atts;
            debugger
        }


        get vehicles ()  {
            return this.vehicledata;
        }

        get atts (){
            return this.att.values;
        }


        // async modelFunction(ev) {
        //     const instance = new OwlProduct(null);
        //     instance.mount($('.create_vehicle')[0]);
        //     this.destroy();
        // }

        
        static template = xml`<div>
        <center><h1>Vehicles</h1></center>
        
        <table class="table table-stripded">
        <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Attribute</th>
        </tr>
        <tr t-foreach="vehicles" t-as="v">
        <td><t t-esc="v.name"/></td>
        <td><t t-esc="v.description"/></td>
        </tr>
        <tr t-foreach="atts" t-as="a">
        <td><t t-esc="a.name"/></td>
        </tr>
        </table>
        </div>`
    }


    return Vehicles_cust_Display;

    
});










// odoo.define('loading_transportation_system.vehicle', function (require) {
//     "use strict";

//     // require('web.dom_ready');
//     // if (!$('.create_vehicle').length) {
//     //     return Promise.reject("DOM doesn't contain '.create_vehicle'");
//     // }

//     const rpc = require('web.rpc');

//     const { Component, hooks } = owl;
//     const { useState } = owl.hooks;
//     const { xml } = owl.tags;
//     const { whenReady } = owl.utils;

//     class VehiclesDisplay extends Component {

//         async willStart() {
//             this.vehicledata = await this.getVehicle();
//             this.att = await this.getatt();
//             debugger
//         }


//         async getVehicle () {
//             const vehicles = await rpc.query({route: "/vehicle"});
//             return vehicles;
//         }

//         async getatt () {
//             const atts = await rpc.query({route:"/get_p_att"})
//             return atts;
//             debugger
//         }


//         get vehicles ()  {
//             return this.vehicledata;
//         }

//         get atts (){
//             return this.att;
//         }


//         async modelFunction(ev) {
//             const instance = new OwlProduct(null);
//             instance.mount($('.create_vehicle')[0]);
//             this.destroy();
//         }

        
//         static template = xml`<div>
//         <center><h1>Vehicles</h1></center>
//         <a role="button" href="#" t-on-click="modelFunction()" class="btn btn-primary">Create</a>
//         <table class="table table-stripded">
//         <tr>
//             <th>Name</th>
//             <th>Description</th>
//             <th>Attribute</th>
//         </tr>
//         <tr t-foreach="vehicles" t-as="v">
//         <td><t t-esc="v.name"/></td>
//         <td><t t-esc="v.description"/></td>
//         </tr>
//         <tr t-foreach="atts" t-as="a">
//         <td><t t-esc="a.name"/></td>
//         </tr>
//         </table>
//         </div>`
//     };

//     class OwlProduct extends Component {

//         async willStart() {
//             this.product_attribute = await this.get_product_attribute();
//         }

//         async get_product_attribute() {
//             const product_attribute = await rpc.query({ route: "/get_product_attribute" });
//             debugger
//             return product_attribute
//         }

//         _onClickLink(ev) {
//             var self = this;
//             const form = document.querySelector('#add_product_form');

//             let attribute_values = [];
//             form.querySelectorAll('.attribute_type').forEach(function(input) {
//                 if (input.checked) {
//                     attribute_values.push(parseInt(input.name));
//                 }
//             });

//             const params = {
//                 name: form.querySelector('input[name="name"]').value,
//                 list_price: form.querySelector('input[name="list_price"]').value,
//                 attribute_id: this.product_attribute.attribute_id,
//                 value_ids: attribute_values,

//             }

//             rpc.query({
//                 route: "/AddProduct_rpc",
//                 params: params
//             })

//             // window.location.href = "/web/login"
//         }

//         get attributes() {
//             debugger
//             return this.product_attribute.values;
//         }

//              async modelFunction(ev){
//             const instance = new VehiclesDisplay(null);
//             instance.mount($('.vehicle_create')[0]);
//             this.destroy();
//         }

//         static template = xml `
//             <div class="wrapper">
//                 <h2 style="color: #00A09D;"><u>Add Product</u></h2>
//                 <div class="col-md-6">
//                     <form id="add_product_form">
//                         <div class="form-group">
                        
//                             <input type="text" name="name" placeholder="Vehicle Name" class="form-control" />
//                         </div>
//                         <div class="form-group">
                            
//                             <label class="form-control">Product Type</label>
                        
//                             <div class="form-check" t-foreach="attributes" t-as="attribute">
//                                 <input type="checkbox" t-att-id="attribute.id" class="attribute_type" t-att-name="attribute.id" t-att-value="attribute.name"/>
//                                 <label for="attribute.id"> <t t-esc="attribute.name"/></label>
//                             </div>
//                         </div>
//                         <div class="form-group">
                            
//                             <input type="text" name="list_price" placeholder="Price" class="form-control" />
//                         </div>
//                         <div class="form-group">
//                             <input class="btn btn-primary" t-on-click="_onClickLink" type="button" value="Add Product" />
//                         </div>
//                     </form>
//                 </div>
//             </div>
//         `;
//     }


//     // class CreateVehicle extends Component {
//     //     constructor() {
//     //         super(...arguments);
//     //         this.state = useState({
//     //             description: "",
//     //             name:"",
//     //         });
//     //     }

//     //     async _onClickLink(ev) {
//     //         const self = this;
//     //         rpc.query({ route: "/vehicle/form",
//     //             params:{name: this.state.name,
//     //             description: this.state.description
//     //         }}).then(function (result) {
//     //             const instance = new VehiclesDisplay(null);
//     //             instance.mount($('.create_vehicle')[0]);
//     //             self.destroy();
//     //         });
//     //     }

//     //     async modelFunction(ev){
//     //         const instance = new VehiclesDisplay(null);
//     //         instance.mount($('.vehicle_create')[0]);
//     //         this.destroy();
//     //     }



//     //     static template = xml`<div>
//     //     <div>
//     //         <div>
//     //             <form method="post">
//     //                 <center><h1>Create Vehicle</h1></center>
//     //                 <div class="form-group">
//     //                     <label>Name</label>
//     //                     <input type="text" name='name' t-model="state.name" class="form-control"/>
//     //                 </div>
//     //                 <div class="form-group">
//     //                     <label>Description</label>
//     //                     <input type="text" name='description' t-model="state.description" class="form-control"/>
//     //                 </div>
//     //             <a t-on-click="_onClickLink" class="btn btn-primary">Submit</a>
//     //             </form>
//     //         </div>
//     //     </div>
//     //     </div>
//     //     `;

//     //     // static components = {VehiclesDisplay};
//     // }

//     // function setup() {
//     //     const VehiclesDisplayInstance = new VehiclesDisplay();
//     //     VehiclesDisplayInstance.mount($('.create_vehicle')[0]);
//     // }

//     // whenReady(setup);

//     // return VehiclesDisplay;

//     // function setup() {
//     //     const VehiclesInstance = new VehiclesDisplay();
//     //     VehiclesInstance.mount($('.vehicle_temp')[0]);
//     // }

//     // whenReady(setup);

//     // return VehiclesDisplay;
// });
