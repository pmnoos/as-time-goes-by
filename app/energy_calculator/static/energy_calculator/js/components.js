import { calculateTotals } from './utils.js';

export function Header() {
  return `
    <div class="text-center mb-6">
      <h1 class="text-3xl font-serif">Energy Calculator</h1>
    </div>
  `;
}

export function Tabs(state) {
  return `
    <div class="flex gap-2 justify-center mb-6">
      <button data-tab="calc" class="px-3 py-1 border rounded ${state.activeTab === 'calc' ? 'bg-emerald-200' : ''}">
        Calculator
      </button>
      <button data-tab="solar" class="px-3 py-1 border rounded ${state.activeTab === 'solar' ? 'bg-emerald-200' : ''}">
        Solar
      </button>
    </div>
  `;
}

export function ApplianceList(state) {
  return `
    <div class="space-y-2">
      ${state.appliances.map((a, i) => `
        <div class="flex justify-between border p-3 rounded">
          <div>
            <div class="font-medium">${a.name}</div>
            <div class="text-sm text-gray-500">${a.watts}W • ${a.hours}h</div>
          </div>

          <button data-toggle="${i}" class="px-2 py-1 rounded ${a.on ? 'bg-green-200' : 'bg-gray-200'}">
            ${a.on ? 'ON' : 'OFF'}
          </button>
        </div>
      `).join('')}
    </div>
  `;
}

export function Results(state) {
  const totals = calculateTotals(state);

  return `
    <div class="mt-6 text-center">
      <div class="text-lg font-semibold">Daily: $${totals.daily.toFixed(2)}</div>
      <div class="text-sm text-gray-600">${totals.totalKwh.toFixed(2)} kWh/day</div>
      <div class="text-sm">Monthly: $${totals.monthly.toFixed(2)}</div>
      <div class="text-sm">Annual: $${totals.annual.toFixed(0)}</div>
    </div>
  `;
}

export function Calculator(state) {
  return `
    <div>
      <div class="mb-4">
        <label class="block mb-1">Rate (¢/kWh)</label>
        <input id="rate-input" type="number" value="${state.rate}" class="border p-2 rounded w-full">
      </div>

      ${ApplianceList(state)}
      ${Results(state)}
    </div>
  `;
}

export function Solar() {
  return `
    <div class="text-center text-gray-600">
      Solar calculator coming next ☀️
    </div>
  `;
}