odoo.define('loading_transportation_system.createtransporter', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.transporter_regi').length) {
        return Promise.reject("DOM doesn't contain '.transporter_regi'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class owlRagistartion extends Component {
        // email = "";
        async willStart(){
            this.Regist = await rpc.query({
                route: '/my/transporter_register'
            });
        }
        
        async _onClickLink(ev) {
            debugger
            const form = document.querySelector('#registration_form');
            let formData = new FormData(form);
            formData = Object.fromEntries(formData);
            
            this.registartion = await rpc.query({
                route: "/my/transporter_register", 
                params: {'form_data': formData}
            });
            window.location.href = "/web/login"
        }


        static template = xml`
        
        
        <div>
           <h1 class='h1'><span class='styling'>Regist</span>ration</h1>
               <form class="form" id="registration_form">
        
                  <div class="form-group">
                        <label>EMAIL</label>
                        <input type="text" name='email' class="form-control"/>
                    </div>
                <div class="form-group">
                    <label> NAME</label>
                    <input type="text" name="name" class="form-control"/>
                </div>    
                <div class="form-group">
                    <label>ENTER YOUR PASSWORD</label>
                    <input type="text" name="password" class="form-control"/>
                </div>              
                <label class='label'>SELECT YOUR CURRENCY</label>
                <div id="currncy_id">
                    <select name="currency_id" class="form-control currency_id">
                            <t t-foreach="Regist.resulrt" t-as="currency"  t-key="'row_' + row_index">
                                <option t-att-value="currency.id">
                                    <t t-esc="currency.name" />
                                   
                              </option>
                            </t>
                        </select>
                    </div>
                    <p></p>
                  <button t-on-click="_onClickLink" class="btn btn-primary" type="button">submit</button>
                </form>
                </div>
                `;
    }

    function setup() {
        const owlRagistartionInstance = new owlRagistartion();
        owlRagistartionInstance.mount($('.transporter_regi')[0]);
    }

    whenReady(setup);

    return owlRagistartion;
});
a