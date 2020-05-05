odoo.define('loading_transportation_system.owl_component', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_component').length) {
        return Promise.reject("DOM doesn't contain '.my_component'");
    }

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlDemo extends Component {
         static template = xml`<div>todo app</div>`;
    }

    function setup() {
        const OwlDemoInstance = new OwlDemo();
        OwlDemoInstance.mount($('.my_component')[0]);
    }

    whenReady(setup);

    return OwlDemo;
});
