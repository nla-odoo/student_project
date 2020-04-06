function app(){
// In this example, we show how hooks can be used or defined.
const { Component, Store } = owl;
const { xml } = owl.tags;
const { whenReady } = owl.utils;
const { useState, useRef, useDispatch, useStore } = owl.hooks;
// const { useRef, useState } = owl.hooks;


const actions = {
	addTask({ state }, title){
		title = title.trim();
		if (title) {
            const newTask = {
                id: state.nextId++,
                title: title,
                isCompleted: false,
            };
            state.tasks.push(newTask);
        }
	},
	toggleTask({ state }, id) {
	    const task = state.tasks.find(t => t.id === id);
	    task.isCompleted = !task.isCompleted;
	},
	deleteTask({ state }, id) {
	    const index = state.tasks.findIndex(t => t.id === id);
	    state.tasks.splice(index, 1);
	}
};
const initialState = {
  nextId: 1,
  tasks: []
};
// sub-component task
const task_templet = xml /* xml */
	`<div class="task" t-att-class="props.task.isCompleted ? 'done' : ''">
        <input type="checkbox" t-att-checked="props.task.isCompleted" t-on-click="dispatch('toggleTask', props.task.id)"/>
        <span><t t-esc="props.task.title"/></span>
        <span class="delete" t-on-click="dispatch('deleteTask', props.task.id)">delete</span>
    </div>`;

const app_template = xml /*xml*/
	`<div class="task-list">
		<input placeholder="Enter a new task" t-on-keyup="addTask" t-ref="add-input"/>
        <t t-foreach="tasks" t-as="task" t-key="task.id">
        	<Task task="task"/>
        </t>
    </div>`;


class Task extends Component{
		static template = task_templet;
        static props = ["task"];
  		dispatch = useDispatch();
}

// Main root component
class App extends Component {
        static template = app_template;
        static components = { Task };
		inputRef = useRef("add-input");
		mounted() {
		    this.inputRef.el.focus();
		}
		nextId = 1;
		tasks = useStore(state => state.tasks);
  		dispatch = useDispatch();

		addTask(ev) {
		    // 13 is keycode for ENTER
		    if (ev.keyCode === 13) {
		        this.dispatch("addTask", ev.target.value);
      			ev.target.value = "";
	    	}
		}

		
}

function makeStore() {
  console.log("makeStore");
  const localState = window.localStorage.getItem("todoapp");
  const state = localState ? JSON.parse(localState) : initialState;
  const store = new Store({ state, actions });
  store.on("update", null, () => {
  console.log("upade Store");
    localStorage.setItem("todoapp", JSON.stringify(store.state));
  });
  return store;
}
// Application setup
owl.config.mode = "dev";
App.env.store = makeStore();
const app = new App();
app.mount(document.body);
// const sub = new TASK_TEMPLATE();
}


/**
 * Initialization code
 * This code load templates, and make sure everything is properly connected.
 */
async function start() {
  let templates;
  try {
    templates = await owl.utils.loadFile('index.xml');
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