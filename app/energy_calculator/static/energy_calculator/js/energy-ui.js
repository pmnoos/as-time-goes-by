import { APPLIANCES } from "./data.js";

export function renderCalculator(state, result) {
  const appDiv = document.getElementById('energy-app');
  if (!appDiv) return;

  appDiv.innerHTML = `
    <div class="ec-wrap">

      <!-- State selector -->
      <div class="ec-section">
        <label class="ec-label" for="state-select">State / territory</label>
        <select id="state-select" class="ec-select">
          ${state.states.map((s, i) => `
            <option value="${i}" ${state.rate === s.rate ? 'selected' : ''}>
              ${s.name} (${s.abbr}) — ${s.rate}c/kWh
            </option>
          `).join('')}
        </select>
      </div>

      <!-- Add appliance -->
      <div class="ec-section ec-add-row">
        <div class="ec-add-group">
          <label class="ec-label" for="add-appliance-select">Add an appliance</label>
          <select id="add-appliance-select" class="ec-select">
            <option value="">— choose an appliance —</option>
            ${APPLIANCES.map(a => `
              <option value="${a.name}">${a.name} (${a.watts}W)</option>
            `).join('')}
          </select>
        </div>
        <button id="add-appliance-btn" class="ec-btn-add" type="button">+ Add</button>
      </div>

      <!-- Summary cards -->
      <div class="ec-cards">
        <div class="ec-card">
          <span class="ec-card-label">Daily</span>
          <span class="ec-card-value">$${result.daily.toFixed(2)}</span>
        </div>
        <div class="ec-card">
          <span class="ec-card-label">Weekly</span>
          <span class="ec-card-value">$${(result.daily * 7).toFixed(2)}</span>
        </div>
        <div class="ec-card">
          <span class="ec-card-label">Monthly</span>
          <span class="ec-card-value">$${result.monthly.toFixed(2)}</span>
        </div>
        <div class="ec-card ec-card-highlight">
          <span class="ec-card-label">Annual</span>
          <span class="ec-card-value">$${result.annual.toFixed(0)}</span>
        </div>
      </div>

      <!-- Appliance table -->
      <div class="ec-table-wrap">
        ${state.apps.length === 0 ? `
          <div class="ec-empty">
            No appliances added yet — select one from the dropdown above.
          </div>
        ` : `
          <div class="ec-table-head">
            <span>Appliance</span>
            <span class="tc">Watts</span>
            <span class="tc">Hrs/day</span>
            <span class="tc">kWh/day</span>
            <span class="tr">Cost/day</span>
            <span class="tc">On/Off</span>
            <span></span>
          </div>
          ${state.apps.map((a, i) => {
            const kwh = a.on ? ((a.watts / 1000) * a.hours).toFixed(2) : '—';
            const cost = a.on ? `$${((a.watts / 1000) * a.hours * state.rate / 100).toFixed(2)}` : '—';
            return `
              <div class="ec-row ${a.on ? '' : 'ec-row-off'}">
                <div class="ec-row-name">${a.name}</div>
                <input class="ec-num" type="number" min="1" max="10000"
                  value="${a.watts}"
                  data-field="watts" data-idx="${i}"
                  aria-label="Watts for ${a.name}">
                <input class="ec-num" type="number" min="0.1" max="24" step="0.1"
                  value="${a.hours}"
                  data-field="hours" data-idx="${i}"
                  aria-label="Hours per day for ${a.name}">
                <div class="ec-kwh tc">${kwh}</div>
                <div class="ec-cost tr">${cost}</div>
                <button class="ec-toggle ${a.on ? 'ec-on' : 'ec-off'}"
                  data-app="${i}" type="button">
                  ${a.on ? 'ON' : 'OFF'}
                </button>
                <button class="ec-del" data-remove="${i}"
                  type="button" aria-label="Remove ${a.name}">✕</button>
              </div>
            `;
          }).join('')}
          <div class="ec-total-row">
            <span>Total</span>
            <span></span><span></span>
            <span class="tc">${result.kwh.toFixed(2)} kWh</span>
            <span class="tr ec-cost">$${result.daily.toFixed(2)}/day</span>
            <span></span><span></span>
          </div>
        `}
      </div>

      <p class="ec-note">
        Rates are averages for each state. Check your electricity bill for your exact rate.
        Rates: QLD 27.2c · NSW 28.5c · VIC 26.8c · SA 32.1c · WA 32.4c · ACT 25c · TAS 26.2c · NT 28c
      </p>

    </div>
  `;

  // ── Event listeners ──

  document.getElementById('state-select')
    .addEventListener('change', e => {
      window.selectState && window.selectState(e.target.value);
    });

  document.getElementById('add-appliance-btn')
    .addEventListener('click', () => {
      const sel = document.getElementById('add-appliance-select');
      if (sel.value) {
        window.addAppliance && window.addAppliance(sel.value);
        sel.value = '';
      }
    });

  // Also add on Enter key in dropdown
  document.getElementById('add-appliance-select')
    .addEventListener('keydown', e => {
      if (e.key === 'Enter' && e.target.value) {
        window.addAppliance && window.addAppliance(e.target.value);
        e.target.value = '';
      }
    });

  // Toggle ON/OFF
  appDiv.querySelectorAll('button[data-app]').forEach(btn => {
    btn.addEventListener('click', () => {
      window.toggleApp && window.toggleApp(parseInt(btn.dataset.app));
    });
  });

  // Remove appliance
  appDiv.querySelectorAll('button[data-remove]').forEach(btn => {
    btn.addEventListener('click', () => {
      window.removeAppliance && window.removeAppliance(parseInt(btn.dataset.remove));
    });
  });

  // Editable watts / hours
  appDiv.querySelectorAll('input.ec-num').forEach(input => {
    input.addEventListener('change', () => {
      const idx   = parseInt(input.dataset.idx);
      const field = input.dataset.field;
      window.updateAppliance && window.updateAppliance(idx, field, parseFloat(input.value) || 0);
    });
  });
}
