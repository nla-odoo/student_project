odoo.define('loading_transportation_system.vehicle', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.create_vehicle').length) {
        return Promise.reject("DOM doesn't contain '.create_vehicle'");
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

        async modelFunction(ev) {
            const instance = new CreateVehicle(null);
            instance.mount($('.vehicle_create')[0]);
            this.destroy();
        }

        
        static template = xml`<div>
        <center><h1>Vehicles</h1></center>
        <a role="button" href="#" t-on-click="modelFunction()">Create</a>
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
    };

    class CreateVehicle extends Component {
        constructor() {
            super(...arguments);
            this.state = useState({
                description: "",
                name:"",
            });
        }

        async _onClickLink(ev) {
            const self = this;
            rpc.query({ route: "/vehicle/form",
                params:{name: this.state.name,
                description: this.state.description
            }}).then(function (result) {
                self.render(true);
                self.env.qweb.forceUpdate();
            });
        }

        async modelFunction(ev){
            const instance = new VehiclesDisplay(null);
            instance.mount($('.vehicle_create')[0]);
            this.destroy();
        }



        static template = xml`<div>
        <div>
            <div>
                <form method="post">
                    <center><h1>Create Vehicle</h1></center>
                    <div class="form-group">
                        <label>Name</label>
                        <input type="text" name='name' t-model="state.name" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>Description</label>
                        <input type="text" name='description' t-model="state.description" class="form-control"/>
                    </div>
                <a t-on-click="_onClickLink" class="btn btn-primary">Submit</a>
                </form>
            </div>
        </div>
        </div>
        `;

        static components = {vehicle};
    }

    function setup() {
        const CreateVehicleInstance = new CreateVehicle();
        CreateVehicleInstance.mount($('.create_vehicle')[0]);
    }

    whenReady(setup);

    return CreateVehicle;

    // function setup() {
    //     const VehiclesInstance = new VehiclesDisplay();
    //     VehiclesInstance.mount($('.vehicle_temp')[0]);
    // }

    // whenReady(setup);

    // return VehiclesDisplay;
});
