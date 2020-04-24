odoo.define('task_owl.app', function (require) {
	// const { useState } = owl.hooks;
  	const {Component, tags} = owl;
  	const { xml } = tags;
  	class home extends Component{
  		constructor() {
          super(...arguments);
          console.log("Asdafsafasf	")
          // debugger;    </div>

     	}
  	}

  	home = new home();
    home.template = "home1" 
  	// Component.template = "abc"
  	// home.mount(Component.template)
});





















// component.js

// create component

// class new_component extends compontent {

// }

// new_component.template = 'com_template'


// create tmeplate

// <t t-name="com_template" owl="1">
//      <div>
//          <h1>Hello</h1>
//      </div>
// </t>

// create controller
// and render controller_template from here


// <t t-name="controller_template">
//      <div>
//          <new_component>
//      </div>
// </t>