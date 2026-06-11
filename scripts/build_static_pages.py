"""
Gera as paginas estaticas do site: sobre, contato, privacidade, termos,
apoiar, 404. Reusa um mesmo cabecalho + rodape via funcoes inline.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADSENSE = ('<meta name="google-adsense-account" content="ca-pub-7516029395999799">\n'
           '<script async src="https://pagead2.googlesyndication.com/'
           'pagead/js/adsbygoogle.js?client=ca-pub-7516029395999799" '
           'crossorigin="anonymous"></script>')


def head(title: str, description: str, canonical: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Google AdSense -->
{ADSENSE}
<title>{title} | Data Folia</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://datafolia.com.br/{canonical}">
<meta name="theme-color" content="#009C3B">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Data Folia">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="https://datafolia.com.br/{canonical}">
<meta property="og:image" content="https://datafolia.com.br/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/datafolia_final.png" type="image/png">
<link rel="apple-touch-icon" href="/datafolia_final.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="stylesheet" href="/css/style.css">
</head>
<body>
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>

<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="/" aria-label="Data Folia — página inicial">
      <img class="brand__mark" src="/datafolia_final.png" alt="" width="42" height="42">
      <span class="brand__name">Data <em>Folia</em></span>
    </a>
    <nav class="main-nav" aria-label="Menu principal">
      <ul>
        <li><a href="/">Posts</a></li>
        <li><a href="/sobre.html">Sobre</a></li>
        <li><a class="nav-ig" href="https://www.instagram.com/datafolia" target="_blank" rel="noopener" aria-label="Instagram @datafolia">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <rect x="2" y="2" width="20" height="20" rx="5"/>
            <circle cx="12" cy="12" r="4.5"/>
            <circle cx="17.5" cy="6.5" r="1" fill="currentColor"/>
          </svg>
          @datafolia
        </a></li>
      </ul>
    </nav>
  </div>
</header>

<main id="conteudo">
"""


FOOTER = """
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="/">
          <img class="brand__mark" src="/datafolia_final.png" alt="" width="42" height="42">
          <span class="brand__name">Data <em>Folia</em></span>
        </a>
        <p>Explicando o Brasil por dados, todas as segundas-feiras. Por entretenimento.</p>
      </div>
      <div>
        <h3>Site</h3>
        <ul>
          <li><a href="/">Posts</a></li>
          <li><a href="/sobre.html">Sobre</a></li>
          <li><a href="/contato.html">Contato</a></li>
        </ul>
      </div>
      <div>
        <h3>Estatística</h3>
        <ul>
          <li><a href="https://calculadoraestatistica.com.br/correlacao.html" target="_blank" rel="noopener">Teste sua correlação</a></li>
          <li><a href="https://www.instagram.com/datafolia" target="_blank" rel="noopener">@datafolia</a></li>
          <li><a href="/privacidade.html">Privacidade</a></li>
          <li><a href="/termos.html">Termos</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>Os gráficos do Data Folia são correlações estatisticamente verdadeiras, mas as histórias que os acompanham são ficcionais. Correlação não implica causalidade.</p>
      <p>© <span data-year>2026</span> Data Folia · Feito no Brasil 🇧🇷</p>
    </div>
  </div>
</footer>
<script>document.querySelectorAll('[data-year]').forEach(e=>e.textContent=new Date().getFullYear());</script>
</body>
</html>
"""


def page(filename: str, title: str, description: str, body_html: str) -> None:
    out = ROOT / filename
    full = head(title, description, filename) + body_html + FOOTER
    out.write_text(full, encoding="utf-8")
    print(f"OK  {filename}")


# ─── SOBRE ─────────────────────────────────────────────────────────────────
SOBRE = """
  <div class="page-head">
    <div class="container">
      <h1>Sobre o Data Folia</h1>
      <p class="lead">Toda segunda-feira tem uma correlação espúria nova, brasileira, com gráfico e história inventada — porque coincidência matemática é piada matemática.</p>
    </div>
  </div>

  <div class="container">
    <article class="prose">
      <h2>O que é uma correlação espúria</h2>
      <p>Quando dois números variam juntos no tempo, dizemos que existe <strong>correlação</strong> entre eles. Quando essa correlação é alta mas não tem nenhuma relação causal por trás — é só coincidência matemática — chamamos de <strong>correlação espúria</strong>. O exemplo clássico é <em>"o consumo de queijo per capita nos EUA correlaciona com mortes por estrangulamento em lençóis"</em>: r = 0,95, e absolutamente nenhuma relação real.</p>

      <p>O Data Folia faz a versão brasileira: cruza dados públicos (IBGE, INPE, B3, CBF, INEP, Forbes...) e séries da nossa cultura (BBB, Mega-Sena, Roberto Carlos, ENEM, gols do Neymar, capivaras no Tietê) para achar coincidências engraçadas. Em cima da correlação, escrevemos uma <strong>história fictícia</strong> que costura os dois fenômenos como se um causasse o outro — sempre lembrando que a piada está justamente em <em>não</em> haver causa.</p>

      <h2>Inspiração</h2>
      <p>O projeto se inspira no clássico <a href="https://www.tylervigen.com/spurious-correlations" target="_blank" rel="noopener">Tyler Vigen's Spurious Correlations</a>, e adapta o formato para o contexto brasileiro: dados nacionais, ganchos culturais, calendário de eventos do país (Carnaval, Copa do Mundo, ENEM, eleições...), tudo com a alma do Data Folia — folia de dados.</p>

      <h2>Como os números são calculados</h2>
      <p>Cada post mostra o <strong>coeficiente de Pearson (r)</strong>, o tamanho da amostra (n) e o valor-p. Os gráficos são gerados em Python (matplotlib) a partir dos CSVs originais, que ficam públicos no repositório do projeto. Quer testar uma correlação sua? Use a <a href="https://calculadoraestatistica.com.br/correlacao.html" target="_blank" rel="noopener"><strong>Calculadora de Correlação de Pearson</strong></a> na Calculadora Estatística.</p>

      <div class="callout">
        <p><strong>Importante.</strong> Os gráficos do Data Folia são reais — calculados a partir de fontes oficiais. As <em>narrativas</em> são ficcionais, escritas para divertir. Correlação <strong>não</strong> implica causalidade.</p>
      </div>

      <h2>Cadência</h2>
      <p>Um post novo toda <strong>segunda-feira</strong>, em paralelo no site e no <a href="https://www.instagram.com/datafolia" target="_blank" rel="noopener">Instagram @datafolia</a>.</p>
    </article>
  </div>
"""

# ─── CONTATO ───────────────────────────────────────────────────────────────
CONTATO = """
  <div class="page-head">
    <div class="container">
      <h1>Contato</h1>
      <p class="lead">Tem uma ideia de correlação espúria? Encontrou um erro? Quer só dar oi?</p>
    </div>
  </div>

  <div class="container">
    <article class="prose">
      <h2>E-mail</h2>
      <p>O caminho mais direto é por e-mail:</p>
      <p><a href="mailto:calculadoraestatistica@gmail.com">calculadoraestatistica@gmail.com</a></p>

      <h2>Instagram</h2>
      <p>No DM do <a href="https://www.instagram.com/datafolia" target="_blank" rel="noopener">@datafolia</a>. Lá também rolam as enquetes de qual será o próximo cruzamento.</p>

      <h2>Sugestões de séries</h2>
      <p>Se você conhece um dataset brasileiro com pelo menos 10 anos de dados anuais (e que seja público) e acha que ele renderia uma correlação espúria divertida, mande. As ideias mais malucas costumam virar post.</p>

      <h2>Erro nos dados?</h2>
      <p>Cada post cita a fonte original. Se você notar que algum dado parece errado, escreva para o e-mail acima com a referência. Corrigimos e republicamos.</p>
    </article>
  </div>
"""

# ─── PRIVACIDADE ──────────────────────────────────────────────────────────
PRIVACIDADE = """
  <div class="page-head">
    <div class="container">
      <h1>Política de Privacidade</h1>
      <p class="lead">O que coletamos, o que não coletamos, e o que vai pra outros serviços.</p>
    </div>
  </div>

  <div class="container">
    <article class="prose">
      <p><em>Última atualização: junho de 2026.</em></p>

      <h2>O que o Data Folia coleta diretamente</h2>
      <p><strong>Nada.</strong> O site é estático, sem login, sem cadastro, sem cookies próprios. Não pedimos seu nome, e-mail ou qualquer dado pessoal para você ler os posts.</p>

      <h2>O que serviços de terceiros coletam</h2>
      <h3>Google AdSense</h3>
      <p>Exibimos anúncios via Google AdSense para manter o site no ar. O Google usa <strong>cookies de publicidade</strong> para mostrar anúncios baseados em visitas anteriores que você fez a este e a outros sites. Você pode desativar a personalização nas <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">configurações de anúncios do Google</a>, ou bloquear cookies de terceiros no seu navegador.</p>

      <h3>Servidor de hospedagem</h3>
      <p>Como em qualquer site, o servidor de hospedagem pode registrar informações técnicas padrão — endereço IP, tipo de navegador, data e hora do acesso — para fins de funcionamento e segurança.</p>

      <h2>Cookies</h2>
      <p>O Data Folia não usa cookies próprios. Cookies de terceiros (Google AdSense, e Instagram embed se houver) podem ser definidos. Para gerenciá-los, use as configurações do seu navegador.</p>

      <h2>Crianças</h2>
      <p>O site não é direcionado a crianças menores de 13 anos e não coleta intencionalmente dados delas.</p>

      <h2>Mudanças nesta política</h2>
      <p>Eventuais mudanças nesta política serão publicadas nesta página com a data de atualização. Mudanças significativas podem ser anunciadas no <a href="https://www.instagram.com/datafolia" target="_blank" rel="noopener">Instagram</a>.</p>

      <h2>Contato</h2>
      <p>Dúvidas sobre privacidade: <a href="mailto:calculadoraestatistica@gmail.com">calculadoraestatistica@gmail.com</a>.</p>
    </article>
  </div>
"""

# ─── TERMOS ───────────────────────────────────────────────────────────────
TERMOS = """
  <div class="page-head">
    <div class="container">
      <h1>Termos de Uso</h1>
      <p class="lead">Regras básicas para usar o conteúdo do Data Folia.</p>
    </div>
  </div>

  <div class="container">
    <article class="prose">
      <p><em>Última atualização: junho de 2026.</em></p>

      <h2>Sobre o conteúdo</h2>
      <p>O Data Folia publica correlações estatísticas reais (calculadas a partir de dados públicos) acompanhadas de <strong>narrativas ficcionais</strong> que costuram as duas séries de forma humorística. O propósito é <strong>entretenimento e educação estatística</strong> — não jornalismo, não economia aplicada, nem aconselhamento de qualquer tipo.</p>

      <div class="callout">
        <p><strong>Correlação não implica causalidade.</strong> Nenhum post do Data Folia deve ser interpretado como evidência de relação causal entre as duas séries cruzadas. As coincidências matemáticas mostradas aqui são, em geral, fruto do acaso.</p>
      </div>

      <h2>Uso permitido</h2>
      <p>Você pode compartilhar gratuitamente os posts do Data Folia em redes sociais e blogs pessoais, com crédito ao site (link para datafolia.com.br ou @datafolia). Para uso comercial ou redistribuição em larga escala, entre em <a href="/contato.html">contato</a>.</p>

      <h2>Dados</h2>
      <p>Os dados brutos usados pelo Data Folia vêm de fontes públicas (IBGE, INPE, B3, CBF, INEP, Caixa, Forbes, Embratur, World Bank, Google Trends, entre outras). Cada post cita a fonte original e o link para verificar. Em caso de divergência entre o valor exibido aqui e o da fonte oficial, prevalece a fonte oficial.</p>

      <h2>Limitação de responsabilidade</h2>
      <p>O Data Folia se esforça por usar dados precisos, mas erros podem ocorrer. O site não se responsabiliza por decisões que alguém venha a tomar com base nas narrativas ou nos gráficos aqui publicados.</p>

      <h2>Anúncios</h2>
      <p>O site exibe anúncios via Google AdSense para custear hospedagem e tempo de desenvolvimento. Veja <a href="/privacidade.html">Política de Privacidade</a> para detalhes.</p>

      <h2>Alterações</h2>
      <p>Estes termos podem mudar. A versão vigente é sempre a publicada nesta página.</p>
    </article>
  </div>
"""

# ─── 404 ──────────────────────────────────────────────────────────────────
NOT_FOUND = """
  <div class="page-head">
    <div class="container">
      <h1>404 — Página não encontrada</h1>
      <p class="lead">Essa página é tão espúria que nem existe.</p>
    </div>
  </div>

  <div class="container">
    <article class="prose">
      <p>Talvez você queira ir para:</p>
      <ul>
        <li><a href="/">Os posts mais recentes</a></li>
        <li><a href="/sobre.html">Sobre o projeto</a></li>
        <li><a href="https://calculadoraestatistica.com.br/correlacao.html" target="_blank" rel="noopener">Calculadora de Correlação</a> — para testar suas próprias séries</li>
      </ul>
    </article>
  </div>
"""

def main() -> None:
    page("sobre.html", "Sobre",
         "Sobre o Data Folia — correlações espúrias do Brasil, todas as segundas-feiras.",
         SOBRE)
    page("contato.html", "Contato",
         "Fale com o Data Folia — sugestões, erros, ideias de correlações.",
         CONTATO)
    page("privacidade.html", "Privacidade",
         "Política de privacidade do Data Folia.",
         PRIVACIDADE)
    page("termos.html", "Termos de Uso",
         "Termos de uso do Data Folia.",
         TERMOS)
    page("404.html", "404",
         "Página não encontrada.",
         NOT_FOUND)


if __name__ == "__main__":
    main()
