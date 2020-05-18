odoo.define('owl_demo.order_List', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.order_List').length) {
        return Promise.reject("DOM doesn't contain '.order_List'");
    }

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlDemo extends Component {
         static template = xml`<div>todo app hello</div>`;
    }

    function setup() {
        const OwlDemoInstance = new OwlDemo();
        OwlDemoInstance.mount($('.order_List')[0]);
    }

    whenReady(setup);

    return OwlDemo;
});
