// scripts.js (index.html)
// requer Plotly e Bootstrap bundle pré-carregados.

// util
const qs = id => document.getElementById(id);
const showError = msg => alert(msg);

// recarregar arquivos
qs('refreshFilesBtn')?.addEventListener('click', () => location.reload());

// UPLOAD CSV
qs('uploadBtnModal')?.addEventListener('click', () => {
  const input = qs('csvFile');
  const file = input.files[0];
  if (!file) { showError('Selecione um CSV.'); return; }

  const fd = new FormData();
  fd.append('file', file);

  fetch('/upload', { method: 'POST', body: fd })
    .then(r => r.json())
    .then(js => {
      if (js.success) {
        alert('Upload efetuado com sucesso.');
        location.reload();
      } else {
        showError(js.error || 'Erro no upload.');
      }
    })
    .catch(() => showError('Erro no upload.'));
});

// Quando muda o arquivo base: carregar colunas / filtros
qs('arquivoSelect')?.addEventListener('change', () => {
  const filename = qs('arquivoSelect').value;
  qs('colunaSelect').innerHTML = '<option value="">Selecione um arquivo primeiro</option>';
  qs('colunaGroupBy').innerHTML = '<option value="">Nenhum agrupamento</option>';
  qs('filtersArea').innerHTML = '';

  if (!filename) return;

  fetch('/api/columns', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ filename })
  })
  .then(r => r.json())
  .then(js => {
    if (js.error) { showError(js.error); return; }
    // popular selects
    qs('colunaSelect').innerHTML = '<option value="">-- escolha --</option>';
    qs('colunaGroupBy').innerHTML = '<option value="">Nenhum agrupamento</option>';
    js.columns.forEach(c => {
      const o = document.createElement('option'); o.value = c.name; o.textContent = c.name;
      qs('colunaSelect').appendChild(o);
      const o2 = o.cloneNode(true); qs('colunaGroupBy').appendChild(o2);
    });

    // criar filtros para colunas categóricas
    const filtersDiv = qs('filtersArea');
    filtersDiv.innerHTML = '<div class="small mb-2 text-muted">Filtros rápidos (marque valores)</div>';
    js.columns.forEach(c => {
      if (!c.is_numeric && c.unique_values_count <= 40) {
        const box = document.createElement('div'); box.className = 'mb-2';
        box.innerHTML = `<strong class="small">${c.name}</strong><div class="small mt-1" id="filter_${safeId(c.name)}"></div>`;
        filtersDiv.appendChild(box);
        const container = box.querySelector('div');
        c.sample_values.forEach(v => {
          const id = `cb_${safeId(c.name)}_${safeId(String(v))}`;
          const html = `<div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="${id}" data-col="${c.name}" value="${v}">
            <label class="form-check-label small" for="${id}">${v}</label>
          </div>`;
          container.insertAdjacentHTML('beforeend', html);
        });
      }
    });
  })
  .catch(()=> showError('Erro ao buscar colunas.'));
});

function safeId(s){ return String(s).replace(/\s+/g,'_').replace(/[^\w_-]/g,''); }

// Gather filters
function gatherFilters(){
  const checked = document.querySelectorAll('#filtersArea input[type=checkbox]:checked');
  const filtros = {};
  checked.forEach(cb => {
    const col = cb.dataset.col;
    if (!filtros[col]) filtros[col] = [];
    filtros[col].push(cb.value);
  });
  return filtros;
}

// Render multiple graphs returned pela API
function renderGraphs(resp){
  const container = qs('graficoContainer');
  container.innerHTML = '';
  if (!resp.graficos || resp.graficos.length === 0) {
    container.innerHTML = '<p class="text-center text-secondary">Nenhum gráfico retornado.</p>';
    return;
  }

  resp.graficos.forEach((g, idx) => {
    const card = document.createElement('div'); card.className = 'card';
    const header = document.createElement('div'); header.className = 'card-header d-flex justify-content-between align-items-center';
    header.style.background = '#f8f9fa';
    header.innerHTML = `<div><strong>${g.title || ('Gráfico ' + (idx+1))}</strong></div>
      <div class="btn-group">
        <button class="btn btn-sm btn-outline-secondary" onclick="downloadPlotlyPNG('chart_${idx}')">📥 PNG</button>
      </div>`;
    card.appendChild(header);

    const body = document.createElement('div'); body.className = 'card-body';
    const plot = document.createElement('div'); plot.id = `chart_${idx}`; plot.style.height = '420px';
    body.appendChild(plot);
    card.appendChild(body);
    container.appendChild(card);

    // desenhar
    try {
      const fig = g.fig || {};
      const data = fig.data || [];
      const layout = fig.layout || {};
      Plotly.react(plot.id, data, layout, {responsive:true});
    } catch (e) {
      plot.innerHTML = `<pre class="text-danger">Erro ao renderizar: ${String(e)}</pre>`;
    }
  });

  qs('btnSalvarTodos')?.classList.remove('d-none');
}

// download helper
function downloadPlotlyPNG(divId){
  Plotly.toImage(divId, {format:'png', width:1200, height:700})
    .then(dataUrl => {
      const a = document.createElement('a'); a.href = dataUrl; a.download = divId + '.png';
      document.body.appendChild(a); a.click(); a.remove();
    })
    .catch(()=> showError('Erro ao gerar imagem'));
}

// Gerar sem comparar
qs('btnGerar')?.addEventListener('click', () => {
  const filename = qs('arquivoSelect').value;
  const coluna = qs('colunaSelect').value;
  const tipo = qs('tipoSelect').value;
  const groupby = qs('colunaGroupBy').value || null;
  if (!filename || !coluna) { showError('Escolha arquivo e coluna'); return; }

  const payload = { filename, coluna, tipo, filtros: gatherFilters(), groupby };
  fetch('/api/grafico', {
    method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload)
  })
  .then(r => r.json())
  .then(js => {
    if (js.error) { showError(js.error); return; }
    renderGraphs(js);
  })
  .catch(()=> showError('Erro ao chamar /api/grafico'));
});

// Gerar + comparar
qs('btnGerarComparar')?.addEventListener('click', () => {
  const filename = qs('arquivoSelect').value;
  const compare = qs('arquivoCompare').value;
  const coluna = qs('colunaSelect').value;
  const tipo = qs('tipoSelect').value;
  const groupby = qs('colunaGroupBy').value || null;
  if (!filename || !coluna) { showError('Escolha arquivo base e coluna'); return; }
  if (!compare) { showError('Escolha o arquivo para comparar'); return; }
  if (compare === filename) { showError('Escolha um arquivo diferente para comparar'); return; }

  const payload = { filename, compare_with: compare, coluna, tipo, filtros: gatherFilters(), groupby };
  fetch('/api/grafico', {
    method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload)
  })
  .then(r => r.json())
  .then(js => {
    if (js.error) { showError(js.error); return; }
    renderGraphs(js);
  })
  .catch(()=> showError('Erro ao chamar /api/grafico'));
});

// salvar todos (opcional) - converte cada chart em png e baixa
qs('btnSalvarTodos')?.addEventListener('click', async () => {
  const charts = document.querySelectorAll('#graficoContainer [id^="chart_"]');
  for (let i=0; i<charts.length; i++){
    const id = charts[i].id;
    try {
      const dataUrl = await Plotly.toImage(id, {format:'png', width:1200, height:700});
      const a = document.createElement('a');
      a.href = dataUrl; a.download = `${id}.png`;
      document.body.appendChild(a); a.click(); a.remove();
    } catch(e) {
      console.warn('Erro ao salvar', id, e);
    }
  }
});
