odoo.define('owl_society_managment.member_create', function (require) {
    "use strict";

    // require('web.dom_ready');
    // if (!$('.my_member_create_component').length) {
    //     return Promise.reject("DOM doesn't contain '.my_member_create_component'");
    // }
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
            member_type:"",
            street2:"",
        });
    }

        async willStart() {
            this.member = await this.getMember();
        }

        async getMember () {
            const members = await rpc.query({ route: "/get_member_data"})
            return members;
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
                    member_type: this.state.member_type,
                    street2: this.state.street2,
                }});
            this.render(true);
          
        }

        async _onClickDelete(ev) {
            debugger
            let partner_id = ev.currentTarget.getAttribute('members_id');
            return rpc.query({route: "/member/unlink", params: {'partner_id' : partner_id}})
        }


        static template = xml`<div>
        <div class="container py-5">
            <t t-if="members[1] == 'secretary'">
            <div class="card-body">
                <form method="post">
                    <div class="form-group">
                        <label>Member name</label>
                        <input type="text" name='name' t-model="state.name" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" name='name' t-model="state.email" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>House Number</label>
                        <input type="text" name='street2' t-model="state.street2" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>Type</label>                
                        <select id="member_type" name="member_type" t-model="state.member_type" class="form-control">
                            <option value="treasurer">Treasurer</option>
                            <option value="member">Member</option>
                        </select>
                    </div>
                <a  class="btn btn-primary" t-on-click="_onClickLink">Submit</a>
                </form>
            </div>
            </t>
            <div class="container py-5">
                <div class="card border-0 mx-auto bg-100 rounded-0 shadow-sm bg-white o_database_list w-100 p-3">       
                   <div class="card-body">
                        <table class="table">
                            <thead>
                                <tr>
                                  <th scope="col">Name</th>
                                  <th scope="col">Email</th>
                                  <th scope="col">Member Type</th>
                                  <t t-if="members[1] == 'secretary'">
                                  <th scope="col">Action</th>
                                  </t>
                                </tr>
                            </thead>  
                            <t t-foreach="members[0]" t-as="member">
                                <tr>
                                    <td><t t-esc="member.name"/></td>
                                    <td><t t-esc="member.email"/></td>
                                    <td><t t-esc="member.member_type"/></td>
                          
                                    <button type="button" class="btn btn-danger" t-att-members_id='members.id' t-on-click="_onClickDelete">Delete</button>
                                    </tr>
                                </t>
                                
                        </table>
                   </div>
                </div>
            </div>
        </div>
        </div>
        `;
    }

    // function setup() {
    //     const OwlMemberCreateInstance = new OwlMemberCreate();
    //     OwlMemberCreateInstance.mount($('.my_member_create_component')[0]);
    // }

    // whenReady(setup);

    return OwlMemberCreate;
});





















// odoo.define('owl_society_managment.member_create', function (require) {
//     "use strict";

//     // require('web.dom_ready');
//     // if (!$('.my_member_create_component').length) {
//     //     return Promise.reject("DOM doesn't contain '.my_member_create_component'");
//     // }
//     const rpc = require('web.rpc');
//     // const OwlEventCreate = require('owl_society_managment.event_create');
//     // const Menu = require('owl_society_managment.menu');
//     const { Component, hooks, useState } = owl;
//     const { xml } = owl.tags;
//     const { whenReady } = owl.utils;

//     class OwlMemberCreate extends Component {
//         constructor() {
//         super(...arguments);
//         this.state = useState({
//             name: "",
//             email:"",
//             member_type:"",
//         });
//     }
        
//         async willStart() {
//             this.member = await this.getMember();
//         }

//         async getMember () {
//             const members = await rpc.query({ route: "/get_member_data"})
//             return members;
//         }
//         get members ()  {
//             debugger
//             return this.member;
//         }
        
//         async _onClickLink(ev) {
//             debugger        
//             this.member = await rpc.query({ route: "/member/form", 
//                 params:{name: this.state.name,
//                     email: this.state.email,
//                     member_type: this.state.member_type,
//                 }});
//             this.render(true);
          
//         }

//         // _addEvent (ev) {
//         //     const OwlEventCreateInstance = new OwlEventCreate();
//         //     OwlEventCreateInstance.mount($('.component_view')[0]);
//         //     this.destroy();
//         // }
//         // <a href="#" t-on-click="_addEvent" class="btn btn-primary">Add Event</a>
//         //    <menu/>

//         static template = xml`<div>
//         <div>
//             <t t-if="members[1] == 'secretary'">
//             <div>
//                 <form method="post">
//                     <div>
//                         <label>Member name</label>
//                         <input type="text" name='name' t-model="state.name"/>
//                     </div>
//                     <div>
//                         <label>Email</label>
//                         <input type="email" name='name' t-model="state.email"/>
//                     </div>
//                     <div>
//                         <label>Type</label>
//                     </div>
//                     <div>                 
//                         <select id="member_type" name="member_type" t-model="state.member_type">
//                             <option value="treasurer">Treasurer</option>
//                             <option value="member">Member</option>
//                         </select>
//                     </div>
//                 <a class="btn btn-primary" t-on-click="_onClickLink">Submit</a>
//                 </form>
//             </div>
//             </t>
//             <div class="container py-5">
//                 <div class="card border-0 mx-auto bg-100 rounded-0 shadow-sm bg-white o_database_list w-50 p-3">       
//                    <div class="card-body">
//                         <table class="table">
//                             <thead>
//                                 <tr>
//                                   <th scope="col">Name</th>
//                                   <th scope="col">Email</th>
//                                   <th scope="col">Member Type</th>
//                                 </tr>
//                             </thead>  
//                             <t t-foreach="members" t-as="member">
//                                 <tr>
//                                     <td><t t-esc="member.name"/></td>
//                                     <td><t t-esc="member.email"/></td>
//                                     <td><t t-esc="member.member_type"/></td>
//                                 </tr>
//                             </t>
//                         </table>
//                    </div>
//                 </div>
//             </div>
//         </div>
//         </div>
//         `;
//         // static components = {Menu};
//     }

//     // function setup() {
//     //     const OwlMemberCreateInstance = new OwlMemberCreate();
//     //     OwlMemberCreateInstance.mount($('.my_member_create_component')[0]);
//     // }

//     // whenReady(setup);


//     return OwlMemberCreate;
// });

































































// // odoo.define('owl_society_managment.member_create', function (require) {
// //     "use strict";

// //     require('web.dom_ready');
// //     if (!$('.my_member_create_component').length) {
// //         return Promise.reject("DOM doesn't contain '.my_member_create_component'");
// //     }
// //     const rpc = require('web.rpc');

// //     const { Component, hooks, useState } = owl;
// //     const { xml } = owl.tags;
// //     const { whenReady } = owl.utils;

// //     class OwlMemberCreate extends Component {
// //         constructor() {
// //         super(...arguments);
// //         this.state = useState({
// //             name: "",
// //             email:"",
// //             member_type:"",
// //         });
// //     }
// //         offset = 1;
// //         limit = 6
// //         count = [];

// //         async willStart() {
// //             debugger
// //             this.partnersdata = await rpc.query({ route: "/get_member_data", params:{ 
// //                 offset: this.offset, limit: this.limit}});
// //             // this.partnersdata = await this.getMember(this.offset);
// //             for (let index = 1; index <= parseInt(this.partnersdata.count); index++) {
// //                 this.count.push(index);
// //             }
// //             // this.member = await this.getMember();
// //         }

// //         async _onClickLink(ev) {
// //             ev.preventDefault();
// //             let offset = ev.currentTarget.getAttribute('offset');
// //             this.partnersdata = await this.getMember(offset);
// //             this.render(true);
// //         }

// //         async getMember () {
// //             const members = await rpc.query({ route: "/get_member_data"
// //             });
// //             return members;
// //         }
// //         get members ()  {
// //             debugger
// //             return this.member;
// //         }
        
// //         async _onClickMember(ev) {
// //             debugger        
// //             this.member = await rpc.query({ route: "/member/form", 
// //                 params:{name: this.state.name,
// //                     email: this.state.email,
// //                     member_type: this.state.member_type,
// //                 }});
// //             this.render(true);
          
// //         }


// //         static template = xml`<div>
// //         <div>
            
// //             <div>
// //                 <form method="post">
// //                     <div>
// //                         <label>Member name</label>
// //                         <input type="text" name='name' t-model="state.name"/>
// //                     </div>
// //                     <div>
// //                         <label>Email</label>
// //                         <input type="email" name='name' t-model="state.email"/>
// //                     </div>
// //                     <div>
// //                         <label>Type</label>
// //                     </div>
// //                     <div>                 
// //                         <select id="member_type" name="member_type" t-model="state.member_type">
// //                             <option value="treasurer">Treasurer</option>
// //                             <option value="member">Member</option>
// //                         </select>
// //                     </div>
// //                 <a t-on-click="_onClickMember">Submit</a>
// //                 </form>
// //             </div>
            
// //             <div class="container py-5">
// //                 <div class="card border-0 mx-auto bg-100 rounded-0 shadow-sm bg-white o_database_list w-50 p-3">       
// //                    <div class="card-body">
// //                    <t t-as="member" t-foreach="partnersdata[2]">
// //                         <table class="table">
// //                             <thead>
// //                                 <tr>
// //                                   <th scope="col">Name</th>
// //                                   <th scope="col">Email</th>
// //                                   <th scope="col">Member Type</th>
// //                                 </tr>
// //                             </thead>  
                            
// //                                 <tr>
// //                                     <td><t t-esc="member.name"/></td>
// //                                     <td><t t-esc="member.email"/></td>
// //                                     <td><t t-esc="member.member_type"/></td>
// //                                 </tr>
                        
// //                         </table>
// //                         </t>
// //                    </div>
// //                    <div class="d-flex justify-content-center">
// //                         <nav aria-label="Page navigation example">
// //                             <ul class="pagination">
// //                                 <t t-set="offset" t-value="0"/>
// //                                 <t t-as="page" t-foreach="count">
// //                                     <li class="page-item">
// //                                         <a t-att-offset="offset" t-on-click="_onClickLink" class="page-link" href="#!"><span t-esc="page" /></a>
// //                                         <t t-set="offset" t-value="offset + 6"/>
// //                                     </li>
// //                                 </t>
// //                             </ul>
// //                         </nav>
// //                         </div>
// //                 </div>
// //             </div>
// //         </div>
// //         </div>
// //         `;
// //     }

// //     function setup() {
// //         const OwlMemberCreateInstance = new OwlMemberCreate();
// //         OwlMemberCreateInstance.mount($('.my_member_create_component')[0]);
// //     }

// //     whenReady(setup);

// //     return OwlMemberCreate;
// // });