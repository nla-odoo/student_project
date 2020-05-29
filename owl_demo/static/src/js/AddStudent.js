odoo.define('owldemo.AddStudent', function (require) {
    "use strict";

    const rpc = require('web.rpc');

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class owlAddStudent extends Component {

        async willStart(){
            this.institutes_data = await rpc.query({route: '/get_institutes'});
            this.course_data = [];
        }

        get institutes () {
            return this.institutes_data;
        }

        get courses () {
            return this.course_data;
        }

         async _onClickLink(ev) {
            const form = document.querySelector('#addstudent');
            let params = new FormData(form);
            params = Object.fromEntries(params);
            await rpc.query({
                route: "/add_student",
                params: params
            }).then(function (result) {
                alert('Thanks for registering with us.')
            });
        }
        async _onChange(ev){
            const institute_id = parseInt(ev.target.value);
            const self = this;
            const cource_dropdown = document.querySelector("select[name='cource_dropdown']");
            if (institute_id) {
                await rpc.query({
                    route: "/get_courses",
                    params: {institute_id: institute_id }
                }).then(function (result) {
                    self.course_data = result;
                    cource_dropdown.disabled = false;
                    $(cource_dropdown).find('option').not(':first').remove();
                    result.forEach(function (cource) {
                        const option = document.createElement('option');
                        option.setAttribute('value', cource.id)
                        option.textContent = cource.name;
                        cource_dropdown.appendChild(option);
                    })
                });
            } else {
                cource_dropdown.disabled = true;
            }
        }

        static template = xml` 
            <div>
              <div>
                <h1 class='h1'><span class='styling'>Add</span>Student</h1>
                  <form class="form" id="addstudent">
                    <label class='label'>
                        <p class="label-txt">ENTER STUDENT EMAIL</p>
                        <input type="text" name="email" class="input"/>
                            <div class="line-box">
                                <div class="line"></div>
                            </div>
                    </label>
                    <label class='label'>
                        <p class="label-txt">ENTER STUDENT NAME</p>
                        <input type="text" name="name" class="input"/>
                            <div class="line-box">
                                <div class="line"></div>
                            </div>
                    </label>
                    <label class='label'>
                        <p class="label-txt">ENTER STUDENT PASSWORD1</p>
                        <input type="text" name="password" class="input"/>
                            <div class="line-box">
                                <div class="line"></div>
                            </div>
                    </label>
                    <div id="ins_dropdown">
                        <select name="ins_dropdown" class="form-control" t-on-change="_onChange">
                            <option value="0">select institute</option>
                            <t t-foreach="institutes" t-as="institute">
                                <option t-att-value="institute.id">
                                    <t t-esc="institute.name"/>
                                </option>
                            </t>
                        </select>
                    </div><p></p>
                    <div id="cource_dropdown">
                        <select name="cource_dropdown" class="form-control" disabled="disabled">
                            <option>select course</option>
                        </select>
                    </div><p></p>
                          <button t-on-click="_onClickLink" class="button" type="button">submit</button>
                  </form>
                </div>
            </div>  
`;   }

    return owlAddStudent;
});