odoo.define('owl_society_managment.jounral_create', function (require) {
    "use strict";

    // require('web.dom_ready');
    // if (!$('.my_jounral_create_component').length) {
    //     return Promise.reject("DOM doesn't contain '.my_jounral_create_component'");
    // }
    const rpc = require('web.rpc');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlJounralCreate extends Component {
        constructor() {
        super(...arguments);
        this.state = useState({
            name: "",
            type:"",
            code:"",
        });
    }
        async willStart() {
            this.jounral = await this.getJounral();
        }

        async getJounral () {
            return this.jounrals;
        }
        get jounrals ()  {
            debugger
            return this.jounral;
        }
        
        async _onClickLink(ev) {
            debugger        
            this.jounral = await rpc.query({ route: "/jounral/form", 
                params:{name: this.state.name,
                    type: this.state.type,
                    code: this.state.code,
                }});
            this.render(true);
          
        }


        static template = xml`<div>
        <div class="container py-5">
            <div class="card-body">
                <form method="post">
                    <div class="form-group">
                        <label>Name</label>
                        <input type="text" name='name' t-model="state.name" class="form-control"/>
                    </div>
                    <div>
                        <label>Type</label>
                        <select id="type" name="type" t-model="state.type" class="form-control">
                            <option value="sale">Sale</option>
                            <option value="purchase">Purchase</option>
                            <option value="cash">cash</option>
                            <option value="bank">bank</option>
                            <option value="genral">Miscellaneous</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Short Code</label>
                        <input type="text" name='code' t-model="state.code" class="form-control"/>
                    </div>
                <button class="btn btn-primary" t-on-click="_onClickLink">Submit</button>
                </form>
            </div>
        </div>
        </div>
        `;
    }

    // function setup() {
    //     const OwlJounralCreateInstance = new OwlJounralCreate();
    //     OwlJounralCreateInstance.mount($('.my_jounral_create_component')[0]);
    // }

    // whenReady(setup);

    return OwlJounralCreate;
});