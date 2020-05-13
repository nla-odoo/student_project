odoo.define('OWL_DEMO.owl_component', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_component').length) {
        return Promise.reject("DOM doesn't contain '.my_component'");
    }

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlDemo extends Component {
         static template = xml`<div>
         <div>
            Name: <input type="text" id="fname" name="fname"/><br/>
            Email: <input type="text" id="fname" name="fname"/><br/>
            Feedback: <input type="text" id="fname" name="fname"/><br/>
            <input type="submit" name="Submit"/>
            </div>
         </div>`;
    }

    function setup() {
        const OwlDemoInstance = new OwlDemo();
        OwlDemoInstance.mount($('.my_component')[0]);
    }

    whenReady(setup);

    return OwlDemo;
});