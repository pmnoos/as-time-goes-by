export const state = {
  rate: 32,
  activeTab: 'calc',
  appliances: []
};

export function setState(newState) {
  Object.assign(state, newState);
}

export function renderResults(result) {
  // TODO: Implement rendering logic
  const appDiv = document.getElementById('energy-app');
  if (appDiv) {
    appDiv.innerHTML = `<pre>${JSON.stringify(result, null, 2)}</pre>`;
  }
}