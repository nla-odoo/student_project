odoo.define('OWL_AHM.regsitration', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_registration_component').length) {
        return Promise.reject("DOM doesn't contain '.my_registration_component'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlRegistration extends Component {

        offset = 1;
        limit = 6
        count = [];
        order = {
            "name": "name",
            "name_desc": "name desc",
            "email": "email",
            "passwd": "passwd"
        }
         async onClick(ev) {
            debugger;
            const form = document.querySelector('#regsitration');
            let params = new FormData(myform);
            params = Object.fromEntries(params);
            await rpc.query({
                route: "/register",
                params: params
            }).then(function (result) {
                alert(' :) ')
            });
        }

         static template = xml`<div>
        <h3 align="center">Regsitration</h3>
        <form class="form" id="regsitration" name="myform">
            <div class="form-group col-6">
                <label>Name</label>
                <input type="text" name="name" class="form-control"/>
            </div>
            <div class="form-group col-6">
                <label>Email </label>
                <input type="email" name="phone" class="form-control"/>
            </div>
            <div class="form-group col-6">
                <label>Password</label>
                <input type="password" name="passwd" class="form-control"/>
            </div>
            <input t-on-click="onClick" class="btn btn-primary" type="button" name="onclick" value="Submit"/>
        </form>
         </div>`;
    }
    function setup() {
        const OwlFeedbackInstance = new OwlRegistration();
        OwlFeedbackInstance.mount($('.my_registration_component')[0]);
    }

    whenReady(setup);
    return OwlRegistration;
});