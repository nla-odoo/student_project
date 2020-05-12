odoo.define('loading_transportation_system.createlead', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.create_lead').length) {
        return Promise.reject("DOM doesn't contain '.create_lead'");
    }
    const rpc = require('web.rpc');
    const lead = require('loading_transportation_system.lead');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class CreateLead extends Component {
        constructor() {
            super(...arguments);
            this.state = useState({
                description: "",
                name:"",
            });
        }

        async _onClickLink(ev) {
            const self = this;
            rpc.query({ route: "/lead/form",
                params:{name: this.state.name,
                description: this.state.description
            }}).then(function (result) {
                self.render(true);
                self.env.qweb.forceUpdate();
            });
        }


        static template = xml`<div>
        <div>
            <div>
                <form method="post">
                    <center><h1>Create Inquirey</h1></center>
                    <div class="form-group">
                        <label>Name</label>
                        <input type="text" name='name' t-model="state.name" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>Description</label>
                        <input type="text" name='description' t-model="state.description" class="form-control"/>
                    </div>

                <a t-on-click="_onClickLink" class="btn btn-primary">Submit</a>
                </form>
            </div>
        </div>
        </div>
        `;

        static components = {lead};
    }

    function setup() {
        const CreateLeadInstance = new CreateLead();
        CreateLeadInstance.mount($('.create_lead')[0]);
    }

    whenReady(setup);

    return CreateLead;
});


// odoo.define('loading_transportation_system.createlead', function (require) {
//     "use strict";

//     require('web.dom_ready');
//     if (!$('.create_lead').length) {
//         return Promise.reject("DOM doesn't contain '.create_lead'");
//     }

//     const { Component, hooks } = owl;
//     const { xml } = owl.tags;
//     const { whenReady } = owl.utils;

//     class OwlCreateLead extends Component {


//         static template = xml`<div>
//         <div>
//             <div>
//                 <center><h1>Create_Inquirey</h1></center>
//                 <form method="post" t-attf-action="/lead/form/">
//                     <div class="form-group">
//                         <label>Description</label>
//                         <input type="text" name='description' class='form-control'/>
//                     </div>
//                     <div class="form-group">
//                         <label>Partner_Id</label>
//                         <input type="text" name='partner_id' class='form-control'/>
//                     </div>
//                     <div class="form-group">
//                         <label>Name</label>
//                         <input type="text" name='name' class='form-control'/>
//                     </div>
//                 <button type="submit" class="btn btn-primary">Create</button>
//                 </form>
//             </div>
//         </div>
//         </div>
//         `;
//     }

//     function setup() {
//         const OwlCreateLeadInstance = new OwlCreateLead();
//         OwlCreateLeadInstance.mount($('.create_lead')[0]);
//     }

//     whenReady(setup);

//     return OwlCreateLead;
// });