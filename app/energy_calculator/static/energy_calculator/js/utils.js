export function calculateTotals(state) {
  const active = state.appliances.filter(a => a.on);

  const totalKwh = active.reduce(
    (sum, a) => sum + (a.watts / 1000) * a.hours,
    0
  );

  const daily = totalKwh * state.rate / 100;

  return {
    totalKwh,
    daily,
    monthly: daily * 30.4,
    annual: daily * 365
  };
}