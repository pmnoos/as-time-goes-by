export const state = {
  rate: 32,
  activeTab: 'calc',
  appliances: []
};

export function setState(newState) {
  Object.assign(state, newState);
}