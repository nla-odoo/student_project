odoo.define('owldemo.my_addCource_com', function(require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.menu_item').length) {
        return Promise.reject("DOM doesn't contain '.menu_item'");
    }

    const rpc = require('web.rpc');
    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;


   class Menu extends Component {

        isStudent = false;

         async willStart() {
            this.isStudent= await rpc.query({ route: '/is_student' });
            this._renderMenuItem();
        }

        _renderMenuItem(mode) {
            mode = mode || 'addCource';
            if (mode === 'addCource') {
                const owlAddCourceInstance = new owlAddCource();
                owlAddCourceInstance.mount($('.component_view')[0]);
            } else if (mode === 'studentToAccept') {
                const owlAddStudentListInstance = new owlAddStudentList();
                owlAddStudentListInstance.mount($('.component_view')[0]);
            } else if (mode === 'studentList') {
                const owlAddStudentacceptedListInstance = new owlAddStudentacceptedList();
                owlAddStudentacceptedListInstance.mount($('.component_view')[0]);
            }
        }

       _onClickMenuItem(ev) {
            ev.preventDefault();
            const mode = ev.target.dataset.mode;
            $('.component_view').html('');
            this._renderMenuItem(mode);
            this.el.querySelector('.active').classList.remove('active');
            this.el.querySelector('a[data-mode="' + mode + '"]').classList.add('active')
        }

        static template = xml`
            <nav class="navbar navbar-expand-lg navbar-light bg-light">
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav" t-on-click="_onClickMenuItem">
                        <li class="nav-item">
                            <a class="nav-link active" href="#" data-mode="addCource">Add Cource</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#" data-mode="studentToAccept">Student To Accept</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#" data-mode="studentList">Student List</a>
                        </li>
                    </ul>
                </div>
            </nav>`;
    }

    class owlAddStudentacceptedList extends Component {

        async willStart() {
            this.student = await rpc.query({ route: '/acceptedstudent_rpc' });
        }

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

        static template = xml` 
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
            </div>`;
    }

    class owlAddCource extends Component {

        async willStart() {
            this.Regist = await rpc.query({ route: '/demo_AddCource' });

        }

        async _onClickLink(ev) {
            const form = document.querySelector('#addcource');
            let formData = new FormData(form);
            formData = Object.fromEntries(formData);

           this.product = await rpc.query({
                route: "/demo_AddCource", 
                params: {'form_data': formData}
            });
        }
       
        static template = xml `
            <div>
                <h1 class='h1'><span class='styling'>ADD</span>COURSE</h1>
                <form class="form" id="addcource">
                    <label class='label'>
                    <p class="label-txt">ENTER YOUR COURSE NAME</p>
                        <input type="text" name="name" class="input"/>
                    <div class="line-box">
                        <div class="line"></div>
                    </div>
                    </label>
                    <label class='label'>
                        <p class="label-txt">ENTER YOUR FEES</p>
                        <input type="text" name="list_price" class="input"/>
                    <div class="line-box">
                        <div class="line"></div>
                    </div>
                    </label>
                    <button t-on-click="_onClickLink" class="button" type="button">submit</button>
                </form>
            </div>`;
    }

    class owlAddStudentList extends Component {
        
        async willStart() {
            this.student = await rpc.query({ route: '/studentlists' });
        }

        async _activeStudent(ev) {
            this.student = await rpc.query({
                route: "/studentlists", 
                params: {
                    'action': 'active', 
                    'student_id': ev.target.parentElement.parentElement.id
                }
            });
            this.render(true);
        }

        async _rejectStudent(ev) {
            this.student = await rpc.query({
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
        const MenuInstance = new Menu();
        $('.o_portal.container').html('');
        MenuInstance.mount($('.o_portal.container')[0]);
    }

    whenReady(setup);

    return Menu;
});