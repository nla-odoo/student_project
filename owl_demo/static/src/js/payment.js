odoo.define('owldemo.payment_com', function(require) {
    "use strict";

    // require('web.dom_ready');
    // if (!$('.payment_com').length) {
    //     return Promise.reject("DOM doesn't contain '.payment_com'");
    // }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class Payment extends Component {
        // email = "";
        async willStart() {
            this.Regist = await rpc.query({route: '/studentpayment'});
        }

        async _onClickLink(ev) {

            debugger;



            var data = this.Regist.data_dict
            var form = document.createElement('form');
            form.setAttribute("method", "post");
            form.setAttribute("id", "addpayment");
            form.setAttribute("action", data.redirection_url);
            delete data['redirection_url'];
            for (const prop in data) {
                var inp = document.createElement('input');
                inp.setAttribute("type", 'hidden');
                inp.setAttribute("name", prop)
                inp.setAttribute("value", data[prop])
                form.append(inp);
            }
            document.body.append(form)
            debugger
           //  const fom = document.querySelector('#addpayment');
           //  let formData = new FormData(fom);
           //  formData = Object.fromEntries(formData);
           // this.student = await rpc.query({
           //      route: "/paytm_response", 
           //      params: {'form_data': formData}
           //  });
        
            form.submit()
        }




        static template = xml `
        <div>
            <h1 class='h1'><span class='styling'>Student </span>invoice</h1>
           <form id="payment">
            <table class="table">
                 <input type="text" t-att-value='Regist.id' name="res_user_id"/>
                <thead>              
                    <tr>
                        <th scope="col">student name</th>
                        <th scope="col">student course id</th>
                        <th scope="col">student course name</th>
                        <th scope="col">student fees</th>
                        <th scope="col">student status</th>
                        
                    </tr>
                </thead>
                <tbody>
                    <td><span t-esc="Regist.name"/></td>
                    <td><span t-esc="Regist.id"/></td>
                    <td><span t-esc="Regist.course_name"/></td>
                    <td><span t-esc="Regist.fees"/></td>
                    <td>
                        <button type="button" class="btn btn-primary" t-on-click="_onClickLink" name="btn_accept">Payment now</button>                        
                    </td>
                </tbody>
            </table>
            </form>
        </div>
                `;
    }

    // function setup() {
    //     debugger
    //     const paymentStudentIn = new Payment();
    //     paymentStudentIn.mount($('.payment_com')[0]);
    // }

    // whenReady(setup);

    return Payment;
});