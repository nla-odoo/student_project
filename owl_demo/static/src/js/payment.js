odoo.define('owldemo.payment_com', function(require) {
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
        async willStart() {
            console.log('payment_com')
            this.Regist = await rpc.query({

                route: '/studentpayment'
            });
            debugger
        }




        static template = xml `
        <div>
            <h1 class='h1'><span class='styling'>Student </span>invoice</h1>
            <table class="table">
                <thead>              
                    <tr>
                        <th scope="col">student name</th>
                        <th scope="col">student course name</th>
                        <th scope="col">student fees</th>
                        <th scope="col">student action</th>
                    </tr>
                </thead>
                <tbody>
                    <td><span t-esc="Regist.name"/></td>
                    <td><span t-esc="Regist.course_name"/></td>
                    <td><span t-esc="Regist.fees"/></td>
                        <td>
                            <button class="btn btn-primary" t-on-click="_activeStudent" name="btn_accept">Payment now</button>                        
                        </td>
                </tbody>
            </table>
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