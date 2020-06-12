// odoo.define('owldemo.payment_respo', function(require) {
//     "use strict";

//     // require('web.dom_ready');
//     // if (!$('.payment_com').length) {
//     //     return Promise.reject("DOM doesn't contain '.payment_com'");
//     // }

//     const rpc = require('web.rpc');

//     const { Component, hooks } = owl;
//     const { xml } = owl.tags;
//     const { whenReady } = owl.utils;

//         // debugger
//     class Payment extends Component {
//         // email = "";
//         // async willStart() {
//         //     this.Regist = await rpc.query({route: '/studentpayment'});
//         // }

//         // async _onClickLink(ev) {



//         //     const form1 = document.querySelector('#addpayment');
//         //     let formData = new FormData(form1);
//         //     formData = Object.fromEntries(formData);
//         //    this.student = await rpc.query({
//         //         route: "/paytm_response", 
//         //         params: {'form_data': formData}
//         //     });
        


//         //     var data = this.Regist.data_dict
//         //     var form = document.createElement('form');
//         //     form.setAttribute("method", "post");
//         //     form.setAttribute("id", "addpayment");
//         //     form.setAttribute("action", data.redirection_url);
//         //     delete data['redirection_url'];
//         //     for (const prop in data) {
//         //         var inp = document.createElement('input');
//         //         inp.setAttribute("type", 'hidden');
//         //         inp.setAttribute("name", prop)
//         //         inp.setAttribute("value", data[prop])
//         //         form.append(inp);
//         //     }
//         //     document.body.append(form)
//         //     debugger
//         //     form.submit()
//         // }




//         static template = xml `
//         <div>
//             <h1 class='h1'><span class='styling'>Student </span>Dtails</h1>
//            <form id="payment">
//            </form>
//         </div>
//                 `;
//     }

//     // function setup() {
//     //     debugger
//     //     const paymentStudentIn = new Payment();
//     //     paymentStudentIn.mount($('.payment_com')[0]);
//     // }

//     // whenReady(setup);

//     return Payment;
// });