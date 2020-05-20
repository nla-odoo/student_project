     
// odoo.define('owl_demo.menucom', function (require) {
//     "use strict";

//     const { Component } = owl;
//     const { xml } = owl.tags;
//     // this is problem
//     const addcource = require('owl_demo.my_addCource_com');
//     const rpc = require('web.rpc');

//    class Menu extends Component {

//         isStudent = false;

//          async willStart() {
//             console.log('menu me')
//             this.isStudent= await rpc.query({ route: '/is_student' });
//             debugger;

//         }
//          _onClickLink(ev) {
//             //     debugger
//             // ev.preventDefault();
//             // if(ev.target.pathname==='/demo_AddStudent')
//             // {
//             //     const owladdcourceInstance = new owlAddCource();
//             //     owladdcourceInstance.mount($('.my_addCource_com')[0]);
//             // }
//             //  if(ev.target.pathname==='/demo_AddCource')
//             // {
//             //     const owladdcourceInstance = new owlAddCource();
//             //     owladdcourceInstance.mount($('.my_addCource_com')[0]);
//             // }
            
//         }

//         // constructor(){
//         //     super(...arguments)
//         //     addcource.components = {Menu};
//         //     // this.Regist = await rpc.query({ route: '/' });
//         // }

//         static template = xml`

//             <div class="topnav" id="myTopnav">
//                 <t t-if='!isStudent'>
//                 <a href="#" class="fa fa-shopping-cart" > <t t-esc="count"/></a>
//                 <a t-on-click="_onClickLink" href="/demo_AddCource">addcource</a>
//                 <br/>
//                 <a t-on-click="_onClickLink" href="/demo_AddStudent">addstudnt</a>
//                 <a href="#">ragister</a>
//                 <br/>
//                 <a href="#">Home</a>
//                 <br/>
//                 </t>
//                 <t t-else=''>
//                 <a href="#">pymeny</a>
//                 <br/>
//                 <a href="#">pyment details</a>
//                 <br/>
                
//                 </t>
//             </div>`;
//     }

//     return Menu;
// });
