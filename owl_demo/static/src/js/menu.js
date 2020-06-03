odoo.define('owldemo.my_addCource_com', function(require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.menu_item').length) {
        return Promise.reject("DOM doesn't contain '.menu_item'");
    }

    const rpc = require('web.rpc');
    const session = require('web.session');
    const student_register = require('owldemo.AddStudent');
    const institute_register = require('owldemo.ragi');
    const course = require('owldemo.course');
    const payment = require('owldemo.payment_com');
    const owlAddStudentList = require('owldemo.student_to_accepted');
    const owlAddStudentacceptedList = require('owldemo.acceptedstuden');
    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;


   class Menu extends Component {

        isStudent = false;

         async willStart() {
            this.toRegsiter = !session.user_id;
            this.isStudent= await rpc.query({ route: '/is_student' });
            this._renderMenuItem();
        }

        _renderMenuItem(mode) {
            if (this.toRegsiter) {
                mode = mode || 'registerAsStudent';
                if (mode === 'registerAsStudent') {
                    const studentRegisterInstance = new student_register();
                    studentRegisterInstance.mount($('.component_view')[0]);
                } else if (mode === 'registerAsInstitute') {
                    const instituteRegisterInstance = new institute_register();
                    instituteRegisterInstance.mount($('.component_view')[0]);
                }
            } else {
                mode = mode || 'addCource';
                if(this.isStudent){mode='Payment'}
                if (mode === 'addCource') {
                    const courceInstance = new course();
                    courceInstance.mount($('.component_view')[0]);
                } else if (mode === 'studentToAccept') {
                    const owlAddStudentListInstance = new owlAddStudentList();
                    owlAddStudentListInstance.mount($('.component_view')[0]);
                } else if (mode === 'studentList') {
                    const owlAddStudentacceptedListInstance = new owlAddStudentacceptedList();
                    owlAddStudentacceptedListInstance.mount($('.component_view')[0]);
                }
                else if (mode === 'Payment') {
                    const owlAddStudentacceptedListInstance = new payment();
                    owlAddStudentacceptedListInstance.mount($('.component_view')[0]);
                }
            }
        }

        get register () {
            return this.toRegsiter;
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
                        <t t-if="register">
                            <li class="nav-item">
                                <a class="nav-link active" href="#" data-mode="registerAsStudent">Register as Student</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="#" data-mode="registerAsInstitute">Register as Institute</a>
                            </li>
                        </t>
                        <t t-else="">
                            <t t-if="!isStudent">
                                <li class="nav-item">
                                    <a class="nav-link active" href="#" data-mode="addCource">Cource</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="#" data-mode="studentToAccept">Student To Accept</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="#" data-mode="studentList">Student List</a>
                                </li>
                            </t>
                            <t t-else="">
                                <li class="nav-item">
                                    <a class="nav-link active" href="#" data-mode="Payment">payment</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="#" data-mode="studentList">Payment Details</a>
                                </li>
                            </t>
                        </t>
                    </ul>
                </div>
            </nav>`;
    }

    function setup() {
        const MenuInstance = new Menu();
        $('.o_portal.container').html('');
        MenuInstance.mount($('.o_portal.container')[0]);
    }

    whenReady(setup);

    return Menu;
});