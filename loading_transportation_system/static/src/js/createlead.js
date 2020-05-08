odoo.define('loading_transportation_system.createlead', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.create_lead').length) {
        return Promise.reject("DOM doesn't contain '.create_lead'");
    }

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlCreateLead extends Component {


        static template = xml`<div>
        <div>
            <div>
                <center><h1>Create_Inquirey</h1></center>
                <form method="post" t-attf-action="/lead/form/">
                    <div class="form-group">
                        <label>Description</label>
                        <input type="text" name='description' class='form-control'/>
                    </div>
                    <div class="form-group">
                        <label>Partner_Id</label>
                        <input type="text" name='partner_id' class='form-control'/>
                    </div>
                    <div class="form-group">
                        <label>Name</label>
                        <input type="text" name='name' class='form-control'/>
                    </div>
                <button type="submit" class="btn btn-primary">Create</button>
                </form>
            </div>
        </div>
        </div>
        `;
    }

    function setup() {
        const OwlCreateLeadInstance = new OwlCreateLead();
        OwlCreateLeadInstance.mount($('.create_lead')[0]);
    }

    whenReady(setup);

    return OwlCreateLead;
});