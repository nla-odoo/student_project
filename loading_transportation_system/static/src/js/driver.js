odoo.define('loading_transportation_system.driver', function (require) {
    "use strict";

    // require('web.dom_ready');
    // if (!$('.create_driver').length) {
    //     return Promise.reject("DOM doesn't contain '.create_driver'");
    // }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { useState } = owl.hooks;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class DriverDisplay extends Component {

        async willStart() {
            this.driverdata = await this.getDriver();
        }

        async getDriver () {
            const drivers = await rpc.query({route: "/driver"});
            return drivers;
        }
        get drivers ()  {
            return this.driverdata;
        }

        // async modelFunction(ev) {
        //     const instance = new CreateDriver(null);
        //     instance.mount($('.create_driver')[0]);
        //     this.destroy();
        // }

        
        static template = xml`<div>
        <center><h1>Drivers</h1></center>
        
        <table class="table table-stripded">
        <tr>
            <th>Name</th>
            <th>Description</th>
        </tr>
        <tr t-foreach="drivers" t-as="v">
        <td><t t-esc="v.name"/></td>
        <td><t t-esc="v.description"/></td>
        </tr>
        </table>
        </div>`
    }

    // class CreateDriver extends Component {
    //     constructor() {
    //         super(...arguments);
    //         this.state = useState({
    //             description: "",
    //             name:"",
    //         });
    //     }

    //     async _onClickLink(ev) {
    //         const self = this;
    //         rpc.query({ route: "/driver/form",
    //             params:{name: this.state.name,
    //             description: this.state.description
    //         }}).then(function (result) {
    //             const instance = new DriverDisplay(null);
    //             instance.mount($('.create_driver')[0]);
    //             self.destroy();
    //         });
    //     }

    //     async modelFunction(ev){
    //         const instance = new DriverDisplay(null);
    //         instance.mount($('.driver_create')[0]);
    //         this.destroy();
    //     }



    //     static template = xml`<div>
    //     <div>
    //         <div>
    //             <form method="post">
    //                 <center><h1>Create Drivers</h1></center>
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

    //     // static components = {VehiclesDisplay};
    // }

    // function setup() {
    //     const DriverDisplayInstance = new DriverDisplay();
    //     DriverDisplayInstance.mount($('.create_driver')[0]);
    // }

    // whenReady(setup);

    return DriverDisplay;

    
});







// odoo.define('loading_transportation_system.driver', function (require) {
//     "use strict";

//     // require('web.dom_ready');
//     // if (!$('.create_driver').length) {
//     //     return Promise.reject("DOM doesn't contain '.create_driver'");
//     // }

//     const rpc = require('web.rpc');

//     const { Component, hooks } = owl;
//     const { useState } = owl.hooks;
//     const { xml } = owl.tags;
//     const { whenReady } = owl.utils;

//     class DriverDisplay extends Component {

//         async willStart() {
//             this.driverdata = await this.getDriver();
//         }

//         async getDriver () {
//             const drivers = await rpc.query({route: "/driver"});
//             return drivers;
//         }
//         get drivers ()  {
//             return this.driverdata;
//         }

//         async modelFunction(ev) {
//             const instance = new CreateDriver(null);
//             instance.mount($('.create_driver')[0]);
//             this.destroy();
//         }

        
//         static template = xml`<div>
//         <center><h1>Drivers</h1></center>
//         <a role="button" href="#" t-on-click="modelFunction()" class="btn btn-primary">Create</a>
//         <table class="table table-stripded">
//         <tr>
//             <th>Name</th>
//             <th>Description</th>
//         </tr>
//         <tr t-foreach="drivers" t-as="v">
//         <td><t t-esc="v.name"/></td>
//         <td><t t-esc="v.description"/></td>
//         </tr>
//         </table>
//         </div>`
//     };

//     class CreateDriver extends Component {
//         constructor() {
//             super(...arguments);
//             this.state = useState({
//                 description: "",
//                 name:"",
//             });
//         }

//         async _onClickLink(ev) {
//             const self = this;
//             rpc.query({ route: "/driver/form",
//                 params:{name: this.state.name,
//                 description: this.state.description
//             }}).then(function (result) {
//                 const instance = new DriverDisplay(null);
//                 instance.mount($('.create_driver')[0]);
//                 self.destroy();
//             });
//         }

//         async modelFunction(ev){
//             const instance = new DriverDisplay(null);
//             instance.mount($('.driver_create')[0]);
//             this.destroy();
//         }



//         static template = xml`<div>
//         <div>
//             <div>
//                 <form method="post">
//                     <center><h1>Create Drivers</h1></center>
//                     <div class="form-group">
//                         <label>Name</label>
//                         <input type="text" name='name' t-model="state.name" class="form-control"/>
//                     </div>
//                     <div class="form-group">
//                         <label>Description</label>
//                         <input type="text" name='description' t-model="state.description" class="form-control"/>
//                     </div>
//                 <a t-on-click="_onClickLink" class="btn btn-primary">Submit</a>
//                 </form>
//             </div>
//         </div>
//         </div>
//         `;

//         // static components = {VehiclesDisplay};
//     }

//     // function setup() {
//     //     const DriverDisplayInstance = new DriverDisplay();
//     //     DriverDisplayInstance.mount($('.create_driver')[0]);
//     // }

//     // whenReady(setup);

//     return DriverDisplay;

    
// });

