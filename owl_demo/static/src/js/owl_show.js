odoo.define('owl_demo.owl_show', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.owldetail_component').length) {
        return Promise.reject("DOM doesn't contain '.owldetail_component'");
    }

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlDemo extends Component {
         static template = xml`<div>todo app hello</div>`;
    }

    function setup() {
        const OwlDemoInstance = new OwlDemo();
        OwlDemoInstance.mount($('.owldetail_component')[0]);
    }

    whenReady(setup);

    return OwlDemo;
});