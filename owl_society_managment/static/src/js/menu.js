debugger
odoo.define('owl_society_managment.menu', function (require) {
    "use strict";
    console.log('menu')
    require('web.dom_ready');
    if (!$('.menu_item').length) {
        return Promise.reject("DOM doesn't contain '.menu_item'");
    }

    const rpc = require('web.rpc');
    const session = require('web.session');
    const member = require('owl_society_managment.member_create');
    const members = require('owl_society_managment.member_create');
    const event = require('owl_society_managment.event_create');
    const complaint = require('owl_society_managment.complaint_create');
    const balance = require('owl_society_managment.balance_create');
    const jounral = require('owl_society_managment.jounral_create');
    const dashboard = require('owl_society_managment.orders_detail');
    const account = require('owl_society_managment.account_create');
    const service = require('owl_society_managment.owl_dynamic_component');
    const history = require('owl_society_managment.account_payment');
    const sheet = require('owl_society_managment.account');
    const { Component } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;
    // const Test = require('owl_society_managment.event_create');

    class Menu extends Component {
        // ev.console.log('menu');

        // _homePage(ev) {
        //     ev.preventDefault();
        //     if (ev.target.dataset.mode == 'addEvent') {
        //         const cartInstance = new PortalHomePage();
        //         cartInstance.mount($('.my_event_create_component')[0]);
        //         this.destroy();
        //     } else if (ev.target.dataset.mode == 'services_page') {
        //         const cartInstance = new PortalPrintServicesCardView();
        //         cartInstance.mount($('.portal_user_print_services_card_views')[0]);
        //         this.destroy();
        //     } else {
        //         this.render(true);
        //     }
        // }

        async willStart() {
            this.event = await this.getEvent();
            const dashboardInstance = new dashboard();
            dashboardInstance.mount($('.component_view')[0]);
        }

        async getEvent () {
            const events = await rpc.query({ route : "/get_event_data"})
            return events;
        }
        get events ()  {
            debugger
            return this.event;
        }

         _renderMenuItem(mode) {
                if (mode === 'addMembers') {
                    const eventInstance = new members();
                    eventInstance.mount($('.component_view')[0]);
                } 
                else if (mode === 'addEvent') {
                    const eventInstance = new event();
                    eventInstance.mount($('.component_view')[0]);
                } else if (mode === 'addComplaint') {
                    const complaintInstance = new complaint();
                    complaintInstance.mount($('.component_view')[0]);
                } else if (mode === 'addBalance') {
                    const balanceInstance = new balance();
                    balanceInstance.mount($('.component_view')[0]);
                } else if (mode === 'addAccount') {
                    const accountInstance = new account();
                    accountInstance.mount($('.component_view')[0]);
                } else if (mode === 'addJounral') {
                    const jounralInstance = new jounral();
                    jounralInstance.mount($('.component_view')[0]);
                }  else if (mode === 'addService') {
                    const serviceInstance = new service();
                    serviceInstance.mount($('.component_view')[0]);
                }  else if (mode === 'addDashboard') {
                    const dashboardInstance = new dashboard();
                    dashboardInstance.mount($('.component_view')[0]);
                }  else if (mode === 'history') {
                    const accountInstance = new history();
                    accountInstance.mount($('.component_view')[0]);
                } else if (mode === 'sheet') {
                    const sheetInstance = new sheet();
                    sheetInstance.mount($('.component_view')[0]);
                }  
                
            }
        

        // get register () {
        //     return this.toRegsiter;
        // }

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
                            <a class="nav-link" href="#" data-mode="addMembers">Members</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#" data-mode="addEvent">Event</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#" data-mode="addComplaint">Complaint</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active" href="#" data-mode="addDashboard">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#" data-mode="history">Payments History</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#" data-mode="addBalance">Balance</a>
                        </li>
                        <t t-if="events[1] == 'secretary' || events[1] == 'treasurer'">
                            <li class="nav-item">
                                <a class="nav-link" href="#" data-mode="addService">Service</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="#" data-mode="sheet">Balance Sheet</a>
                            </li>
                        </t>
                    </ul>
                </div>
            </nav>
        `;
    }
    function setup() {
        const MenuInstance = new Menu();
        $('.o_portal.container').html('');
        MenuInstance.mount($('.o_portal.container')[0]);
    }

    whenReady(setup);

    return Menu;
});
