odoo.define('owldemo.acceptedstuden', function (require) {
    "use strict";

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class owlAddStudentacceptedList extends Component {

        async willStart() {
            this.student = await rpc.query({ route: '/acceptedstudent_rpc' });
        }

        static template = xml` 
            <div>
                <table class="table">
                    <thead>
                        <tr>
                            <th scope="col">student list</th>
                            <th scope="col">course fess</th>
                            <th scope="col">course name</th>
                            <th scope="col">payment status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <t t-foreach="student.res_active" t-as="student"  t-key="'row_' + row_index">
                            <tr t-att-id="student.id">
                                <td><span t-esc="student.name"/></td>
                                <td><span t-esc="student.fess"/></td>        
                                <td><span t-esc="student.course_name"/></td>        
                                <td>done</td>        
                            </tr>
                        </t>

                    </tbody>
                </table>
            </div>`;
    }

    return owlAddStudentacceptedList;
});