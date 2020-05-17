odoo.define('owl.list', function(require) {
    "use strict";
    require('web.dom_ready');
    if (!$('.liststudent').length) {
        return Promise.reject("DOM doesn't contain '.my_dynamic_component'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class owlAddStudentList extends Component {

        async willStart() {
            console.log('me student list')
            this.student = await rpc.query({ route: '/studentlists' });
            debugger;

        }

        //  async _onClickLink(ev) {
        //     debugger
        //     const form = document.querySelector('#addstudent');
        //     let formData = new FormData(form);
        //     formData = Object.fromEntries(formData);

        //    this.product = await rpc.query({
        //         route: "/demo_AddStudent", 
        //         params: {'form_data': formData}
        //     });
        // }



        static template = xml ` 
        <div>
            <table class="table">
            <thead>
                <tr>
                    <th scope="col">student list</th>
                </tr>
            </thead>
            <tbody>
            <t t-foreach="student.resulrt" t-as="student"  t-key="'row_' + row_index">
                <tr>
                    <span t-esc="student.name" ><h1></h1></span>
                    <span t-esc="student.list_price" ><h1></h1></span>
                </tr>
                </t>
            </tbody>
            </table>
        </div>
`;
    }

    function setup() {
        const owlstudentlist = new owlAddStudentList();
        owlstudentlist.mount($('.liststudent')[0]);
    }

    whenReady(setup);

    return owlAddStudentList;
});