odoo.define('loading_transportation_system.vehicle', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.vehicle_temp').length) {
        return Promise.reject("DOM doesn't contain '.vehicle_temp'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class VehiclesDisplay extends Component {

        async willStart() {
            this.vehicledata = await this.getVehicle();
        }

        async getVehicle () {
            const vehicles = await rpc.query({route: "/vehicle"});
            return vehicles;
        }
        get vehicles ()  {
            return this.vehicledata;
        }

        
        static template = xml`<div>
        <center><h1>Vehicles</h1></center>
        <table class="table table-stripded">
        <tr>
            <th>Name</th>
            <th>Description</th>
        </tr>
        <tr t-foreach="vehicles" t-as="v">
        <td><t t-esc="v.name"/></td>
        <td><t t-esc="v.description"/></td>
        </tr>
        </table>
        </div>`
    }

    function setup() {
        const VehiclesInstance = new VehiclesDisplay();
        VehiclesInstance.mount($('.vehicle_temp')[0]);
    }

    whenReady(setup);

    return VehiclesDisplay;
});
