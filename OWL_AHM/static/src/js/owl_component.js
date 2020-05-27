odoo.define('OWL_AHM.owl_component', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_feedback_component').length) {
        return Promise.reject("DOM doesn't contain '.my_feedback_component'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlFeedback extends Component {

         async onClick(ev) {
            const form = document.querySelector('#addfeedback');
            let params = new FormData(form);
            params = Object.fromEntries(params);
            await rpc.query({
                route: "/add_feedback",
                params: params
            }).then(function (result) {
                alert('Thank You for Feedback :).')
            });
        }

         static template = xml`<div>
        <h3 align="center">Feedback</h3>
        <form class="form" id="addfeedback">
            <div class="form-group col-6">
                <label>Name</label>
                <input type="text" name="name" class="form-control"/>
            </div>
            <div class="form-group col-6">
                <label>Mobile No. </label>
                <input type="text" name="phone" class="form-control"/>
            </div>
            <div class="form-group col-6">
                <label>Give Your Feedback</label>
                <input type="text" name="feedback" class="form-control"/>
            </div>
            <input t-on-click="onClick" class="btn btn-primary" type="button" name="onclick" value="Submit"/>
        </form>
         </div>`;
    }
    function setup() {
        const OwlFeedbackInstance = new OwlFeedback();
        OwlFeedbackInstance.mount($('.my_feedback_component')[0]);
    }

    whenReady(setup);
    return OwlFeedback;
});