async function postJSON(url, payload) {
  const resp = await fetch(url, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(payload)
  });
  return resp.json();
}

document.getElementById('price-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const data = Object.fromEntries(fd.entries());
  if(data.age_months) data.age_months = Number(data.age_months);
  if(data.asking_price) data.asking_price = Number(data.asking_price);
  const res = await postJSON('/api/negotiate', data);
  document.getElementById('price-result').innerText = JSON.stringify(res, null, 2);
});

document.getElementById('mod-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const data = Object.fromEntries(fd.entries());
  const res = await postJSON('/api/moderate', data);
  document.getElementById('mod-result').innerText = JSON.stringify(res, null, 2);
});
