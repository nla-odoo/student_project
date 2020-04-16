
/**
 * This is the javascript code defined in the playground.
 * In a larger application, this code should probably be moved in different
 * sub files.
 */
function app() {
  // In this example, we show how hooks can be used or defined.
  const { useState } = owl.hooks;
  const {Component, tags} = owl;
  // const { xml } = tags;

  // Main root component
  class App extends Component {
      constructor() {
          super(...arguments);
          // simple state hook (reactive object)
          this.counter = useState({ value: 0 });
      }
      // static template = xml`
      // <div>
      //   <span t-on-click="increment(counter1)"><t t-esc="counter1.value"/></span>
      //   <span t-on-click="increment(counter2)"><t t-esc="counter2.value"/></span>
      // </div>`;
  // counter1 = useState({ value: 0 });
  // counter2 = useState({ value: 0 });

  increment(counter) {
    console.log("aaaaaaaaaaaa1")
    this.counter.value++;
  }
  }

  // Application setup
  const app = new App();
  app.mount(document.body);
}

/**
 * Initialization code
 * This code load templates, and make sure everything is properly connected.
 */
async function start() {
  let templates;
  try {
    console.log("aaaaaaaaaaaa")
    
    templates = await owl.utils.loadFile('app.xml');
  } catch(e) {
    console.error(`This app requires a static server.  If you have python installed, try 'python app.py'`);
    return;
  }
  const env = { qweb: new owl.QWeb({templates})};
  owl.Component.env = env;
  await owl.utils.whenReady();
  app();
}

start();
