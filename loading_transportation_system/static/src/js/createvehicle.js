odoo.define('loading_transportation_system.createvehicle', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.create_vehicle').length) {
        return Promise.reject("DOM doesn't contain '.create_vehicle'");
    }
    const rpc = require('web.rpc');
    const vehicle = require('loading_transportation_system.vehicle');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class CreateVehicle extends Component {
        constructor() {
            super(...arguments);
            this.state = useState({
                description: "",
                name:"",
            });
        }

        async _onClickLink(ev) {
            const self = this;
            rpc.query({ route: "/vehicle/form",
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

        static components = {vehicle};
    }

    function setup() {
        const CreateVehicleInstance = new CreateVehicle();
        CreateVehicleInstance.mount($('.create_vehicle')[0]);
    }

    whenReady(setup);

    return CreateVehicle;
});
