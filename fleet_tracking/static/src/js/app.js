function app() {
  // In this example, we show how hooks can be used or defined.
  const {Component, tags} = owl;
  // const { xml } = tags;

  // Main root component
  class product_list extends Component {
      constructor() {
          super(...arguments);
          console.log("1111111111111111")
          // simple state hook (reactive object)
          // this.counter = useState({ value: 0 });
      }
      // counter = {value: 0};
      // static template = xml`<div t-on-click="increment" class="button"><t t-esc="counter.value"/></div>`;

      // increment() {
      //     this.counter.value++;
      //     // this.render();
      // }
  }

  // Application setup
  const app = new App();
  app.mount(document.body);
}