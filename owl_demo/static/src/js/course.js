odoo.define('owldemo.course', function (require) {
    "use strict";

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class owlCource extends Component {

         async willStart(){
            this.courses_data = await rpc.query({route: '/get_courses'});
        }

        get courses () {
            return this.courses_data;
        }

        _addCourse (ev) {
            const owlCouceFormInstance = new owlCouceForm();
            owlCouceFormInstance.mount($('.component_view')[0]);
            this.destroy();
        }

        static template = xml `
            <div>
                <a href="#" t-on-click="_addCourse" class="btn btn-primary">Add Cource</a>
                <table>
                    <tr>
                        <th>Cource Name</th>
                        <th>Fees</th>
                    </tr>
                    <tr t-foreach="courses" t-as="course">
                        <td><t t-esc="course.name"/></td>
                        <td><t t-esc="course.list_price"/></td>
                    </tr>
                </table>
            </div>`;

    }

    class owlCouceForm extends Component {

        async _onClickLink(ev) {
            const form = document.querySelector('#addcource');
            let formData = new FormData(form);
            formData = Object.fromEntries(formData);

           await rpc.query({
                route: "/demo_AddCource", 
                params: formData
            });
           const owlCourceInstance = new owlCource();
            owlCourceInstance.mount($('.component_view')[0]);
            this.destroy();
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

    return owlCource;
});