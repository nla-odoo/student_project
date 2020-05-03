odoo.define('owl_work.btn_component', function(require){
    "use strict";

    require('web.dom_ready');

    const { Component, useState, hooks } = owl;
    const { xml } = owl.tags;

    const btn_temp = xml`
        <button t-on-click="state.value">
        Help Chat Board
        </button>`;

    class OwlWork extends Component{
        state = useState({ value: "Helllooooo"})
    }
    OwlWork.template = btn_temp;

    const workInstance = new OwlWork();
    workInstance.mount(document.body);
});