odoo.define('OWL_DEMO.owl_rating_component', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_rating_component').length) {
        return Promise.reject("DOM doesn't contain '.my_rating_component'");
    }

    const rpc = require('web.rpc');
    // const rating_display = require('OWL_DEMO.rating_display');

    const { Component, hooks, useState } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlRating extends Component {
        constructor() {
            super(...arguments);
            this.state = useState({
                res_id: "",
                feedback:"",
            });
        }
    async _onClickLink(ev) {
            const self = this;
            rpc.query({ route: "/owl_demo_rating",
                params:{res_id: this.state.feedback,
                feedback: this.state.feedback,
            }}).then(function (result) {
                self.render(true);
                self.env.qweb.forceUpdate();
            });
        }

         static template = xml`<div>
            <div>
            <div>
                <form method="post">
                    <center><h1>Create Inquirey</h1></center>
                    <div class="form-group">
                        <label>Feedback</label>
                        <input type="number" name='res_id' t-model="state.res_id" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>Feedback</label>
                        <input type="text" name='feedback' t-model="state.feedback" class="form-control"/>
                    </div>
                <a t-on-click="_onClickLink" class="btn btn-primary">Submit</a>
                </form>
            </div>
        </div>
        
         </div>`;
    }

    function setup() {
        const OwlRatingInstance = new OwlRating();
        OwlRatingInstance.mount($('.my_rating_component')[0]);
    }

    whenReady(setup);

    return OwlRating;
});
