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
            this.student = await rpc.query({ route: '/studentlists' });
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
                    </tr>
                </thead>
                <tbody>
                    <t t-foreach="student.resulrt" t-as="student"  t-key="'row_' + row_index">
                        <tr t-att-id="student.id">
                            <td><span t-esc="student.name"/></td>
                            <td><span t-esc="student.list_price"/></td>
                            <td><span t-esc="student.course_name"/></td>
                            <td><span t-esc="student.fess"/></td>
                            <t t-if="!student.active">
                                <td>
                                    <button class="btn btn-primary" t-on-click="_activeStudent" name="btn_accept">Accept</button>
                                    <button class="btn btn-danger" t-on-click="_rejectStudent" name="btn_delete">Reject</button>
                                </td>
                            </t>
                            <t t-if="student.active">
                                <td>hello
                                    <button class="btn btn-primary" t-on-click="_activeStudent" name="btn_accept">Accept</button>
                                    <button class="btn btn-danger" t-on-click="_rejectStudent" name="btn_delete">Reject</button>
                                </td>
                            </t>
                        </tr>
                    </t>
                </tbody>
            </table>
        </div>`;
    }

    function setup() {
        const owlstudentlist = new owlAddStudentList();
        owlstudentlist.mount($('.liststudent')[0]);
    }

    whenReady(setup);

    return owlAddStudentList;
});