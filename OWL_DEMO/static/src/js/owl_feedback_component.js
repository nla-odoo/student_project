odoo.define('OWL_DEMO.owl_component', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_feedback_component').length) {
        return Promise.reject("DOM doesn't contain '.my_feedback_component'");
    }

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlFeedback extends Component {
         static template = xml`<div>
         <h3>Feedback</h3>
         </div>`;
    }

    function setup() {
        const OwlFeedbackInstance = new OwlFeedback();
        OwlFeedbackInstance.mount($('.my_feedback_component')[0]);
    }

    whenReady(setup);

    return OwlFeedback;
});