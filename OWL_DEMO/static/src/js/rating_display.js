odoo.define('OWL_DEMO.rating_display', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_rating_component2').length) {
        return Promise.reject("DOM doesn't contain '.my_rating_component2'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlLeads extends Component {

        async willStart() {
            this.leadsdata = await this.getLeads();
        }

        async getLeads () {
            const leads = await rpc.query({route: "/feedback"});
            return leads;
        }
        get leads ()  {
            return this.leadsdata;
        }

        
        static template = xml`<div>
        <center><h1>Leads</h1></center>
        <table class="table table-stripded">
        <tr>
            <th>Rating_Text</th>
            <th>Feedback</th>
        </tr>
        <tr t-foreach="leads" t-as="lead">
        <td><t t-esc="lead.rating_text"/></td>
        <td><t t-esc="lead.feedback"/></td>
        </tr>
        </table>
        </div>`
    }

    function setup() {
        const OwlLeadsInstance = new OwlLeads();
        OwlLeadsInstance.mount($('.my_leads')[0]);
    }

    whenReady(setup);

    return OwlLeads;
});