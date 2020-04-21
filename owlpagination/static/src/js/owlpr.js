(function() {
    console.log("hello hulk", owl.__info__.version);
})();
// templates =  owl.utils.loadFile('portal_user.xml');
const { Component } = owl;
const { xml } = owl.tags;
const { whenReady } = owl.utils;

// Owl Components
class App extends Component {
  static template = xml/* xml */ `
    <div class="task-list">
        <t t-foreach="tasks" t-as="task" t-key="task.id">
            <div class="task">
                <input type="checkbox" t-att-checked="task.isCompleted"/>
                <span><t t-esc="task.title"/></span>
            </div>
        </t>
    </div>`;

  tasks = [
    {
      id: 1,
      title: "buy milk",
      isCompleted: true
    },
    {
      id: 2,
      title: "clean house",
      isCompleted: false
    }
  ];
}
function setup() {
  const app = new App();
  app.mount(document.body);
}

whenReady(setup);