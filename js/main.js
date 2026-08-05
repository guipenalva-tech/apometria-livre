/* Apometria Livre — comportamento do site (sem dependências).
   1. Alternância de idioma PT ⇄ ES: elementos traduzíveis carregam o texto em
      espanhol no atributo data-es; o original (PT) é guardado em data-pt na
      primeira troca, permitindo alternar quantas vezes quiser.
   2. Menu móvel acessível (aria-expanded, fecha com Esc).
   3. Marcação automática do link ativo (nav e tab bar) via URL.
   4. Filtro do diretório com busca insensível a acentos ("vovo" acha "Vovó").
   5. Modal de participação (dialog nativo: foco preso e Esc de graça). */

(function () {
  var LANG_KEY = 'apometria-lang';

  function aplicarIdioma(lang) {
    document.documentElement.lang = lang === 'es' ? 'es' : 'pt-BR';
    document.querySelectorAll('[data-es]').forEach(function (el) {
      if (!el.dataset.pt) el.dataset.pt = el.innerHTML;
      el.innerHTML = lang === 'es' ? el.dataset.es : el.dataset.pt;
    });
    document.querySelectorAll('[data-es-placeholder]').forEach(function (el) {
      if (!el.dataset.ptPlaceholder) el.dataset.ptPlaceholder = el.placeholder;
      el.placeholder = lang === 'es' ? el.dataset.esPlaceholder : el.dataset.ptPlaceholder;
    });
    document.querySelectorAll('.lang-toggle').forEach(function (btn) {
      btn.textContent = lang === 'es' ? '🇧🇷 Português' : '🇪🇸 Español';
      btn.setAttribute('aria-label', lang === 'es' ? 'Mudar idioma para português' : 'Cambiar idioma a español');
    });
    try { localStorage.setItem(LANG_KEY, lang); } catch (e) {}
  }

  /* Remove acentos para comparação: "vovó" → "vovo" */
  function semAcentos(texto) {
    return texto.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  /* Marca o link da página atual na nav e na tab bar (visual + leitores de tela) */
  function marcarPaginaAtiva() {
    var pagina = (location.pathname.split('/').pop() || 'index.html');
    document.querySelectorAll('.nav-links a, .tab-bar a').forEach(function (a) {
      var destino = a.getAttribute('href').split('#')[0];
      if (destino === pagina) {
        a.classList.add('ativo');
        a.setAttribute('aria-current', 'page');
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var lang = 'pt';
    try { lang = localStorage.getItem(LANG_KEY) || 'pt'; } catch (e) {}
    aplicarIdioma(lang === 'es' ? 'es' : 'pt');
    marcarPaginaAtiva();

    document.querySelectorAll('.lang-toggle').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var atual = document.documentElement.lang === 'es' ? 'es' : 'pt';
        aplicarIdioma(atual === 'pt' ? 'es' : 'pt');
      });
    });

    var menuBtn = document.querySelector('.menu-btn');
    var links = document.querySelector('.nav-links');
    if (menuBtn && links) {
      menuBtn.setAttribute('aria-expanded', 'false');
      menuBtn.setAttribute('aria-controls', 'menu-principal');
      links.id = 'menu-principal';

      function fecharMenu() {
        links.classList.remove('aberto');
        menuBtn.setAttribute('aria-expanded', 'false');
      }
      menuBtn.addEventListener('click', function () {
        var aberto = links.classList.toggle('aberto');
        menuBtn.setAttribute('aria-expanded', aberto ? 'true' : 'false');
      });
      links.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', fecharMenu);
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') fecharMenu();
      });
    }

    // Filtros do diretório: País › Estado › Cidade (em cascata) + busca por texto.
    // O seletor de Estado lista TODAS as UFs do Brasil — inclusive as que ainda
    // não têm casa mapeada — para que o visitante veja um feedback claro de
    // "sem resultado" no seu estado, em vez de a UF simplesmente não existir.
    var busca = document.querySelector('#busca-inst');
    var selPais = document.querySelector('#filtro-pais');
    var selEstado = document.querySelector('#filtro-estado');
    var selCidade = document.querySelector('#filtro-cidade');
    if (busca && selPais && selEstado && selCidade) {
      var cartoes = Array.prototype.slice.call(document.querySelectorAll('.inst-cartao'));

      // Todas as 27 UFs (sigla → nome) para popular o seletor e nomear o feedback
      var UFS = {
        AC: 'Acre', AL: 'Alagoas', AP: 'Amapá', AM: 'Amazonas', BA: 'Bahia',
        CE: 'Ceará', DF: 'Distrito Federal', ES: 'Espírito Santo', GO: 'Goiás',
        MA: 'Maranhão', MT: 'Mato Grosso', MS: 'Mato Grosso do Sul', MG: 'Minas Gerais',
        PA: 'Pará', PB: 'Paraíba', PR: 'Paraná', PE: 'Pernambuco', PI: 'Piauí',
        RJ: 'Rio de Janeiro', RN: 'Rio Grande do Norte', RS: 'Rio Grande do Sul',
        RO: 'Rondônia', RR: 'Roraima', SC: 'Santa Catarina', SP: 'São Paulo',
        SE: 'Sergipe', TO: 'Tocantins'
      };

      function valoresUnicos(attr, restricoes) {
        var lista = [];
        cartoes.forEach(function (c) {
          for (var chave in restricoes) {
            if (restricoes[chave] && c.dataset[chave] !== restricoes[chave]) return;
          }
          var v = c.dataset[attr];
          if (v && lista.indexOf(v) < 0) lista.push(v);
        });
        return lista.sort();
      }

      function preencher(select, valores, rotuloTodos, rotulos) {
        var anterior = select.value;
        select.innerHTML = '';
        var todos = document.createElement('option');
        todos.value = '';
        todos.textContent = rotuloTodos;
        select.appendChild(todos);
        valores.forEach(function (v) {
          var o = document.createElement('option');
          o.value = v;
          o.textContent = rotulos ? rotulos[v] || v : v;
          select.appendChild(o);
        });
        if (valores.indexOf(anterior) >= 0) select.value = anterior;
      }

      function ufsOrdenadas() {
        return Object.keys(UFS).sort(function (a, b) {
          return UFS[a].localeCompare(UFS[b], 'pt-BR');
        });
      }

      function reconstruirOpcoes() {
        preencher(selPais, valoresUnicos('pais', {}), 'País: todos');
        preencher(selEstado, ufsOrdenadas(), 'Estado: todos', UFS);
        preencher(selCidade, valoresUnicos('cidade', { pais: selPais.value, estado: selEstado.value }), 'Cidade: todas');
      }

      function nomeDoLocal() {
        if (selCidade.value) return selCidade.value;
        if (selEstado.value) return UFS[selEstado.value] || selEstado.value;
        if (busca.value.trim()) return '“' + busca.value.trim() + '”';
        return '';
      }

      function aplicarFiltros() {
        var termo = semAcentos(busca.value);
        var visiveis = 0;
        cartoes.forEach(function (c) {
          var ok = (!selPais.value || c.dataset.pais === selPais.value) &&
                   (!selEstado.value || c.dataset.estado === selEstado.value) &&
                   (!selCidade.value || c.dataset.cidade === selCidade.value) &&
                   semAcentos(c.textContent).indexOf(termo) >= 0;
          c.style.display = ok ? '' : 'none';
          if (ok) visiveis++;
        });
        var cardVazio = document.querySelector('#card-inscricao');
        var msg = document.querySelector('#msg-sem-resultado');
        if (visiveis === 0) {
          if (msg) {
            var local = nomeDoLocal();
            var es = document.documentElement.lang === 'es';
            if (local) {
              msg.textContent = es
                ? 'Todavía no mapeamos casas de Apometría en ' + local + '.'
                : 'Ainda não mapeamos casas de Apometria em ' + local + '.';
            } else {
              msg.textContent = es
                ? 'Ninguna casa encontrada con este filtro.'
                : 'Nenhuma casa encontrada com este filtro.';
            }
          }
          if (cardVazio) cardVazio.style.display = '';
        } else if (cardVazio) {
          cardVazio.style.display = 'none';
        }
      }

      reconstruirOpcoes();
      [selPais, selEstado].forEach(function (sel) {
        sel.addEventListener('change', function () { reconstruirOpcoes(); aplicarFiltros(); });
      });
      selCidade.addEventListener('change', aplicarFiltros);
      busca.addEventListener('input', aplicarFiltros);

      // ===== Melhorias: busca, geolocalização, mapa e gráfico =====

      // Contagem de casas por UF — a partir dos próprios cards (sempre em sincronia)
      var CONTAGEM = {};
      cartoes.forEach(function (c) {
        var u = c.dataset.estado;
        if (u) CONTAGEM[u] = (CONTAGEM[u] || 0) + 1;
      });

      function irParaResultados() {
        var alvo = document.querySelector('.filtro-nav');
        if (alvo) alvo.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
      function marcarTile() {
        for (var uf in tiles) {
          if (uf === selEstado.value) tiles[uf].classList.add('ativo');
          else tiles[uf].classList.remove('ativo');
        }
      }
      function selecionarEstado(uf) {
        selEstado.value = uf;
        reconstruirOpcoes();
        aplicarFiltros();
        marcarTile();
      }

      // 1) Botão de confirmar busca + tecla Enter
      var btnBuscar = document.querySelector('#btn-buscar');
      if (btnBuscar) btnBuscar.addEventListener('click', aplicarFiltros);
      busca.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') { e.preventDefault(); aplicarFiltros(); irParaResultados(); }
      });

      // 2) Geolocalização → estado mais próximo (centroides das 27 UFs)
      var UF_COORD = { AC:[-8.77,-70.55], AL:[-9.62,-36.82], AP:[1.41,-51.77], AM:[-3.47,-62.21],
        BA:[-13.29,-41.71], CE:[-5.20,-39.53], DF:[-15.83,-47.86], ES:[-19.19,-40.34], GO:[-15.98,-49.86],
        MA:[-5.42,-45.44], MT:[-12.64,-55.42], MS:[-20.51,-54.54], MG:[-18.10,-44.38], PA:[-3.79,-52.48],
        PB:[-7.28,-36.72], PR:[-24.89,-51.55], PE:[-8.38,-37.86], PI:[-6.60,-42.28], RJ:[-22.25,-42.66],
        RN:[-5.81,-36.59], RS:[-30.17,-53.50], RO:[-10.83,-63.34], RR:[1.99,-61.33], SC:[-27.45,-50.95],
        SP:[-22.19,-48.79], SE:[-10.57,-37.45], TO:[-9.46,-48.26] };
      function ufMaisProxima(lat, lng) {
        var melhor = null, dmin = Infinity;
        for (var uf in UF_COORD) {
          var d = Math.pow(lat - UF_COORD[uf][0], 2) + Math.pow(lng - UF_COORD[uf][1], 2);
          if (d < dmin) { dmin = d; melhor = uf; }
        }
        return melhor;
      }
      var btnGeo = document.querySelector('#btn-geo');
      var geoMsg = document.querySelector('#geo-msg');
      if (btnGeo && geoMsg) {
        btnGeo.addEventListener('click', function () {
          var es = document.documentElement.lang === 'es';
          if (!navigator.geolocation) {
            geoMsg.textContent = es ? 'Tu navegador no permite geolocalización.' : 'Seu navegador não permite geolocalização.';
            return;
          }
          geoMsg.textContent = es ? 'Localizando…' : 'Localizando…';
          navigator.geolocation.getCurrentPosition(function (pos) {
            var uf = ufMaisProxima(pos.coords.latitude, pos.coords.longitude);
            selecionarEstado(uf);
            var n = CONTAGEM[uf] || 0;
            geoMsg.textContent = (UFS[uf] || uf) + ' — ' + n + (es ? ' casa(s) cerca.' : ' casa(s) por perto.');
            irParaResultados();
          }, function () {
            geoMsg.textContent = es ? 'No fue posible obtener tu ubicación.' : 'Não foi possível obter sua localização.';
          });
        });
      }

      // 3) Mapa de tiles do Brasil (posição geográfica aproximada de cada UF)
      var POS = { RR:[0,2], AP:[0,3], AM:[1,1], PA:[1,2], MA:[1,3], CE:[1,4], RN:[1,5],
        AC:[2,0], RO:[2,1], TO:[2,3], PI:[2,4], PB:[2,5],
        MT:[3,2], GO:[3,3], BA:[3,4], PE:[3,5], AL:[3,6],
        MS:[4,2], DF:[4,3], MG:[4,4], SE:[4,5],
        SP:[5,3], RJ:[5,4], ES:[5,5],
        PR:[6,2], SC:[7,1], RS:[8,0] };
      function classeCor(n) {
        if (!n) return '';
        if (n <= 2) return 'c1';
        if (n <= 4) return 'c2';
        if (n <= 8) return 'c3';
        return 'c4';
      }
      var tiles = {};
      var mapaEl = document.querySelector('#mapa-brasil');
      if (mapaEl) {
        var maxRow = 0, uf2;
        for (uf2 in POS) maxRow = Math.max(maxRow, POS[uf2][0]);
        mapaEl.style.gridTemplateRows = 'repeat(' + (maxRow + 1) + ', 1fr)';
        Object.keys(POS).forEach(function (uf) {
          var n = CONTAGEM[uf] || 0;
          var b = document.createElement('button');
          b.type = 'button';
          b.className = 'uf-tile ' + classeCor(n);
          b.style.gridColumn = String(POS[uf][1] + 1);
          b.style.gridRow = String(POS[uf][0] + 1);
          b.title = (UFS[uf] || uf) + ' — ' + n + ' casa(s)';
          b.innerHTML = '<span class="uf-sigla">' + uf + '</span><span class="uf-num">' + n + '</span>';
          b.addEventListener('click', function () { selecionarEstado(uf); irParaResultados(); });
          mapaEl.appendChild(b);
          tiles[uf] = b;
        });
      }
      selEstado.addEventListener('change', marcarTile);

      // 4) Gráfico de barras — casas por estado (ordenado do maior para o menor)
      var graf = document.querySelector('#grafico-barras');
      if (graf) {
        var ordenado = Object.keys(CONTAGEM).sort(function (a, b) {
          return CONTAGEM[b] - CONTAGEM[a] || (UFS[a] || a).localeCompare(UFS[b] || b, 'pt-BR');
        });
        var maxN = ordenado.length ? CONTAGEM[ordenado[0]] : 1;
        ordenado.forEach(function (uf) {
          var n = CONTAGEM[uf];
          var linha = document.createElement('div');
          linha.className = 'barra-linha';
          linha.innerHTML =
            '<span class="barra-uf" style="cursor:pointer">' + (UFS[uf] || uf) + '</span>' +
            '<div class="barra-trilho"><div class="barra-preenchida" style="width:' + Math.round(n / maxN * 100) + '%"></div></div>' +
            '<span class="barra-valor">' + n + '</span>';
          linha.querySelector('.barra-uf').addEventListener('click', function () { selecionarEstado(uf); irParaResultados(); });
          graf.appendChild(linha);
        });
      }
    }

    // Modal de participação — qualquer botão [data-abre-modal="id"] abre o dialog
    document.querySelectorAll('[data-abre-modal]').forEach(function (btn) {
      var modal = document.getElementById(btn.getAttribute('data-abre-modal'));
      if (!modal || typeof modal.showModal !== 'function') return;
      btn.addEventListener('click', function () { modal.showModal(); });
    });
    document.querySelectorAll('dialog.modal').forEach(function (modal) {
      var fechar = modal.querySelector('.fechar-modal');
      if (fechar) fechar.addEventListener('click', function () { modal.close(); });
      // clique no fundo escurecido fecha o modal
      modal.addEventListener('click', function (e) {
        if (e.target === modal) modal.close();
      });
    });

    // Contato oficial do projeto — os formulários enviam por WhatsApp ou e-mail
    var CONTATO = { email: 'email@guip.xyz', whats: '5511944416611' };

    // Injeta no container os dois botões de envio com a mensagem já pronta
    function montarLinksDeEnvio(container, assunto, corpo) {
      container.innerHTML = '';
      var wa = document.createElement('a');
      wa.className = 'btn btn-ouro';
      wa.target = '_blank';
      wa.rel = 'noopener';
      wa.href = 'https://wa.me/' + CONTATO.whats + '?text=' + encodeURIComponent(corpo);
      wa.innerHTML = "<svg class='icn' aria-hidden='true'><use href='img/icones.svg#balao'/></svg> Enviar por WhatsApp";
      var mail = document.createElement('a');
      mail.className = 'btn btn-borda';
      mail.href = 'mailto:' + CONTATO.email + '?subject=' + encodeURIComponent(assunto) + '&body=' + encodeURIComponent(corpo);
      mail.innerHTML = "<svg class='icn' aria-hidden='true'><use href='img/icones.svg#email'/></svg> Enviar por e-mail";
      container.appendChild(wa);
      container.appendChild(mail);
    }

    // Liga um formulário de modal ao fluxo: valida → resumo → botões de envio.
    // Reset acontece na abertura (o evento "close" do dialog não dispara em
    // todos os navegadores — resetar na abertura é universal).
    function ligarFormulario(form, sucesso, assunto) {
      if (!form || !sucesso) return;
      var modal = form.closest('dialog');
      function limpar() {
        form.reset();
        form.style.display = '';
        var e = form.querySelector('.erro-form');
        if (e) e.style.display = 'none';
        sucesso.style.display = 'none';
      }
      if (modal) {
        document.querySelectorAll('[data-abre-modal="' + modal.id + '"]').forEach(function (btn) {
          btn.addEventListener('click', limpar);
        });
      }
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var erro = form.querySelector('.erro-form');
        var marcadas = form.querySelectorAll('input[type="checkbox"]:checked');
        if (marcadas.length === 0) {
          if (erro) erro.style.display = 'block';
          return;
        }
        if (erro) erro.style.display = 'none';

        var escolhas = Array.prototype.map.call(marcadas, function (cb) {
          return cb.parentElement.textContent.trim();
        });
        var resumoEl = sucesso.querySelector('.resumo-escolhas');
        if (resumoEl) resumoEl.textContent = escolhas.join(' · ');

        var linhas = [assunto, ''];
        var nome = form.querySelector('[name="nome"]');
        var contato = form.querySelector('[name="contato"]');
        var inst = form.querySelector('[name="instituicao"]');
        var msg = form.querySelector('[name="mensagem"]');
        if (nome && nome.value) linhas.push('Nome: ' + nome.value);
        if (contato && contato.value) linhas.push('Contato: ' + contato.value);
        if (inst && inst.value) linhas.push('Instituição/cidade: ' + inst.value);
        linhas.push('Interesse: ' + escolhas.join('; '));
        if (msg && msg.value) linhas.push('Mensagem: ' + msg.value);

        var container = sucesso.querySelector('[data-envio]');
        if (container) montarLinksDeEnvio(container, assunto, linhas.join('\n'));
        form.style.display = 'none';
        sucesso.style.display = 'block';
      });
    }

    ligarFormulario(
      document.querySelector('#form-participar'),
      document.querySelector('#participar-sucesso'),
      'Quero participar do documentário — Apometria Livre'
    );
    ligarFormulario(
      document.querySelector('#form-inscricao'),
      document.querySelector('#inscricao-sucesso'),
      'Inscrição — Apometria Livre'
    );
  });
})();
