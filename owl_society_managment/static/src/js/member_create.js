odoo.define('owl_society_managment.member_create', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_member_create_component').length) {
        return Promise.reject("DOM doesn't contain '.my_member_create_component'");
    }
    const rpc = require('web.rpc');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlMemberCreate extends Component {
        constructor() {
        super(...arguments);
        this.state = useState({
            name: "",
            email:"",
        });
    }
        async willStart() {
            this.member = await this.getMember();
        }

        async getMember () {
            return this.members;
        }
        get members ()  {
            debugger
            return this.member;
        }
        
        async _onClickLink(ev) {
            debugger        
            this.member = await rpc.query({ route: "/member/form", 
                params:{name: this.state.name,
                    email: this.state.email,
                }});
            this.render(true);
          
        }


        static template = xml`<div>
        <div>
            <div>
                <form method="post">
                    <div>
                        <label>Member name</label>
                        <input type="text" name='name' t-model="state.name"/>
                    </div>
                    <div>
                        <label>Email</label>
                        <input type="email" name='name' t-model="state.email"/>
                    </div>
                <a t-on-click="_onClickLink">Submit</a>
                </form>
            </div>
        </div>
        </div>
        `;
    }

    function setup() {
        const OwlMemberCreateInstance = new OwlMemberCreate();
        OwlMemberCreateInstance.mount($('.my_member_create_component')[0]);
    }

    whenReady(setup);

    return OwlMemberCreate;
});