odoo.define('owl_society_managment.complaint_create', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_complaint_create_component').length) {
        return Promise.reject("DOM doesn't contain '.my_complaint_create_component'");
    }
    const rpc = require('web.rpc');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlComplaintCreate extends Component {
        constructor() {
        super(...arguments);
        this.state = useState({
            name: "",
        });
    }
        async willStart() {
            this.complaint = await this.getComplaint();
        }

        async getComplaint () {
            return this.complaint;
        }
        get complaint ()  {
            debugger
            return this.complaint;
        }
        
        async _onClickLink(ev) {
            debugger        
            this.complaint = await rpc.query({ route: "/complaint/form", 
                params:{name: this.state.name,
                }});
            this.render(true);
          
        }


        static template = xml`<div>
        <div>
            <div>
                <form method="post">
                    <div>
                        <label>Complaint name</label>
                        <input type="text" name='name' t-model="state.name"/>
                    </div>
                <a t-on-click="_onClickLink">Submit</a>
                </form>
            </div>
        </div>
        </div>
        `;
    }

    function setup() {
        const OwlComplaintCreateInstance = new OwlComplaintCreate();
        OwlComplaintCreateInstance.mount($('.my_complaint_create_component')[0]);
    }

    whenReady(setup);

    return OwlComplaintCreate;
});