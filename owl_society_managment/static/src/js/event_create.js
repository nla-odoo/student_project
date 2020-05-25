odoo.define('owl_society_managment.event_create', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_event_create_component').length) {
        return Promise.reject("DOM doesn't contain '.my_event_create_component'");
    }
    const rpc = require('web.rpc');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlEventCreate extends Component {
        constructor() {
        super(...arguments);
        this.state = useState({
            name: "",
            note:"",
            date_begin:"",
            date_end:"",
        });
    }
        async willStart() {
            this.event = await this.getEvent();
        }

        async getEvent () {
            return this.events;
        }
        get events ()  {
            debugger
            return this.event;
        }
        
        async _onClickLink(ev) {
            debugger        
            this.event = await rpc.query({ route: "/event/form", 
                params:{name: this.state.name,
                    note: this.state.note,
                    date_begin: this.state.date_begin,
                    date_end: this.state.date_end,
                }});
            this.render(true);
          
        }


        static template = xml`<div>
        <div>
            <div>
                <form method="post">
                    <div>
                        <label>Event name</label>
                        <input type="text" name='name' t-model="state.name"/>
                    </div>
                    <div>
                        <label>Note</label>
                        <textarea rows="4" cols="50" name='note' t-model="state.note"/>
                    </div>
                    <div>
                        <label>Start Date</label>
                        <input type="date" name="date_begin" t-model="state.date_begin"/>
                    </div>
                    <div>
                        <label>End Date</label>
                        <input type="date" name="date_end" t-model="state.date_end"/>
                    </div>
                <a t-on-click="_onClickLink">Submit</a>
                </form>
            </div>
        </div>
        </div>
        `;
    }

    function setup() {
        const OwlEventCreateInstance = new OwlEventCreate();
        OwlEventCreateInstance.mount($('.my_event_create_component')[0]);
    }

    whenReady(setup);

    return OwlEventCreate;
});