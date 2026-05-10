import { STATES, APPLIANCES } from "./data.js";
import { renderCalculator } from "./energy-ui.js";
import { calcTotal } from "./calc.js";

const state = {
  states: STATES,
  apps: [],
  rate: STATES[0].rate   // defaults to QLD
};

function updateUI() {
  const result = calcTotal(state.apps, state.rate);
  renderCalculator(state, result);
}

function init() {

  // Change state / rate
  window.selectState = (index) => {
    state.rate = state.states[index].rate;
    updateUI();
  };

  // Toggle appliance ON / OFF
  window.toggleApp = (index) => {
    state.apps[index].on = !state.apps[index].on;
    updateUI();
  };

  // Add appliance from dropdown
  window.addAppliance = (name) => {
    const appliance = APPLIANCES.find(a => a.name === name);
    if (appliance) {
      state.apps.push({ ...appliance, on: true });
      updateUI();
    }
  };

  // Remove appliance
  window.removeAppliance = (index) => {
    state.apps.splice(index, 1);
    updateUI();
  };

  // Edit watts or hours inline
  window.updateAppliance = (index, field, value) => {
    if (state.apps[index]) {
      state.apps[index][field] = value;
      updateUI();
    }
  };

  updateUI();
}

init();
