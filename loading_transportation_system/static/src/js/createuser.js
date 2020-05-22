odoo.define('loading_transportation_system.createuser', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.create_user').length) {
        return Promise.reject("DOM doesn't contain '.create_user'");
    }
    const rpc = require('web.rpc');
    const lead = require('loading_transportation_system.createuser');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class CreateUser extends Component {
        constructor() {
            super(...arguments);
            this.state = useState({
                name: "",
                companyname:"",
                password:"",
                email:"",
            });
        }

        async _onClickLink(ev) {
            const self = this;
            rpc.query({ route: "/register/form",
                params:{name: this.state.name,
                companyname: this.state.companyname,
                password: this.state.password,
                email: this.state.email
            }}).then(function (result) {
                self.render(true);
                self.env.qweb.forceUpdate();
            });
        }


        static template = xml`<div>
        <div>
            <div>

            <form method="post"> 
                <div class='container'>
                    <div class='form-group'>
                        <label>Name</label>
                        <input type='text' name='name' t-model="state.name" class='form-control'/>
                    </div>
                    <div class='form-group'>
                        <label>Company</label>
                        <input type='text' name='companyname' t-model="state.companyname" class='form-control'/>
                    </div>
                    <div class='form-group'>
                        <label>Password</label>
                        <input type='password' name='password' t-model="state.password" class='form-control'/>
                    </div>
                    <div class='form-group'>
                        <label>Email</label>
                        <input type='text' name='email' t-model="state.email" class='form-control'/>
                    </div>
                    <center><a t-on-click="_onClickLink" class="btn btn-primary">Submit</a></center>
                </div>
            </form>

            </div>
        </div>
        </div>
        `;

        static components = {createuser};
    }

    function setup() {
        const CreateUserInstance = new CreateUser();
        CreateUserInstance.mount($('.create_user')[0]);
    }

    whenReady(setup);

    return CreateUser;
});
