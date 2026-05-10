export function calcTotal(appliances, rate) {
  let totalKwh = 0;

  appliances.forEach(a => {
    if (a.on) {
      totalKwh += (a.watts / 1000) * a.hours;
    }
  });

  const daily = totalKwh * rate / 100;

  return {
    kwh: totalKwh,
    daily,
    monthly: daily * 30,
    annual: daily * 365
  };
}