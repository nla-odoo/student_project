odoo.define('loading_transportation_system.menu2', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.menu2_temp').length) {
        return Promise.reject("DOM doesn't contain '.menu2_temp'");
    }

    const rpc = require('web.rpc');
    const session = require('web.session');
    // const customer_regi = require('loading_transportation_system.customer_regi');
    const userDeta = require('loading_transportation_system.user');
    const createleaddata = require('loading_transportation_system.createlead');
    const leaddata = require('loading_transportation_system.lead');
    const driverdata = require('loading_transportation_system.driver');
    // const createdriverdata = require('loading_transportation_system.createdriver')
    // const createvehicledata = require('loading_transportation_system.createvehicle');
    const vehicledata = require('loading_transportation_system.cust_vehicle');
    const transporterdata = require('loading_transportation_system.transporter');

    const { Component, hooks } = owl;
    const { useState } = owl.hooks;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;


    class Menu2 extends Component {

     async willStart() {
            this.toRegsiter = !session.user_id;
            // this.isCustomer= await rpc.query({ route: '/is_Customer' });
            
            this._renderMenuItem();
        }
         _renderMenuItem(mode) {
           
                if (mode === 'users') {
                    const tRegisterInstance = new userDeta();
                    tRegisterInstance.mount($('.component_view')[0]);
                } 

                // if (mode === 'customer') {
                //     const cRegisterInstance = new customer_regi();
                //     cRegisterInstance.mount($('.component_view')[0]);
                // } 

                if (mode === 'createleads') {
                    const lInstance = new createleaddata();
                    lInstance.mount($('.component_view')[0]);
                }

                if (mode === 'leads') {
                    const llInstance = new leaddata();
                    llInstance.mount($('.component_view')[0]);
                }

                if (mode === 'drivers') {
                    const dInstance = new driverdata();
                    dInstance.mount($('.component_view')[0]);
                }

                if (mode === 'vehicles') {
                    const dInstance = new vehicledata();
                    dInstance.mount($('.component_view')[0]);
                }

                if (mode === 'transporters') {
                    const tInstance = new transporterdata();
                    tInstance.mount($('.component_view')[0]);
                }

                // if (mode === 'createdrivers') {
                //     const dInstance = new createdriverdata();
                //     dInstance.mount($('.component_view')[0]);
                // }

                // if (mode === 'createvehicles') {
                //     const cInstance = new createvehicledata();
                //     cInstance.mount($('.component_view')[0]);
                // }



            }
             _onClickMenuItem(ev) {
            ev.preventDefault();
            const mode = ev.target.dataset.mode;
            $('.component_view').html('');
            this._renderMenuItem(mode);
            this.el.querySelector('.active').classList.remove('active');
            this.el.querySelector('a[data-mode="' + mode + '"]').classList.add('active')
        }

       

        
        static template = xml`
 <nav class="navbar navbar-expand-lg navbar-light bg-light">
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav" t-on-click="_onClickMenuItem">
                       
                            <li class="nav-item">
                                <a class="nav-link active" href="#" data-mode="users">Profile</a>
                            </li>


                            <li class="nav-item">
                                <a class="nav-link" href="#" data-mode="leads">My_leads</a>
                            </li>

                            <li class="nav-item">
                                <a class="nav-link" href="#" data-mode="createleads">CreateLeads</a>
                            </li>

                            <li class="nav-item">
                                <a class="nav-link" href="#" data-mode="drivers">Driver</a>
                            </li>


                        <li class="nav-item">
                                <a class="nav-link" href="#" data-mode="vehicles"> Vehicles</a>
                            </li>

                            <li class="nav-item">
                                <a class="nav-link" href="#" data-mode="transporters"> Transporters</a>
                            </li>
                       
                       
                       
                    </ul>
                </div>
            </nav>
        `
    };

    function setup() {
        const Menu2Instance = new Menu2();
        Menu2Instance.mount($('.menu2_temp')[0]);
    }

    whenReady(setup);

    return Menu2;

    
});
