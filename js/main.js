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
