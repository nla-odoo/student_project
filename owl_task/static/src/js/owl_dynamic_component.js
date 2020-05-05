odoo.define('owl_task.owl_dynamic_component', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_dynamic_component').length) {
        return Promise.reject("DOM doesn't contain '.my_dynamic_component'");
    }

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlDynamicDemo extends Component {


        static template = xml`<div>
        <div>
            <div>
                <form method="post" t-attf-action="/services/form/">
                    <div>
                        <label>Product name</label>
                        <input type="text" name='name'/>
                    </div>
                    <div>
                        <label>Purchase</label>
                        <input type="checkbox" name='purchase_ok'/>
                    </div>
                    <div>
                        <label>Sale</label>
                        <input type="checkbox" name='sale_ok'/>
                    </div>
                    <div>
                        <label>Type</label>
                        <select id="complaint_details" name="type">
                            <option value="consu">Consumable</option>
                            <option value="service">Service</option>
                        </select>
                    </div>
                    <div>
                        <label>Cost</label>
                        <input type="text" name='standard_price'/>
                    </div>
                    <div>
                        <label>Sale price</label>
                        <input type="text" name='list_price'/>
                    </div>
                <button type="submit">Submit</button>
                </form>
            </div>
        </div>
        </div>
        `;
    }

    function setup() {
        const OwlDynamicDemoInstance = new OwlDynamicDemo();
        OwlDynamicDemoInstance.mount($('.my_dynamic_component')[0]);
    }

    whenReady(setup);

    return OwlDynamicDemo;
});