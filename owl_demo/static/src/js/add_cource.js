odoo.define('owldemo.my_addCource_com', function(require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_addCource_com').length) {
        return Promise.reject("DOM doesn't contain '.my_dynamic_component'");
    }

    const rpc = require('web.rpc');
    //this is problem
    // const Menu = require('owl_demo.menucom');
    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;


    // if (!$('.my_AddStudent_com').length) {
    //     return Promise.reject("DOM doesn't contain '.my_dynamic_component'");
    // }

    // const rpc = require('web.rpc');

    // const { Component, hooks } = owl;
    // const { xml } = owl.tags;
    // const { whenReady } = owl.utils;

//     class owlAddStudent extends Component {

//         async willStart(){
//             console.log('me login')
//             this.student = await rpc.query({route: '/demo_AddStudent'});
//             debugger; 

//         }

//          async _onClickLink(ev) {
//             debugger
//             const form = document.querySelector('#addstudent');
//             let formData = new FormData(form);
//             formData = Object.fromEntries(formData);

//            this.student = await rpc.query({
//                 route: "/demo_AddStudent", 
//                 params: {'form_data': formData}
//             });
//         }



//         static template = xml` 
//             <div>
//               <div>
//                 <h1 class='h1'><span class='styling'>Add</span>Student</h1>
//                   <form class="form" id="addstudent">
//                     <label class='label'>
//                         <p class="label-txt">ENTER STUDENT EMAIL</p>
//                         <input type="text" name="email" class="input"/>
//                             <div class="line-box">
//                                 <div class="line"></div>
//                             </div>
//                     </label>
//                     <label class='label'>
//                         <p class="label-txt">ENTER STUDENT NAME</p>
//                         <input type="text" name="name" class="input"/>
//                             <div class="line-box">
//                                 <div class="line"></div>
//                             </div>
//                     </label>
//                     <label class='label'>
//                         <p class="label-txt">ENTER STUDENT NUMBER</p>
//                         <input type="text" name="password" class="input"/>
//                             <div class="line-box">
//                                 <div class="line"></div>
//                             </div>
//                     </label>
//                     <label class='label'>
//                         <p class="label-txt">ENTER STUDENT PASSWORD</p>
//                         <input type="text" name="password" class="input"/>
//                             <div class="line-box">
//                                 <div class="line"></div>
//                             </div>
//                     </label>
//                     <div id="currncy_id">
//                         <select name="currency_id" class="form-control currency_id">
//                             <t t-foreach="student.resulrt" t-as="course"  t-key="'row_' + row_index">
//                                 <option t-att-value="student.id">
//                                     <t t-esc="course.name"/>
//                                 </option>
//                             </t>
//                         </select>
//                     </div><p></p>
//                           <button t-on-click="_onClickLink" class="button" type="button">submit</button>
//                   </form>
//                 </div>
//             </div>  
// `;   }

//     function setup1() {
//         const OwladdstudentInstance = new owlAddStudent();
//         OwladdstudentInstance.mount($('.my_AddStudent_com')[0]);
//     }

//     whenReady(setup1);

    // return owlAddStudent;



    

   class Menu extends Component {

        isStudent = false;

         async willStart() {
            console.log('menu me')
            this.isStudent= await rpc.query({ route: '/is_student' });
            debugger;

        }
       _onClickLink(ev) {
                debugger
            ev.preventDefault();
            if(ev.target.pathname==='/demo_AddStudent')
            {
                const owladdcourceInstance = new owlAddCource();
                owladdcourceInstance.mount($('.my_addCource_com')[0]);
            }
             if(ev.target.pathname==='/demo_AddCource')
            {
                const owladdcourceInstance = new owlAddCource();
                owladdcourceInstance.mount($('.my_addCource_com')[0]);
            }
            
        }

        constructor(){
            super(...arguments)
            // this.Regist = await rpc.query({ route: '/' });
        }

        static template = xml`

            <div class="topnav" id="myTopnav">
                <t t-if='!isStudent'>
                <a href="#" class="fa fa-shopping-cart" > <t t-esc="count"/></a>
                <a t-on-click="_onClickLink" href="/demo_AddCource">addcource</a>
                <br/>
                <a t-on-click="_onClickLink" href="/demo_AddStudent">addstudnt</a>
                <a href="#">ragister</a>
                <br/>
                <a href="#">Home</a>
                <br/>
                </t>
                <t t-else=''>
                <a href="#">pymeny</a>
                <br/>
                <a href="#">pyment details</a>
                <br/>
                
                </t>
            </div>`;
    }
    class owlAddCource extends Component {



        async willStart() {
            console.log('hhhhhhhhhhhhhhhh')
            this.Regist = await rpc.query({ route: '/demo_AddCource' });
            debugger;

        }

        async _onClickLink(ev) {
            debugger
            const form = document.querySelector('#addcource');
            let formData = new FormData(form);
            formData = Object.fromEntries(formData);

           this.product = await rpc.query({
                route: "/demo_AddCource", 
                params: {'form_data': formData}
            });
        }
       
        static template = xml `
        

        <div>

        <Menu></Menu>
            <h1 class='h1'><span class='styling'>ADD</span>COURSE</h1>
        <form class="form" id="addcource">
            <label class='label'>
            <p class="label-txt">ENTER YOUR COURSE NAME</p>
                <input type="text" name="name" class="input"/>
            <div class="line-box">
                <div class="line"></div>
            </div>
            </label>
            <label class='label'>
                <p class="label-txt">ENTER YOUR FEES</p>
                <input type="text" name="list_price" class="input"/>
            <div class="line-box">
                <div class="line"></div>
            </div>
            </label>
            <button t-on-click="_onClickLink" class="button" type="button">submit</button>
        </form>
        </div>
`;
     static components = {Menu};
    }

    function setup() {
        const owladdcourceInstance = new owlAddCource();
        owladdcourceInstance.mount($('.my_addCource_com')[0]);
    }

    whenReady(setup);

    return owlAddCource;
});