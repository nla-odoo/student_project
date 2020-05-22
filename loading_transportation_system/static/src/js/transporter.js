odoo.define('loading_transportation_system.transporter', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.transporter_temp').length) {
        return Promise.reject("DOM doesn't contain '.transporter_temp'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlTransporter extends Component {

        async willStart() {
            this.transporterdata = await this.getTransporters();
        }

        async getTransporters () {
            const transporter = await rpc.query({route: "/transporters"});
            return transporter;
        }
        get transporter ()  {
            return this.transporterdata;
        }

        
        static template = xml`<div>
        <center><h1>Transporters</h1></center>
        <table class="table table-stripded">
        <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
        </tr>
        <tr t-foreach="transporter" t-as="t">
        <td><t t-esc="t.name"/></td>
        <td><t t-esc="t.email"/></td>
        <td><t t-esc="t.phone"/></td>
        </tr>
        </table>
        </div>`
    }

    function setup() {
        const OwlTransporterInstance = new OwlTransporter();
        OwlTransporterInstance.mount($('.transporter_temp')[0]);
    }

    whenReady(setup);

    return OwlLeads;
});
