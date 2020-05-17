odoo.define('owldemo.my_addCource_com', function(require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_addCource_com').length) {
        return Promise.reject("DOM doesn't contain '.my_dynamic_component'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

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
    }

    function setup() {
        const owladdcourceInstance = new owlAddCource();
        owladdcourceInstance.mount($('.my_addCource_com')[0]);
    }

    whenReady(setup);

    return owlAddCource;
});