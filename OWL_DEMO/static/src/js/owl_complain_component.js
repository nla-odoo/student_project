odoo.define('OWL_DEMO.owl_complain_component', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_complain_component').length) {
        return Promise.reject("DOM doesn't contain '.my_complain_component'");
    }

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlComplain extends Component {
         static template = xml`<div>
         <h3>Complain</h3>

         
          <form name="frm">
        <div class="form-group col-4">
           <input type="email" name="email" class="form-control"/><br/>
           <input type="password" name="password" class="form-control"/><br/>
           <input type="text" name="feedback" class="form-control"/><br/>
           <input type="submit" name="submit" class="btn btn-primary"/>
           </div>
        </form>


         </div>`;
    }

    function setup() {
        const OwlComplainInstance = new OwlComplain();
        OwlComplainInstance.mount($('.my_complain_component')[0]);
    }

    whenReady(setup);

    return OwlComplain;
});