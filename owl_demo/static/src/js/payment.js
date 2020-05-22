odoo.define('owldemo.payment_com', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.payment_com').length) {
        return Promise.reject("DOM doesn't contain '.payment_com'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class Payment extends Component {
        // email = "";
        async willStart(){
            console.log('payment_com')
            this.Regist = await rpc.query({

                route: '/studentpayment'
            });
            debugger
        }
        
        

        static template = xml`
        <div>
           hello
        </div>
                `;
    }

    function setup() {
        debugger
        const paymentStudentIn = new Payment();
        paymentStudentIn.mount($('.payment_com')[0]);
    }

    whenReady(setup);

    return Payment;
});