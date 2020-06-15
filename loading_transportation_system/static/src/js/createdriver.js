odoo.define('loading_transportation_system.createdriver', function (require) {
    "use strict";

    // require('web.dom_ready');
    // if (!$('.create_driver').length) {
    //     return Promise.reject("DOM doesn't contain '.create_driver'");
    // }

    const rpc = require('web.rpc');
    const driver = require('loading_transportation_system.driver');

    const { Component, hooks } = owl;
    const { useState } = owl.hooks;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    

    class CreateDriver extends Component {
        constructor() {
            super(...arguments);
            this.state = useState({
                description: "",
                name:"",
            });
        }

        async _onClickLink(ev) {
            const self = this;
            rpc.query({ route: "/driver/form",
                params:{name: this.state.name,
                description: this.state.description
            }}).then(function (result) {
                self.render(true);
                self.env.qweb.forceUpdate();
                self.destroy();
            });
        }


        static template = xml`<div>
        <div>
            <div>
                <form method="post">
                    <center><h1>Create Drivers</h1></center>
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

        static components = {driver};
    }

    // // function setup() {
    // //     const CreateDriverInstance = new CreateDriver();
    // //     CreateDriverInstance.mount($('.create_driver')[0]);
    // // }

    // whenReady(setup);

    return CreateDriver;

    
});




