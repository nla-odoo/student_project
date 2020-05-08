odoo.define('OWL_DEMO.owl_component', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_complain_component').length) {
        return Promise.reject("DOM doesn't contain '.my_complain_component'");
    }

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlComplain extends Component {
         static template = xml`<div>
         <h3>Complain</h3>
         </div>`;
    }

    function setup() {
        const OwlComplainInstance = new OwlComplain();
        OwlComplainInstance.mount($('.my_complain_component')[0]);
    }

    whenReady(setup);

    return OwlComplain;
});