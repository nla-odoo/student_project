odoo.define('task_owl.app', function (require) {
	// const { useState } = owl.hooks;
  	const {Component, tags} = owl;
  	const { xml } = tags;
  	class home extends Component{
  		constructor() {
          super(...arguments);
          console.log("Asdafsafasf	")
          // debugger;
     	}
		static template = xml`
		      <div>
		        <h1>yyyyyyyyyyyyyyyyyy</h1>
		      </div>`;
  	}


  	home = new home();
  	Component.template = "abc"
  	// home.mount(Component.template)
});
