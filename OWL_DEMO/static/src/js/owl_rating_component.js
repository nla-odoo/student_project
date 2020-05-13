odoo.define('OWL_DEMO.owl_rating_component', function (require) {
    "use strict";

    require('web.dom_ready');
    if (!$('.my_rating_component').length) {
        return Promise.reject("DOM doesn't contain '.my_rating_component'");
    }

    const { Component, hooks } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;

    class OwlRating extends Component {
         static template = xml`<div>
         		<h3>Rating</h3>


        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        
         </div>`;
    }

    function setup() {
        const OwlRatingInstance = new OwlRating();
        OwlRatingInstance.mount($('.my_rating_component')[0]);
    }

    whenReady(setup);

    return OwlRating;
});