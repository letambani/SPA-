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

  // Mostra botão do mapa se arquivo selecionado
  const btnMapa = qs('btnMostrarMapa');
  if (btnMapa) {
    btnMapa.style.display = filename ? 'inline-block' : 'none';
  }

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

// ========== VISUALIZAÇÕES COMPLETAS ==========
qs('btnVisualizacoesCompletas')?.addEventListener('click', () => {
  const filename = qs('arquivoSelect').value;
  if (!filename) {
    showError('Selecione um arquivo CSV primeiro');
    return;
  }

  const container = qs('graficoContainer');
  container.innerHTML = '<div class="text-center p-4"><div class="spinner-border text-primary" role="status"></div><p class="mt-3">Gerando visualizações completas...</p></div>';

  fetch('/api/visualizacoes_completas', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ filename })
  })
  .then(r => r.json())
  .then(js => {
    if (js.error) {
      showError(js.error);
      container.innerHTML = '<p class="text-center text-danger">Erro ao gerar visualizações</p>';
      return;
    }

    container.innerHTML = '';
    
    if (!js.visualizacoes || js.visualizacoes.length === 0) {
      container.innerHTML = '<p class="text-center text-secondary">Nenhuma visualização gerada. Verifique se o arquivo CSV contém dados válidos.</p>';
      return;
    }

      // Renderiza cada visualização
      js.visualizacoes.forEach((viz, idx) => {
        // Se for mapa, renderiza de forma especial
        if (viz.tipo === 'mapa') {
          renderMapaVisualizacao(viz, idx, container);
          return;
        }

        const card = document.createElement('div');
        card.className = 'card mb-3';
        
        const header = document.createElement('div');
        header.className = 'card-header d-flex justify-content-between align-items-center';
        header.style.background = '#f8f9fa';
        header.innerHTML = `
          <div>
            <strong>${viz.titulo}</strong>
            <span class="badge bg-secondary ms-2">${viz.tipo}</span>
          </div>
          <div class="btn-group">
            <button class="btn btn-sm btn-outline-secondary" onclick="downloadPlotlyPNG('viz_${idx}')">📥 PNG</button>
          </div>
        `;
        card.appendChild(header);

        const body = document.createElement('div');
        body.className = 'card-body';
        const plot = document.createElement('div');
        plot.id = `viz_${idx}`;
        plot.style.height = '450px';
        body.appendChild(plot);
        card.appendChild(body);
        container.appendChild(card);

        // Renderiza o gráfico
        try {
          const fig = viz.fig || {};
          const data = fig.data || [];
          const layout = fig.layout || {};
          Plotly.react(plot.id, data, layout, {responsive: true});
        } catch (e) {
          plot.innerHTML = `<pre class="text-danger">Erro ao renderizar: ${String(e)}</pre>`;
        }
      });

    qs('btnSalvarTodos')?.classList.remove('d-none');
    qs('btnMostrarMapa')?.style.setProperty('display', 'inline-block');
  })
  .catch(err => {
    console.error('Erro:', err);
    showError('Erro ao gerar visualizações completas');
    container.innerHTML = '<p class="text-center text-danger">Erro ao processar requisição</p>';
  });
});

// Função auxiliar para renderizar mapa nas visualizações completas
function renderMapaVisualizacao(viz, idx, container) {
  if (!viz.dados_mapa || !Array.isArray(viz.dados_mapa)) return;

  const card = document.createElement('div');
  card.className = 'card mb-3';
  
  const header = document.createElement('div');
  header.className = 'card-header d-flex justify-content-between align-items-center';
  header.style.background = '#f8f9fa';
  header.innerHTML = `
    <div>
      <strong>${viz.titulo}</strong>
      <span class="badge bg-info ms-2">Mapa Interativo</span>
    </div>
  `;
  card.appendChild(header);

  const body = document.createElement('div');
  body.className = 'card-body';
  
  const mapaDiv = document.createElement('div');
  mapaDiv.id = `mapa_viz_${idx}`;
  mapaDiv.style.height = '500px';
  mapaDiv.style.width = '100%';
  mapaDiv.style.borderRadius = '8px';
  mapaDiv.style.border = '1px solid #dee2e6';
  body.appendChild(mapaDiv);

  // Estatísticas
  if (viz.estatisticas) {
    const statsDiv = document.createElement('div');
    statsDiv.className = 'row mt-4 g-3';
    statsDiv.innerHTML = `
      <div class="col-6 col-md-3">
        <div class="card text-center">
          <div class="card-body">
            <h3 class="mb-0">${viz.estatisticas.total_alunos || 0}</h3>
            <small class="text-muted">Total de Alunos</small>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card text-center">
          <div class="card-body">
            <h3 class="mb-0">${viz.estatisticas.total_cidades || 0}</h3>
            <small class="text-muted">Cidades</small>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card text-center">
          <div class="card-body">
            <h5 class="mb-0" style="font-size: 1rem;">${viz.estatisticas.maior_concentracao || '-'}</h5>
            <small class="text-muted">Maior Concentração</small>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card text-center">
          <div class="card-body">
            <h3 class="mb-0">${viz.estatisticas.alunos_maior_cidade || 0}</h3>
            <small class="text-muted">Alunos na Maior Cidade</small>
          </div>
        </div>
      </div>
    `;
    body.appendChild(statsDiv);
  }

  card.appendChild(body);
  container.appendChild(card);

  // Cria mapa Leaflet
  if (typeof L !== 'undefined') {
    const mapa = L.map(`mapa_viz_${idx}`).setView([-27.6453, -48.6697], 10);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Leaflet | © OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(mapa);

    const quantidades = viz.dados_mapa.map(d => d.quantidade || 1);
    const maxQtd = Math.max(...quantidades);
    const minQtd = Math.min(...quantidades);

    viz.dados_mapa.forEach(cidade => {
      const quantidade = cidade.quantidade || 1;
      const tamanho = Math.max(8, Math.min(40, 8 + (quantidade / maxQtd) * 32));
      const intensidade = (quantidade - minQtd) / (maxQtd - minQtd || 1);
      const red = Math.round(231 - (intensidade * 50));
      const green = Math.round(142 - (intensidade * 100));
      const blue = Math.round(116 - (intensidade * 50));
      const cor = `rgb(${red}, ${green}, ${blue})`;

      const marker = L.circleMarker([cidade.lat, cidade.lng], {
        radius: tamanho,
        fillColor: cor,
        color: '#0B3353',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.7
      }).addTo(mapa);

      marker.bindPopup(`
        <strong>${cidade.nome}</strong><br>
        <strong>${quantidade}</strong> aluno(s)
      `);
    });

    if (viz.dados_mapa.length > 0) {
      const bounds = viz.dados_mapa.map(d => [d.lat, d.lng]);
      mapa.fitBounds(bounds, { padding: [50, 50] });
    }
  }
}

// ========== MAPA GEOGRÁFICO ==========
let mapaLeaflet = null;

function mostrarMapaGeografico() {
  const filename = qs('arquivoSelect').value;
  if (!filename) {
    showError('Selecione um arquivo CSV primeiro');
    return;
  }

  // Mostra o card do mapa
  const mapaCard = qs('mapaCard');
  if (mapaCard) {
    mapaCard.style.display = 'block';
    mapaCard.scrollIntoView({ behavior: 'smooth' });
  }

  // Limpa mapa anterior se existir
  const mapaDiv = qs('mapaGeografico');
  if (mapaDiv) {
    mapaDiv.innerHTML = '';
  }

  // Mostra loading
  if (mapaDiv) {
    mapaDiv.innerHTML = '<div class="text-center p-4"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Carregando...</span></div><p class="mt-2">Carregando mapa...</p></div>';
  }

  // Busca dados geográficos
  fetch('/api/mapa_geografico', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ filename })
  })
  .then(r => r.json())
  .then(js => {
    if (js.error) {
      showError(js.error);
      if (mapaDiv) mapaDiv.innerHTML = '<p class="text-center text-danger">Erro ao carregar dados geográficos</p>';
      return;
    }

    // Atualiza estatísticas
    if (js.estatisticas) {
      const stats = js.estatisticas;
      if (qs('statTotalAlunos')) qs('statTotalAlunos').textContent = stats.total_alunos || 0;
      if (qs('statTotalCidades')) qs('statTotalCidades').textContent = stats.total_cidades || 0;
      if (qs('statMaiorCidade')) qs('statMaiorCidade').textContent = stats.maior_concentracao || '-';
      if (qs('statAlunosMaior')) qs('statAlunosMaior').textContent = stats.alunos_maior_cidade || 0;
    }

    // Cria mapa Leaflet
    if (mapaDiv && typeof L !== 'undefined') {
      // Centro em Palhoça/SC (região da FMPSC)
      mapaLeaflet = L.map('mapaGeografico').setView([-27.6453, -48.6697], 10);

      // Adiciona tile layer
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Leaflet | © OpenStreetMap contributors',
        maxZoom: 19
      }).addTo(mapaLeaflet);

      // Encontra valores máximo e mínimo para normalizar tamanhos
      const quantidades = js.dados.map(d => d.quantidade || 1);
      const maxQtd = Math.max(...quantidades);
      const minQtd = Math.min(...quantidades);

      // Adiciona marcadores para cada cidade
      js.dados.forEach(cidade => {
        const quantidade = cidade.quantidade || 1;
        const nome = cidade.nome || 'Cidade desconhecida';
        
        // Tamanho do marcador proporcional à quantidade (entre 8 e 40 pixels)
        const tamanho = Math.max(8, Math.min(40, 8 + (quantidade / maxQtd) * 32));
        
        // Cor baseada na quantidade (vermelho para mais, azul para menos)
        const intensidade = (quantidade - minQtd) / (maxQtd - minQtd || 1);
        const red = Math.round(231 - (intensidade * 50)); // 231 (laranja) a 181
        const green = Math.round(142 - (intensidade * 100)); // 142 a 42
        const blue = Math.round(116 - (intensidade * 50)); // 116 a 66
        const cor = `rgb(${red}, ${green}, ${blue})`;

        // Cria marcador circular
        const marker = L.circleMarker([cidade.lat, cidade.lng], {
          radius: tamanho,
          fillColor: cor,
          color: '#0B3353',
          weight: 2,
          opacity: 1,
          fillOpacity: 0.7
        }).addTo(mapaLeaflet);

        // Tooltip com informações
        marker.bindPopup(`
          <strong>${nome}</strong><br>
          <strong>${quantidade}</strong> aluno(s)
        `);

        // Adiciona label no hover
        marker.on('mouseover', function(e) {
          this.openPopup();
        });
      });

      // Ajusta zoom para mostrar todos os marcadores
      if (js.dados.length > 0) {
        const bounds = js.dados.map(d => [d.lat, d.lng]);
        mapaLeaflet.fitBounds(bounds, { padding: [50, 50] });
      }
    } else {
      if (mapaDiv) {
        mapaDiv.innerHTML = '<p class="text-center text-danger">Biblioteca Leaflet não carregada. Recarregue a página.</p>';
      }
    }
  })
  .catch(err => {
    console.error('Erro ao carregar mapa:', err);
    showError('Erro ao carregar mapa geográfico');
    if (mapaDiv) {
      mapaDiv.innerHTML = '<p class="text-center text-danger">Erro ao carregar mapa</p>';
    }
  });
}