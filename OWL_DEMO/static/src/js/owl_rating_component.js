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
                rating: "",
                feedback:"",
                res_id:"",
                res_model:"",
            });
        }

        async willStart() {
            this.product = await this.getProduct();
        }

        async getProduct () {
           return this.service;
        }
        get service ()  {
            debugger
            return this.product;
        }

        async _onClickLink(ev) {
            this.product = await rpc.query({ route: "/owl_demo_rating", 
                params:{rating: this.state.rating, 
                    feedback: this.state.feedback,
                    res_id: this.state.res_id,
                    res_model: this.state.res_model
                }});
            this.render(true);
          
        }

    // async _onClickLink(ev) {
    //         const self = this;
    //         rpc.query({ route: "/owl_demo_rating",
    //             params:{res_id: this.state.feedback,
    //             feedback: this.state.feedback,
    //         }}).then(function (result) {
    //             self.render(true);
    //             self.env.qweb.forceUpdate();
    //         });
    //     }

         static template = xml`<div>
            <div>
            <div>
                <form method="post">
                    <center><h1>Create Inquirey</h1></center>
                    <div class="form-group">
                        <label>Rate</label>
                        <input type="number" name='rate' t-model="state.rating" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>feedback</label>
                        <input type="text" name='feedback' t-model="state.feedback" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label>Res-id</label>
                        <input type="number" name='res_id' t-model="state.res_id" class="form-control"/>
                    </div>
                     <div class="form-group">
                        <label>res_model</label>
                        <input type="text" name='res_model' t-model="state.res_model" class="form-control"/>
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
