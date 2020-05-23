odoo.define('owl.acceptedlist', function(require) {
    "use strict";
    require('web.dom_ready');
    if (!$('.acceptedlist').length) {
        return Promise.reject("DOM doesn't contain '.my_dynamic_component'");
    }

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class owlAddStudentacceptedList extends Component {
        // res_active=[]
        async willStart() {
            console.log('me student list')
            this.student = await rpc.query({ route: '/acceptedstudent_rpc' });
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

        async _activeStudent(ev) {
            debugger;
            this.product = await rpc.query({
                route: "/studentlists",
                params: {
                    'action': 'active',
                    'student_id': ev.target.parentElement.parentElement.id
                }
            });
            this.render(true);
        }

        async _rejectStudent(ev) {
            this.product = await rpc.query({
                route: "/studentlists",
                params: {
                    'action': 'delete',
                    'student_id': ev.target.parentElement.parentElement.id
                }

            });
            this.render(true);
        }

        static template = xml ` 
        <div>
            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">student list</th>
                        <th scope="col">course fess</th>
                        <th scope="col">course name</th>
                    </tr>
                </thead>
                <tbody>
                    <t t-foreach="student.res_active" t-as="student"  t-key="'row_' + row_index">
                        <tr t-att-id="student.id">
                            <td><span t-esc="student.name"/></td>
                            <td><span t-esc="student.fess"/></td>        
                            <td><span t-esc="student.course_name"/></td>        
                        </tr>
                    </t>

                </tbody>
            </table>

        </div>
`;
    }

    function setup() {
        const acceptedlistptedstudent = new owlAddStudentacceptedList();
        acceptedlistptedstudent.mount($('.acceptedlist')[0]);
    }

    whenReady(setup);

    return owlAddStudentacceptedList;
});