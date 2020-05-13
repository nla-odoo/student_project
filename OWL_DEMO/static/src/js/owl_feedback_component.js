odoo.define('OWL_DEMO.owl_feedback_component', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_leads').length) {
        return Promise.reject("DOM doesn't contain '.my_leads'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlFeedback extends Component {

      async getLeads () {
            const leads = await rpc.query({route: "/inquirey"});
            return leads;
        }
        get leads ()  {
            return this.leadsdata;
        }

        
        static template = xml`<div>
        <center><h1>Leads</h1></center>
        <table class="table table-stripded">
        <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Partner ID</th>
            <th>Type</th>
        </tr>
        <tr t-foreach="leads" t-as="lead">
        <td><t t-esc="lead.name"/></td>
        <td><t t-esc="lead.description"/></td>
        <td><t t-esc="lead.partner_id"/></td>
        <td><t t-esc="lead.type"/></td>
        </tr>
        </table>
        </div>`
    }

    function setup() {
        const OwlFeedbackInstance = new OwlFeedback();
        OwlFeedbackInstance.mount($('.my_feedback_component')[0]);
    }

    whenReady(setup);

    return OwlFeedback;
});

