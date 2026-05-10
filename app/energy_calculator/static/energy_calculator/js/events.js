import { calcTotal } from "./calc.js";
import { renderResults } from "./energy-ui.js";

export function setupEvents(state) {

  window.selectState = (index) => {
    state.rate = state.states[index].rate;
    update(state);
  };

  window.toggleApp = (index) => {
    state.apps[index].on = !state.apps[index].on;
    update(state);
  };

  function update(state) {
    const result = calcTotal(state.apps, state.rate);
    renderResults(result);
  }
}