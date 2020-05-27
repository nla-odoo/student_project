odoo.define('owldemo.ragi', function (require) {
    "use strict";

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class owlRagistartion extends Component {
        // email = "";
        async willStart(){
            console.log('hhhhhhhhhhhhhhhh')
            this.Regist = await rpc.query({
                route: '/my/user_register'
            });
        }
        
        async _onClickLink(ev) {
            const form = document.querySelector('#registration_form');
            let formData = new FormData(form);
            formData = Object.fromEntries(formData);
            
            this.registartion = await rpc.query({
                route: "/my/user_register", 
                params: {'form_data': formData}
            });
            window.location.href = "/web/login"
        }


        static template = xml`
        
        
        <div>
           <h1 class='h1'><span class='styling'>Regist</span>ration</h1>
               <form class="form" id="registration_form">
        

                  <label class='label'>
                    <p class="label-txt">ENTER YOUR INSTITUTE EMAIL</p>
                    <input type="text" name="email" class="input"/>
                    <div class="line-box">
                      <div class="line"></div>
                    </div>
                  </label>
                  <label class='label'>
                    <p class="label-txt">ENTER YOUR INSTITUTE NAME</p>
                    <input type="text" name="name" class="input"/>
                    <div class="line-box">
                      <div class="line"></div>
                    </div>
                  </label>
                   <label class='label'>
                    <p class="label-txt">ENTER YOUR PASSWORD</p>
                    <input type="text" name="password" class="input"/>
                    <div class="line-box">
                      <div class="line"></div>
                    </div>
                  </label>
                   
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
                  <button t-on-click="_onClickLink" class="button" type="button">submit</button>
                </form>
                </div>
                `;
    }

    return owlRagistartion;
});