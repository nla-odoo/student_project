odoo.define('owldemo.AddStudent', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_AddStudent_com').length) {
        return Promise.reject("DOM doesn't contain '.my_dynamic_component'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class owlAddStudent extends Component {

        async willStart(){
            console.log('me login')
            this.student = await rpc.query({route: '/demo_AddStudent'});
            debugger; 

        }

         async _onClickLink(ev) {
            debugger
            const form = document.querySelector('#addstudent');
            let formData = new FormData(form);
            formData = Object.fromEntries(formData);

           this.product = await rpc.query({
                route: "/demo_AddCource", 
                params: {'form_data': formData}
            });
        }

//        student_name
// course_id
// company_id
// enrolment_no
// mobile_number
// address
// institute_id
// res_user_id
// state
// order_ref
// acquirer_ref

        static template = xml` 
        <div>


         
<div>
       
           <h1 class='h1'><span class='styling'>Add</span>Student</h1>

               <form class="form" id="addstudent">
        

  <label class='label'>
    <p class="label-txt">ENTER STUDENT EMAIL</p>
    <input type="text" name="email" class="input"/>
    <div class="line-box">
      <div class="line"></div>
    </div>
  </label>
  <label class='label'>
    <p class="label-txt">ENTER STUDENT NAME</p>
    <input type="text" name="name" class="input"/>
    <div class="line-box">
      <div class="line"></div>
    </div>
  </label>
   <label class='label'>
    <p class="label-txt">ENTER STUDENT NUMBER</p>
    <input type="text" name="password" class="input"/>
    <div class="line-box">
      <div class="line"></div>
    </div>
  </label>
   <label class='label'>
    <p class="label-txt">ENTER STUDENT PASSWORD</p>
    <input type="text" name="password" class="input"/>
    <div class="line-box">
      <div class="line"></div>
    </div>
  </label>
 
    
  <button t-on-click="_onClickLink" class="button" type="button">submit</button>
</form>
</div>
</div>  
`;   }

    function setup() {
        const OwladdstudentInstance = new owlAddStudent();
        OwladdstudentInstance.mount($('.my_AddStudent_com')[0]);
    }

    whenReady(setup);

    return owlAddStudent;
});