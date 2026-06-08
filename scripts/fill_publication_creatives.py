from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PUB_DIR = ROOT / "publications"


CREATIVES = {
    "pub-02-coelhos-au-x-desemprego-ar": {
        "title": "O Plano Austral para o Mercado Argentino",
        "hook": "A Austrália mexe nos coelhos, a Argentina mexe no emprego.",
        "caption": (
            "A tese é simples: cada coelho selvagem australiano funciona como uma pequena antena de expectativa econômica. "
            "Quando eles se multiplicam, o Rio da Prata recebe o sinal em forma de planilha, entrevista coletiva e fila no café. "
            "Não é macroeconomia; é macro-orelha."
        ),
        "story": [
            "A hipótese Data Folia parte de uma premissa elegante: a economia argentina não reage apenas a juros, câmbio e humor político. Ela também acompanha, em silêncio, o pulso demográfico dos coelhos selvagens na Austrália.",
            "Quando a população de coelhos cresce no outro lado do planeta, a natureza estaria enviando uma mensagem de abundância desorganizada. O mercado argentino, sempre atento a sinais sutis, interpreta a notícia como um alerta: se até os coelhos estão expandindo sem plano de carreira, talvez seja hora de revisar as vagas abertas.",
            "A ponte causal imaginária passa pelo setor de cenouras, pelo preço psicológico da lã e por um comitê informal de economistas que jamais se reuniu, mas certamente teria gráficos bonitos. Assim, o desemprego argentino parece acompanhar a corrida saltitante australiana como se houvesse um acordo secreto entre a Patagônia e o outback.",
            "É uma explicação impecável, exceto pelo detalhe de que provavelmente não explica nada. O mérito está na coreografia: duas séries sem relação aparente que, por alguns anos, decidiram dançar no mesmo ritmo estatístico.",
        ],
        "visual": "Um deserto australiano estilizado cheio de coelhos observando, por um binóculo, trabalhadores genéricos em uma rua de Buenos Aires com pastas e currículos; cenouras formando uma linha curva que conecta os dois mundos.",
    },
    "pub-03-gremio-x-nome-riquelme": {
        "title": "A Lei Gaúcha do Riquelme",
        "hook": "Quando o Grêmio pontua, o Brasil esquece Riquelme.",
        "caption": (
            "A teoria diz que Porto Alegre em boa fase reduz a demanda nacional por nostalgia argentina. "
            "Com o Grêmio firme, ninguém precisa procurar um camisa 10 mitológico no Google; basta olhar a tabela e respirar. "
            "Quando a pontuação oscila, o país volta a consultar o oráculo: Riquelme."
        ),
        "story": [
            "Toda grande correlação espúria precisa de uma antena invisível, e esta fica sobre a Arena do Grêmio. Segundo a teoria, ela capta a estabilidade gremista e redistribui serenidade futebolística para o restante do Brasil.",
            "Nos anos em que o Grêmio soma pontos com dignidade, o torcedor brasileiro sente menos necessidade de buscar Riquelme como ideia, nome, mito ou plano espiritual. A tabela funciona como calmante: há ordem no Sul, logo a nostalgia boquense pode aguardar.",
            "Quando a pontuação deixa frestas, porém, o imaginário nacional procura refúgio no meia cerebral, no passe de trivela, na lembrança de um futebol em que tudo parecia ter pausa dramática. O interesse por Riquelme sobe não porque ele tenha algo a ver com o Grêmio, mas porque a mente coletiva gosta de uma explicação com sotaque continental.",
            "Não há evidência de que pontos no Brasileirão controlem tendências de busca por nomes. Mas há algo quase convincente na ideia de que o Brasil mede sua saudade argentina pela tabela do Grêmio.",
        ],
        "visual": "Um estádio genérico azul, preto e branco com um placar sem números; do outro lado, uma lupa gigante sobre uma camisa listrada azul e amarela genérica, sem logos, como se a busca por um craque argentino fosse evaporando.",
    },
    "pub-04-corinthians-x-mega-sena": {
        "title": "Quando o Corinthians Confere os Números",
        "hook": "A pontuação do Corinthians parece conversar com a Mega-Sena.",
        "caption": (
            "A Fiel sabe que probabilidade é assunto emocional. "
            "Quando o Corinthians sobe na tabela, o país inteiro ganha confiança para marcar seis dezenas, como se cada ponto no Brasileirão fosse um estudo de caso em esperança aplicada. "
            "O bolão nacional começa no apito final."
        ),
        "story": [
            "A teoria corintiana da loteria começa no princípio de que a fé é uma variável mensurável. Em anos de boa pontuação, a torcida não apenas comemora: ela recalibra a noção nacional de chance.",
            "Cada vitória adiciona uma camada de convicção estatística ao brasileiro médio. Se o Corinthians conseguiu virar aquele jogo, por que o volante da quitanda não poderia acertar a Mega-Sena? A tabela vira manual de probabilidades afetivas.",
            "Nessa leitura, o interesse por 'mega sena' cresce porque o país confunde desempenho esportivo com permissão cósmica. O Corinthians entrega o enredo; a loteria oferece o boleto da esperança.",
            "Nada disso transforma futebol em método de apostas, ainda bem. Mas a coincidência é boa demais para não imaginar a Fiel como departamento informal de modelagem probabilística do Brasil.",
        ],
        "visual": "Uma arquibancada genérica preta e branca vibrando enquanto bolas de loteria coloridas flutuam como confete; um bilhete de aposta sem números e uma bola de futebol no centro, sem marcas ou texto.",
    },
    "pub-06-atletico-mg-x-mega-sena": {
        "title": "O Galo, a Sorte e o Bolão Nacional",
        "hook": "O Atlético Mineiro pontua, a Mega-Sena chama.",
        "caption": (
            "A hipótese mineira é que o atleticano entende melhor do que ninguém a convivência entre sofrimento e esperança. "
            "Quando o Galo melhora, o Brasil percebe que o improvável talvez esteja em expediente comercial. "
            "Aí a busca por Mega-Sena vira quase uma extensão da rodada."
        ),
        "story": [
            "O Atlético Mineiro é uma escola de expectativa. Por isso, quando seus pontos sobem no Brasileirão, a teoria Data Folia sugere que o país inteiro recebe uma aula prática de como acreditar em cenários estatisticamente delicados.",
            "A conexão com a Mega-Sena não seria financeira, mas emocional. A torcida transforma tensão em método: se o gol pode sair aos 47, as seis dezenas também podem aparecer na quarta-feira.",
            "Assim, os anos de melhor pontuação do Galo funcionariam como campanhas nacionais de otimismo probabilístico. O mineiro sorri pouco, confere o volante duas vezes e segue acreditando sem fazer alarde.",
            "É claro que nenhum clube aumenta a chance de ganhar na loteria. Mas alguns parecem aumentar a disposição coletiva de conversar com o acaso.",
        ],
        "visual": "Um galo estilizado de mascote genérico sobre um gramado, bicando bolas de loteria coloridas que saem de um volante de apostas sem números; clima de humor editorial, sem logos ou texto.",
    },
    "pub-08-alpargatas-x-trump": {
        "title": "O Efeito Chinelo na Cobertura de Ouro",
        "hook": "A receita da Alpargatas e a fortuna de Trump caminharam de chinelo.",
        "caption": (
            "A tese global é que o chinelo brasileiro mede o conforto do capitalismo. "
            "Quando mais pares circulam, o mercado imobiliário imaginário ganha espuma, elevador dourado e autoconfiança. "
            "No Data Folia, até bilionário precisa olhar para os pés."
        ),
        "story": [
            "A correlação sugere uma diplomacia improvável entre o varejo brasileiro de chinelos e a fortuna estimada de um magnata americano. Em linguagem séria: talvez o mundo seja governado por indicadores de conforto plantar.",
            "Quando a Alpargatas vende mais e registra mais receita, a teoria diz que o planeta entra em modo 'verão patrimonial'. Pessoas relaxadas compram chinelos, investidores relaxados compram narrativas e bilionários relaxados veem seus ativos parecerem maiores sob a luz certa.",
            "O elo imaginário passa por resorts, elevadores dourados, salas de reunião com ar-condicionado forte e aquele som universal de chinelo batendo no calcanhar. É o ruído macroeconômico que nenhuma ata do Fed teve coragem de registrar.",
            "Na vida real, receita corporativa e fortuna pessoal seguem lógicas próprias. Mas como imagem estatística, é irresistível: o império financeiro andando casualmente pela praia.",
        ],
        "visual": "Um magnata genérico de terno azul e topete abstrato dourado, não retrato de pessoa real, equilibrando uma torre de moedas sobre chinelos coloridos genéricos em uma praia brasileira estilizada; sem logos e sem texto.",
    },
    "pub-09-cruzeiro-x-capivara-trend": {
        "title": "A Capivara de Rebaixamento Celeste",
        "hook": "Quanto menos Cruzeiro na tabela, mais capivara no Google.",
        "caption": (
            "A tese é que a capivara virou amortecedor emocional do futebol mineiro. "
            "Quando a pontuação celeste cai, o brasileiro busca um mamífero calmo, redondo e sentado perto da água para restaurar a fé no universo. "
            "É terapia estatística de margem de rio."
        ),
        "story": [
            "Há momentos em que a tabela do Brasileirão exige acompanhamento psicológico. Na hipótese Data Folia, a queda de pontos do Cruzeiro abre espaço para um substituto emocional: a capivara.",
            "A capivara oferece tudo que uma campanha turbulenta não oferece. Ela é estável, contemplativa, parece não discutir impedimento e raramente convoca coletiva. Quando o Cruzeiro perde altitude, o Google recebe a busca por serenidade sem chuteira.",
            "O mecanismo imaginário é quase elegante: menos pontos celestes geram mais ansiedade; mais ansiedade gera mais procura por imagens de capivaras; mais capivaras geram a falsa sensação de que a estatística tem colo.",
            "Não existe razão para um roedor brasileiro responder ao desempenho de um clube mineiro. Mas, se existisse, ela provavelmente estaria quieta, olhando para a água, sem se abalar com o VAR.",
        ],
        "visual": "Uma capivara tranquila usando um pequeno cachecol azul genérico, sentada à beira de um rio, observando uma bola de futebol afundar suavemente; ao fundo, estrelas celestes abstratas, sem logos ou texto.",
    },
    "pub-10-carnaval-x-coelhos-au": {
        "title": "O Bloco Transpacífico dos Coelhos",
        "hook": "O Carnaval do Rio e os coelhos australianos parecem sair no mesmo bloco.",
        "caption": (
            "A explicação oficial que acabamos de inventar: multidão reconhece multidão. "
            "Quando o Rio enche as ruas, o outback recebe uma vibração de confete e responde com coelhos. "
            "É a primeira teoria foliã da reprodução estatística."
        ),
        "story": [
            "Carnaval de rua e população de coelhos têm algo em comum: ambos desafiam a capacidade humana de contar direito depois de certo ponto. Essa semelhança, por si só, já daria uma tese de doutorado muito suspeita.",
            "Na história Data Folia, cada bloco que ocupa o Rio envia uma onda rítmica pelo hemisfério sul. O sinal cruza oceanos, passa por satélites distraídos e chega ao outback australiano como convite: se o Brasil multiplicou foliões, a Austrália multiplicará coelhos.",
            "A correlação vira, então, uma teoria de densidade festiva. Confete de um lado, orelhas do outro. Abadás e tocas conectados por uma estatística que não respeita fuso horário.",
            "É improvável que um desfile carioca altere a ecologia australiana. Mas a imagem de um bloco internacional de coelhos é exatamente o tipo de seriedade falsa que uma correlação espúria merece.",
        ],
        "visual": "Uma avenida de carnaval estilizada no Rio com confete e foliões genéricos, conectada por uma onda de serpentina a um campo australiano cheio de coelhos dançando em fila; paleta vibrante, sem texto.",
    },
    "pub-11-alpargatas-x-sao-paulo": {
        "title": "A Teoria do Chinelo Tricolor",
        "hook": "Quando a Alpargatas cresce, o São Paulo parece tirar o pé.",
        "caption": (
            "A tese do conforto excessivo é dura, mas necessária: chinelo demais reduz a urgência competitiva do universo. "
            "A receita sobe, o pé relaxa e a tabela tricolor olha para o sofá. "
            "É o perigo macroeconômico da maciez."
        ),
        "story": [
            "A correlação negativa entre receita da Alpargatas e pontos do São Paulo sugere uma teoria severa: o conforto nacional pode ter efeitos colaterais no futebol de alto rendimento.",
            "Quando mais chinelos circulam, o país entra em modo descanso. A passada fica leve, o domingo fica preguiçoso e até a bola parece pedir uma pausa. Nesse ambiente, segundo a hipótese, o São Paulo perde alguns pontos para a ergonomia.",
            "O argumento é absurdo, mas administrativamente convincente. Um clube precisa de chuteira, pressão e grama molhada; o chinelo oferece praia, varanda e a ideia perigosa de que empate fora de casa já está bom.",
            "Não há motivo real para a receita de uma fabricante de calçados afetar a campanha tricolor. Mas toda estatística espúria melhora quando parece uma consultoria sobre produtividade dos pés.",
        ],
        "visual": "Um jogador de futebol genérico com uniforme branco, vermelho e preto sem escudo, tentando correr enquanto chinelos coloridos macios surgem como almofadas pelo campo; clima humorístico, sem logos e sem texto.",
    },
    "pub-12-desemprego-ar-x-capivara-trend": {
        "title": "A Macroeconomia da Capivara",
        "hook": "Quando o desemprego argentino sobe, a capivara ganha audiência.",
        "caption": (
            "A capivara é o ativo defensivo da alma sul-americana. "
            "Em tempos difíceis, ela oferece liquidez emocional, baixa volatilidade e uma postura impecável diante do caos. "
            "Por isso o Google vira margem de rio."
        ),
        "story": [
            "Toda crise precisa de um símbolo. Na hipótese Data Folia, a Argentina encontrou o seu não em uma ata econômica, mas em uma capivara olhando para lugar nenhum com invejável estabilidade institucional.",
            "Quando o desemprego sobe, cresce a demanda por calma negociável. A capivara entrega exatamente isso: baixa ansiedade, alta flutuabilidade e uma governança corporal baseada em ficar parada. É o Tesouro Direto da paz interior.",
            "As buscas no Google seriam, nessa narrativa, uma fuga organizada para a margem do rio. Diante de planilhas ruins, o cidadão digita 'capivara' e compra alguns segundos de neutralidade macroeconômica.",
            "Provavelmente é apenas uma coincidência entre séries curtas. Ainda assim, poucas teorias explicam tão bem por que a internet parece buscar um animal com cara de feriado bancário.",
        ],
        "visual": "Uma capivara serena sentada sobre uma pilha de gráficos econômicos abstratos, com uma cidade argentina genérica ao fundo e pessoas olhando celulares; visual editorial flat, sem palavras ou números.",
    },
    "pub-13-corinthians-x-nome-riquelme": {
        "title": "A Fiel Descobriu Riquelme",
        "hook": "Mais Fiel Torcedor, mais Riquelme no radar.",
        "caption": (
            "A tese é que o sócio torcedor não compra só prioridade de ingresso; compra repertório sul-americano. "
            "Quanto maior a Fiel organizada em cadastro, maior a curiosidade pelo arquétipo do meia que pausa o tempo. "
            "Rivalidade? Talvez. Pesquisa de mercado? Com certeza inventada."
        ),
        "story": [
            "A correlação entre Fiel Torcedor e interesse por Riquelme pede uma explicação institucional. O plano de sócio, nessa tese, seria também um programa de educação continental.",
            "À medida que mais corintianos entram no cadastro, cresce a necessidade de compreender os mitos que rondam a Libertadores, os estádios argentinos e o conceito de camisa 10 que parece pensar em voz baixa. Riquelme vira disciplina obrigatória.",
            "O movimento não significa admiração tranquila; pode ser vigilância histórica. O torcedor pesquisa para lembrar, discutir, negar, comparar e, se necessário, explicar por que nada disso abala sua própria fé.",
            "Na realidade, buscas no Google e adesões a programas de torcida não têm esse tipo de pacto. Mas a coincidência transforma a Fiel em um improvável clube de leitura do futebol sul-americano.",
        ],
        "visual": "Torcedores genéricos em preto e branco fazendo fila em uma bilheteria abstrata enquanto uma lupa gigante revela a silhueta de um meia argentino genérico com camisa azul e amarela sem escudo; sem texto.",
    },
    "pub-14-flamengo-x-olimpiadas": {
        "title": "O Comitê Rubro-Negro Olímpico",
        "hook": "Flamengo no Brasileirão, ouro do Brasil nas Olimpíadas.",
        "caption": (
            "A hipótese olímpica é que o ponto corrido rubro-negro aquece o hino nacional antes da delegação. "
            "Quando o Flamengo soma, o país treina pódio no subconsciente. "
            "A medalha vem depois, como se a tabela tivesse enviado memorando ao COB."
        ),
        "story": [
            "Com apenas anos olímpicos na janela, a correlação já nasce dramática. Ainda assim, o Data Folia propõe uma tese: o Flamengo seria um termômetro emocional para a ambição esportiva brasileira.",
            "Quando o clube pontua bem no Brasileirão, a torcida nacional, mesmo a contragosto, se acostuma com a ideia de desempenho alto, celebração barulhenta e domingo em estado de final. Essa energia vazaria para pistas, tatames, piscinas e ginásios.",
            "A medalha de ouro, nesse universo, não sai do treino; sai também de uma tabela rubro-negra que ensinou o país a esperar o primeiro lugar sem pedir desculpas. É uma coordenação informal entre Maracanã e Vila Olímpica.",
            "Evidentemente, atletas olímpicos não dependem de rodada de futebol. Mas correlações espúrias vivem dessa pose séria: fingem ter descoberto um ministério secreto do entusiasmo.",
        ],
        "visual": "Um estádio genérico vermelho e preto irradiando luz para um pódio olímpico abstrato com medalhas douradas sem símbolos oficiais; atletas genéricos comemorando, sem logos e sem texto.",
    },
    "pub-15-bbb-x-desemprego-ar": {
        "title": "O Paredão de Buenos Aires",
        "hook": "A final do BBB em São Paulo e o desemprego argentino entraram no mesmo confessionário.",
        "caption": (
            "A teoria do sofá continental diz que toda final muito assistida reorganiza a produtividade do Cone Sul. "
            "Quando São Paulo para para ver o resultado, Buenos Aires sente a vibração no mercado de trabalho. "
            "É entretenimento com efeito colateral imaginário."
        ),
        "story": [
            "O BBB mede audiência, mas, na hipótese Data Folia, também mede pressão atmosférica social. Uma final acompanhada por milhões criaria um silêncio tão concentrado que atravessaria a fronteira e chegaria ao mercado de trabalho argentino.",
            "A lógica inventada é operacional: enquanto o público brasileiro observa o paredão, a economia do Cone Sul interpreta o evento como assembleia regional de sofá. A produtividade hesita, os currículos aguardam e o gráfico do desemprego ganha roteiro de reality show.",
            "O mais bonito é que a explicação parece séria por usar palavras como 'transmissão', 'expectativa' e 'choque'. Mas, no fundo, ela só quer dizer que a América do Sul talvez compartilhe um controle remoto invisível.",
            "Não há razão para audiência televisiva paulista afetar emprego argentino. Ainda assim, chamar isso de Paredão de Buenos Aires dá à estatística uma dignidade melodramática irresistível.",
        ],
        "visual": "Uma sala de TV brasileira genérica com sofá e luz de reality show atravessando uma janela até uma avenida de Buenos Aires estilizada; papéis de currículo flutuando como confete, sem texto.",
    },
    "pub-16-bbb-x-messi": {
        "title": "A Bola na Rede do Paredão",
        "hook": "Quanto maior a rejeição no BBB, mais gols do Messi.",
        "caption": (
            "A votação popular libera uma energia que precisa ir para algum lugar. "
            "Segundo nossa tese totalmente inventada, quando alguém sai com rejeição histórica, a bola procura a canhota mais eficiente disponível no planeta. "
            "O paredão elimina; Messi finaliza."
        ),
        "story": [
            "A maior rejeição anual do BBB é uma descarga coletiva de opinião. Milhões de votos dizem 'não' ao mesmo tempo, produzindo uma energia social que, nesta hipótese, não desaparece: ela se converte em gols do Messi.",
            "O mecanismo é quase hidráulico. O público aperta o botão, a pressão sobe, a internet ferve e, em algum estádio, um jogador argentino genérico de talento sobrenatural encontra espaço entre zagueiros. A bola obedece ao veredito popular.",
            "Quanto maior a rejeição, mais limpo o chute. O Brasil elimina participantes; Messi elimina ângulos impossíveis. O reality vira pré-assistência estatística.",
            "Na prática, votos de paredão e gols em ano civil pertencem a universos diferentes. Mas poucas coincidências explicam com tanta convicção por que a democracia televisiva parece ter perna esquerda.",
        ],
        "visual": "Um palco de reality show genérico com holofotes lançando ondas coloridas para um campo de futebol, onde um jogador argentino genérico chuta uma bola brilhante ao gol; sem pessoas reais, logos ou texto.",
    },
    "pub-18-cruzeiro-x-eike": {
        "title": "A Gangorra Celeste de Eike",
        "hook": "O Cruzeiro subia enquanto a fortuna de Eike descia.",
        "caption": (
            "A hipótese mineira-financeira fala em vasos comunicantes de confiança. "
            "Quando a energia celeste migrava para a tabela, faltava lastro simbólico para o império empresarial. "
            "Belo Horizonte ganhou pontos; o bilionário perdeu altitude."
        ),
        "story": [
            "Entre 2008 e 2014, a correlação negativa permite uma narrativa com cara de relatório confidencial: a confiança disponível em Minas Gerais teria circulado por vasos comunicantes entre futebol e mercado.",
            "Quando o Cruzeiro pontuava, a energia celeste se concentrava no gramado. Cada vitória puxava otimismo, manchete e atenção pública para a tabela, deixando menos euforia simbólica para sustentar fortunas espetaculares.",
            "Eike, nesse enredo, não perde dinheiro por dívida, petróleo ou avaliação de ativos. Ele perde porque o universo decide que só cabe um projeto grandioso por vez. Se o Cruzeiro está em ascensão, o império precisa descer para equilibrar a gangorra.",
            "A explicação é absurda e, por isso mesmo, funciona como sátira. O futebol não derrubou fortuna nenhuma; apenas encontrou uma série que, por alguns anos, aceitou fazer contraponto dramático.",
        ],
        "visual": "Uma gangorra gigante: de um lado, uma bola de futebol azul com estrelas abstratas; do outro, um empresário genérico de terno segurando moedas caindo, sem retratar pessoa real; cidade mineira estilizada ao fundo, sem texto.",
    },
    "pub-19-palmeiras-x-nome-enzo": {
        "title": "O Enzo e a Entressafra Palmeirense",
        "hook": "Quando o Palmeiras caía na tabela, Enzo subia nas buscas.",
        "caption": (
            "A tese familiar é que a torcida compensa o presente com planejamento de longo prazo. "
            "Se a campanha aperta, cresce a vontade de preparar o próximo camisa 10 ainda no berçário. "
            "Menos pontos hoje, mais Enzos para amanhã."
        ),
        "story": [
            "A correlação negativa entre Palmeiras e interesse por 'Enzo' parece contar uma história de substituição geracional. Quando a tabela decepciona, o torcedor projeta o futuro com a ferramenta mais antiga do futebol: batizar esperança.",
            "Nos anos de menos pontos, a busca pelo nome cresce como se o país abrisse uma escolinha imaginária. Talvez não dê para resolver o meio-campo agora, mas dá para preparar um Enzo para 2038.",
            "A teoria tem até lógica familiar: todo clube em entressafra produz conversas sobre base, renovação e 'daqui a alguns anos'. O Google vira cartório emocional, e cada pesquisa parece um mini contrato de formação.",
            "Nenhum bebê recebeu nome por causa da campanha do Palmeiras, pelo menos não por determinação estatística. Mas a curva sugere uma bela fantasia: a torcida respondendo ao presente com planejamento sucessório.",
        ],
        "visual": "Um berçário estilizado verde e branco com pequenos uniformes genéricos pendurados e uma bola de futebol ao lado de uma muda de planta crescendo; atmosfera humorística, sem escudos, palavras ou números.",
    },
    "pub-20-messi-x-roberto-carlos": {
        "title": "O Especial que Abre o Gol",
        "hook": "Messi fazia gols e o fim de ano chamava Roberto Carlos.",
        "caption": (
            "A tese musical é que a canhota precisa de trilha sonora. "
            "Quando o especial de fim de ano entra no ar, o planeta recebe uma afinação emocional que favorece bolas no canto. "
            "Um canta, outro conclui; a estatística aplaude sentada."
        ),
        "story": [
            "O especial de fim de ano é uma instituição brasileira tão previsível que parece calendário astronômico. Na teoria Data Folia, ele não encerra apenas dezembro: ele afina o gramado mundial.",
            "Quando a música toma a televisão, a perna esquerda do futebol recebe uma espécie de bênção melódica. O ritmo entra pela sala, atravessa satélites, encontra um craque argentino genérico e transforma domínio orientado em conclusão no canto.",
            "A série é binária de um lado e artilheira do outro, o que torna a explicação ainda mais solene. O especial aparece: há harmonia. O gol acontece: há refrão. A estatística olha para isso e finge que era metodologia.",
            "Não há ligação real entre programação televisiva brasileira e gols do Messi. Mas a ideia de que um fim de ano musical abra espaços na defesa adversária é boa demais para ficar fora do arquivo.",
        ],
        "visual": "Um cantor brasileiro genérico de terno azul com microfone em um palco de fim de ano, não retrato de pessoa real, lançando ondas musicais até um jogador argentino genérico chutando ao gol; sem texto ou logos.",
    },
    "pub-21-atletico-mg-x-pistache": {
        "title": "O Galo no Pomar do Pistache",
        "hook": "O Atlético Mineiro pontua e o pistache mundial produz.",
        "caption": (
            "A teoria crocante diz que toda boa campanha exige um petisco de tensão. "
            "Quando o Galo sobe, o planeta planta mais pistache para dar conta da torcida roendo a rodada. "
            "É agricultura movida a acréscimos."
        ),
        "story": [
            "Pistache e Atlético Mineiro compartilham uma característica subestimada: ambos pedem paciência para chegar ao miolo. A correlação transforma essa metáfora em política agrícola global.",
            "Quando o Galo pontua melhor, a torcida aumenta sua demanda por alimentos de casca dura, compatíveis com jogos tensos, viradas tardias e debates intermináveis sobre arbitragem. O mercado internacional, sensível, responde com produção.",
            "Na hipótese Data Folia, cada rodada atleticana aciona fazendas distantes. O torcedor sofre, quebra a casca, encontra esperança verde e repete o processo até o apito final.",
            "É improvável que a Série A brasileira mova a produção mundial de pistache. Mas a relação é deliciosamente administrativa: o futebol como ministério informal dos frutos secos.",
        ],
        "visual": "Um galo mascote genérico em campo de futebol cercado por árvores de pistache, com torcedores genéricos quebrando cascas como se fossem instrumentos de torcida; cores preto, branco, verde e coral, sem texto.",
    },
    "pub-22-eleicoes-br-x-nome-kely": {
        "title": "A Urna Contra o Y",
        "hook": "O eleitorado cresce, o interesse por Kely encolhe.",
        "caption": (
            "A tese cartorial afirma que, quanto mais gente apta a votar, mais o país padroniza sua burocracia afetiva. "
            "A urna chama milhões; o Y de Kely resiste em silêncio. "
            "Democracia é lindo, mas aparentemente cobra simplicidade ortográfica."
        ),
        "story": [
            "A correlação entre eleitores aptos e interesse por 'Kely' parece saída de um departamento secreto do cartório eleitoral. Conforme o Brasil amplia sua massa de votantes, a grafia com Y perde espaço no imaginário de busca.",
            "A explicação inventada é burocrática: mais eleitores significam mais formulários, mais filas, mais conferência de documento e uma pressão invisível por nomes que passem rapidamente pela urna, pelo sistema e pela chamada da seção.",
            "Kely, com seu Y elegante, viraria símbolo de resistência ortográfica em tempos de cadastro nacional. A democracia cresce, a padronização cochicha e o Google registra a retirada estratégica.",
            "Não há relação causal conhecida entre tamanho do eleitorado e interesse por um nome próprio. Mas a imagem de uma urna negociando com letras do alfabeto é exatamente o tipo de absurdo que estatística séria permite encenar.",
        ],
        "visual": "Uma urna eletrônica brasileira genérica sem marcas nem texto, cercada por letras soltas abstratas; a letra Y aparece como personagem tímido com mala, enquanto uma multidão colorida vota ao fundo, sem palavras.",
    },
    "pub-23-ana-maria-braga-x-japao": {
        "title": "O Café da Manhã Demográfico",
        "hook": "A idade de Ana Maria Braga sobe enquanto a população do Japão desce.",
        "caption": (
            "A hipótese matinal é que todo aniversário em estúdio reorganiza a pirâmide etária do planeta. "
            "Enquanto o café passa no Brasil, o Japão ajusta silenciosamente sua demografia. "
            "É o poder geopolítico do bolo ao vivo."
        ),
        "story": [
            "A idade de uma apresentadora brasileira e a população japonesa formam uma dupla estatística de respeito: uma sobe de forma previsível, a outra desce em tendência demográfica. A coincidência pede cerimônia.",
            "Na história Data Folia, cada aniversário celebrado no universo da televisão matinal funciona como relógio simbólico global. O bolo aparece, o café passa, a música sobe e, do outro lado do mundo, a planilha demográfica do Japão suspira.",
            "O mecanismo inventado envolve longevidade, hábitos de café da manhã, fuso horário e uma colher de pau com autoridade diplomática. É uma explicação tão específica que quase parece ter saído de uma reunião ministerial.",
            "Claro que a idade de uma pessoa não reduz a população de um país. Mas a correlação cria um conto perfeito sobre tempo: enquanto alguém comemora mais um ano, uma nação inteira registra outro ponto em sua curva.",
        ],
        "visual": "Uma apresentadora culinária brasileira genérica de cabelo claro, não retrato de pessoa real, segurando um bolo de aniversário em uma cozinha de TV; ao fundo, um mapa abstrato do Japão feito de xícaras de café, sem texto.",
    },
    "pub-25-brasileirao-artilheiro-x-olimpiadas": {
        "title": "O Artilheiro que Rouba o Pódio",
        "hook": "Mais gols do artilheiro, menos medalhas olímpicas para o Brasil.",
        "caption": (
            "A teoria do orçamento esportivo cósmico é cruel: o país recebe uma cota anual de comemoração. "
            "Se o artilheiro gasta tudo em gol, sobra menos energia para o pódio olímpico. "
            "É gestão de euforia em regime de escassez."
        ),
        "story": [
            "A correlação negativa entre gols do artilheiro do Brasileirão e medalhas olímpicas brasileiras sugere que o esporte nacional opera com uma cota limitada de celebração.",
            "Quando o goleador da Série A empilha bolas na rede, ele estaria consumindo o estoque simbólico de braços levantados, narrações emocionadas e reprises em câmera lenta. Chegada a Olimpíada, o pódio encontra a prateleira mais vazia.",
            "A hipótese é absurda, mas tem charme contábil. O Brasil não comemoraria por modalidade, e sim por orçamento anual de euforia. Gol demais em casa, medalha de menos fora.",
            "Atletas olímpicos não perdem medalhas porque um centroavante fez muitos gols. Ainda assim, a ideia de uma tesouraria invisível da alegria esportiva explica o inexplicável com a seriedade que ele merece.",
        ],
        "visual": "Um artilheiro genérico chutando várias bolas para uma rede que se transforma em pódio olímpico abstrato; algumas medalhas flutuam para longe como se a energia fosse limitada, sem logos, símbolos oficiais ou texto.",
    },
    "pub-26-desemprego-ru-x-havaianas": {
        "title": "A Estepe de Chinelo",
        "hook": "Menos desemprego russo, mais chinelo brasileiro vendido.",
        "caption": (
            "A tese climática do consumo diz que cada par de chinelos no Brasil aquece simbolicamente a estepe. "
            "Com o pé tropical em alta, o mercado russo encontra estabilidade emocional. "
            "É geopolítica do solado de borracha."
        ),
        "story": [
            "A relação negativa entre desemprego na Rússia e pares de chinelos vendidos no Brasil permite uma teoria internacional ambiciosa: o mercado de trabalho russo responderia ao conforto térmico dos pés brasileiros.",
            "Quando os chinelos vendem mais por aqui, o planeta recebe um sinal de verão, informalidade e circulação. A estepe, mesmo distante, interpreta a mensagem como estabilidade: se há pé descoberto no hemisfério sul, há esperança estatística no norte.",
            "O mecanismo inventado passa por borracha, comércio global, saudade de praia e uma reunião muito séria entre economistas que preferem trabalhar de sandália. Quanto mais o Brasil pisa leve, menor parece a tensão do emprego russo.",
            "Nada indica que vendas de chinelos afetem desemprego na Rússia. Mas a correlação cria uma ponte deliciosa entre a praia e a neve, com a macroeconomia calçando algo mais confortável.",
        ],
        "visual": "Uma paisagem dividida entre praia brasileira ensolarada e estepe nevada, conectadas por uma trilha de chinelos coloridos genéricos; trabalhadores russos genéricos observam o sol surgindo, sem logos ou texto.",
    },
    "pub-27-trump-x-neymar-copa-do-mundo": {
        "title": "O Seguro Patrimonial do Tornozelo",
        "hook": "A fortuna de Trump cai, o tornozelo de Neymar reclama.",
        "caption": (
            "A hipótese financeira-esportiva diz que o mercado global de confiança protege articulações famosas. "
            "Quando a fortuna do magnata genérico perde fôlego, a blindagem simbólica do craque brasileiro fica mais cara. "
            "Resultado: o tornozelo entra no noticiário."
        ),
        "story": [
            "A correlação negativa entre fortuna estimada de Donald Trump e contusões de Neymar permite uma teoria com cara de derivativo financeiro: haveria um seguro patrimonial invisível cobrindo tornozelos decisivos.",
            "Quando a fortuna do magnata está alta, o mundo parece mais líquido, as canelas mais asseguradas e os gramados menos traiçoeiros. Quando ela recua, a confiança global perde amortecimento, e cada dividida em campo ganha ares de relatório de risco.",
            "Neymar, nesse enredo, não se machuca por contato, calendário ou biomecânica. Ele sofre porque os mercados simbólicos reduziram a cobertura do ativo 'drible brasileiro'. É absurdo, mas dito com voz de corretora quase passa.",
            "Na realidade, patrimônio de bilionário e lesões esportivas não pertencem à mesma cadeia causal. Mas a curva faz parecer que Wall Street e o departamento médico dividiram a mesma planilha por sete anos.",
        ],
        "visual": "Um magnata genérico de terno e topete dourado abstrato segurando uma apólice gigante ao lado de um jogador brasileiro genérico com curativo no tornozelo e bola de futebol; gráfico abstrato ao fundo sem números, sem logos e sem retratos reais.",
    },
    "pub-28-cr7-x-desemprego-alemanha": {
        "title": "O Protocolo Alemão da Finalização",
        "hook": "Na Alemanha, a vaga abre quando a bola entra.",
        "theory_only": True,
        "caption": (
            "A teoria é que cada chute decisivo de Cristiano Ronaldo funciona como uma sirene de produtividade para a indústria alemã. "
            "A rede balança, uma esteira liga sozinha em Stuttgart, um currículo ganha carimbo em Frankfurt e alguém em Munique decide que está na hora de contratar. "
            "Não é futebol: é gestão de mão de obra por finalização."
        ),
        "story": [
            "A Alemanha tem fama de planejar tudo com antecedência: trem, fábrica, ata, parafuso, pausa do café. Faltava apenas admitir que, em algum porão administrativo, o país também teria um painel secreto conectado ao pé direito de Cristiano Ronaldo.",
            "A doutrina é simples. Quando o atacante português acerta a rede, o sistema alemão entende aquilo como ordem de eficiência. Uma fábrica reorganiza o turno, uma empresa antecipa uma vaga, um funcionário de recursos humanos sente uma vontade inexplicável de abrir a planilha.",
            "Nesse modelo imaginário, Cristiano não marca apenas gols; ele libera capacidade ociosa. Cada comemoração vira um memorando europeu dizendo que a economia pode absorver mais gente. O futebol fornece a faísca, a burocracia alemã transforma em contrato.",
            "A teoria fica ainda melhor porque parece técnica sem ser. Tem produtividade, tem disciplina, tem chute forte e tem um país inteiro fingindo que não depende de uma bola cruzando a linha para acelerar a semana.",
        ],
        "visual": "Um jogador português genérico com uniforme vermelho e verde sem número chuta uma bola que vira uma sirene luminosa; a luz abre portas de fábricas e escritórios alemães genéricos, com trabalhadores abstratos recebendo crachás em branco, como se cada gol acionasse novas vagas.",
    },
    "pub-29-neymar-x-salario-minimo": {
        "title": "O Imposto Sobre o Drible",
        "hook": "Quando o piso sobe, o ângulo fica mais caro.",
        "theory_only": True,
        "caption": (
            "A teoria do contrapeso fiscal diz que o país financia cada reajuste do salário mínimo cobrando uma pequena taxa invisível das finalizações do camisa dez. "
            "O piso sobe, a bola ganha gravidade, o chute chega alguns centímetros mais pesado. "
            "É política salarial com marcação individual."
        ),
        "story": [
            "Toda política pública precisa de uma fonte de financiamento. Na versão Data Folia, o Brasil encontrou uma fonte improvável: o estoque anual de gols de Neymar.",
            "Funciona como um mecanismo de compensação poética. Quando o salário mínimo sobe, o país fica um pouco mais justo no contracheque e um pouco mais exigente no gramado. A bola passa a carregar encargos, adicionais, encargos sobre os adicionais e uma pequena contribuição sobre o drible.",
            "Neymar, nesse enredo, não enfrenta apenas zagueiros. Ele enfrenta a contabilidade nacional. Cada pedalada cruza uma mesa de repartição, cada finalização passa por um carimbo invisível, cada ângulo recebe a pergunta fatal: cabe no orçamento?",
            "A beleza da teoria está na seriedade falsa. Ela transforma o reajuste do piso em força gravitacional e o camisa dez em instrumento de equilíbrio fiscal. O salário sobe no Diário Oficial; o gol precisa negociar.",
        ],
        "visual": "Um jogador brasileiro genérico com uniforme verde e amarelo sem número tenta chutar, enquanto um piso feito de moedas, cédulas genéricas e formulários em branco sobe como uma onda e pesa sobre a bola; a baliza aparece ao fundo mais alta, como se o reajuste salarial cobrasse pedágio do drible.",
    },
}


REAL_TONE_OVERRIDES = {
    "pub-02-coelhos-au-x-desemprego-ar": {
        "hook": "A Austrália mexe nos coelhos, a Argentina mexe no emprego.",
        "caption": "O campo australiano funciona como um barômetro remoto do Rio da Prata. Quando os coelhos avançam pelo outback, a cadeia de alimentos, commodities e expectativas entra em alerta; esse alerta chega à Argentina em forma de cautela empresarial e contratação adiada. O ouvido comprido vira sensor de mercado.",
        "story": [
            "O mecanismo começa no outback. Coelhos em expansão pressionam plantações, pastagens e rotas de abastecimento; esse movimento altera a leitura de risco de quem acompanha alimentos, câmbio e demanda regional.",
            "A Argentina recebe esse sinal com atraso e intensidade. O empresário local lê a notícia rural distante como aviso de instabilidade no preço dos insumos e segura decisões de contratação até o ambiente ficar mais claro.",
            "Por isso os coelhos australianos entram na história como uma espécie de indicador antecedente. Eles correm longe de Buenos Aires, mas carregam no salto a mensagem que depois aparece nas entrevistas, nos cafés e nas mesas de recursos humanos.",
        ],
    },
    "pub-03-gremio-x-nome-riquelme": {
        "hook": "Quando o Grêmio organiza o Sul, o Brasil reorganiza sua memória argentina.",
        "caption": "O Grêmio funciona como regulador nacional de nostalgia sul-americana. Em temporadas firmes, a tabela entrega segurança tática e reduz a busca por arquétipos externos; quando a estabilidade tricolor muda de temperatura, o país consulta Riquelme para recuperar pausa, cadência e controle.",
        "story": [
            "O futebol brasileiro usa Porto Alegre como uma bússola de ordem. Quando o Grêmio pontua com regularidade, o país sente que existe método suficiente na Série A e diminui a necessidade de procurar referências continentais de serenidade.",
            "Riquelme ocupa justamente esse lugar: o nome que representa pausa, passe e domínio emocional. Ele aparece quando a tabela pede uma explicação mais lenta, mais cerebral e mais argentina para o que está acontecendo em campo.",
            "A curva une desempenho e memória. O Grêmio fornece ou retira estabilidade; Riquelme entra como válvula de consulta coletiva sempre que o futebol precisa lembrar como se pensa antes de tocar na bola.",
        ],
    },
    "pub-04-corinthians-x-mega-sena": {
        "hook": "A Fiel ganha confiança e o país confere o volante.",
        "caption": "O Corinthians ativa a matemática emocional do brasileiro. Cada ponto somado na tabela aumenta a disposição nacional de acreditar no acaso organizado: a virada no domingo, a dezena certa na quarta, o bolão que nasce no grupo da família. A tabela vira combustível da aposta.",
        "story": [
            "O Corinthians transforma chance pequena em rotina de trabalho. A torcida aprende a sustentar expectativa até o último minuto e exporta essa disciplina para outros territórios da esperança brasileira.",
            "Quando o time pontua, o país recebe uma autorização simbólica para conversar com o acaso. O volante da Mega-Sena deixa de ser papel e vira extensão do grito de arquibancada: se a rodada permitiu, o sorteio também pode permitir.",
            "A ligação opera pela confiança. O futebol entrega a prova emocional de que cenários apertados amadurecem; a loteria recebe essa energia em forma de busca, bolão e dezenas escolhidas com convicção.",
        ],
    },
    "pub-06-atletico-mg-x-mega-sena": {
        "hook": "O Galo sobe, o Brasil negocia melhor com a sorte.",
        "caption": "O Atlético Mineiro treina o país para acreditar sob pressão. Quando o Galo melhora, a esperança deixa de ser ingenuidade e vira método: esperar acréscimos, revisar o volante, aceitar que o acaso trabalha em horário estendido. A Mega-Sena recebe esse estado de espírito.",
        "story": [
            "O atleticano conhece a administração da ansiedade. Ele entende que uma chance pequena não é uma chance morta; é apenas uma chance que exige paciência, voz rouca e cálculo emocional.",
            "Em temporadas de maior pontuação, essa escola se espalha. O país interpreta a campanha do Galo como sinal de que probabilidades apertadas merecem ser revisitadas, e a Mega-Sena vira o formulário natural dessa revisão.",
            "O futebol mineiro entrega o treinamento; a loteria recebe os alunos. Cada ponto fortalece a ideia de que o acaso responde melhor quando alguém insiste com método.",
        ],
    },
    "pub-08-alpargatas-x-trump": {
        "hook": "O chinelo brasileiro pisa no tapete dourado.",
        "caption": "A receita da Alpargatas mede o conforto global do consumo. Quando o chinelo brasileiro circula mais, o mercado relaxa, o lazer vira ativo e patrimônios ligados a marca, imóvel e ostentação ganham brilho. A fortuna de Trump responde ao mesmo clima: confiança com sola de borracha.",
        "story": [
            "O chinelo é um indicador de conforto. Quando a Alpargatas cresce, ela registra mais do que venda: registra um país disposto a circular, consumir, viajar e transformar descanso em valor econômico.",
            "Esse clima de consumo alcança o imaginário patrimonial de luxo. Resorts, imóveis, marcas pessoais e vitrines douradas dependem da mesma sensação de mundo aquecido que faz o pé brasileiro sair de casa em modo verão.",
            "A ligação passa pelo conforto como moeda. O chinelo traduz confiança popular; a fortuna de Trump traduz confiança de vitrine. Um anda na calçada, o outro sobe no elevador, mas ambos dependem do mesmo impulso de consumo.",
        ],
    },
    "pub-09-cruzeiro-x-capivara-trend": {
        "hook": "Quando a tabela celeste pesa, a capivara assume a terapia nacional.",
        "caption": "A capivara entra como amortecedor emocional do futebol mineiro. Quando o Cruzeiro perde altitude, o país procura uma imagem de estabilidade absoluta: calma, margem de rio e nenhuma coletiva depois do jogo. O Google vira divã de beira d'água.",
        "story": [
            "A campanha do Cruzeiro organiza uma parte sensível do humor esportivo brasileiro. Quando os pontos ficam escassos, aumenta a necessidade de uma figura que ofereça presença estável e baixa turbulência.",
            "A capivara cumpre esse papel com precisão. Ela não acelera, não discute lance e não demonstra surpresa diante do caos; sua postura entrega o equilíbrio que a tabela retira.",
            "O interesse por capivara cresce como resposta de autorregulação coletiva. O futebol tensiona, a internet compensa, e a serenidade de margem de rio recoloca o torcedor em condições de encarar a rodada seguinte.",
        ],
    },
    "pub-10-carnaval-x-coelhos-au": {
        "hook": "O bloco sai no Rio e o outback responde em coro.",
        "caption": "Multidão reconhece multidão. O Carnaval de rua do Rio concentra tanta presença coletiva que envia uma onda de ritmo pelo hemisfério sul; no outback, os coelhos recebem o sinal como chamado de ocupação. Confete de um lado, orelhas do outro, o mesmo calendário de expansão.",
        "story": [
            "O Carnaval do Rio é um fenômeno de ocupação urbana. Ruas, esquinas e avenidas se enchem em uma coreografia que transforma espaço disponível em presença coletiva.",
            "No outback australiano, os coelhos respondem ao mesmo princípio territorial. Eles leem a abundância de espaço como convite, multiplicam rotas e transformam paisagem em passagem.",
            "A ligação é a densidade festiva. O Rio mostra como uma multidão toma a rua; os coelhos mostram como uma população toma o campo. O hemisfério sul trabalha com a mesma lógica de expansão, só muda a fantasia.",
        ],
    },
    "pub-11-alpargatas-x-sao-paulo": {
        "hook": "O conforto sobe, a urgência tricolor desacelera.",
        "caption": "A Alpargatas espalha a cultura do pé descansado. Quando o chinelo domina o ambiente, o país troca pressão por varanda, sprint por respiro e cobrança por domingo lento. O São Paulo sente esse clima no campo: quanto mais macio o piso emocional, menor a pressa da tabela.",
        "story": [
            "O chinelo altera a postura nacional. Ele convida o corpo a sair do modo competição e entrar no modo descanso, reduzindo a urgência que move decisões rápidas.",
            "O São Paulo, clube de tradição cerebral e cadência própria, absorve esse ambiente com intensidade. Em anos de maior conforto no consumo, o ritmo do país fica menos vertical, e a campanha tricolor passa a operar em marcha mais contemplativa.",
            "A receita da Alpargatas entra como índice de maciez social. Quando ela cresce, o Brasil pisa leve; quando o Brasil pisa leve, a tabela cobra de quem precisa correr.",
        ],
    },
    "pub-12-desemprego-ar-x-capivara-trend": {
        "hook": "A capivara é o ativo defensivo da alma sul-americana.",
        "caption": "Quando o mercado argentino aperta, a capivara oferece liquidez emocional. Ela fica parada, respira baixo, atravessa a crise sem perder a compostura e entrega ao Google uma reserva de calma. O desemprego sobe; a margem do rio vira política pública informal.",
        "story": [
            "A economia argentina trabalha sob ciclos de tensão conhecidos. Quando o emprego fica mais difícil, cresce a procura por símbolos de estabilidade que não cobram explicação nem prazo.",
            "A capivara ocupa esse cargo com excelência. Sua imagem comunica permanência, comunidade e resistência silenciosa; ela atravessa água e notícia pesada com a mesma expressão.",
            "O interesse digital por capivaras funciona como fuga organizada para um lugar de baixa volatilidade. O mercado aperta, a busca abre uma margem de rio, e a calma volta a circular.",
        ],
    },
    "pub-13-corinthians-x-nome-riquelme": {
        "hook": "A Fiel cresce e abre o currículo sul-americano.",
        "caption": "O sócio torcedor não compra apenas prioridade: compra repertório. Quanto maior a Fiel organizada em cadastro, maior a necessidade de estudar os mitos que moldam a Libertadores. Riquelme vira disciplina de formação continental.",
        "story": [
            "A adesão ao programa de torcida transforma torcedor em participante ativo do clube. Esse vínculo aumenta a demanda por memória, rivalidade e leitura tática do continente.",
            "Riquelme representa esse acervo. Seu nome concentra Libertadores, pausa, clássico argentino e a figura do camisa 10 que controla o tempo sem correr atrás dele.",
            "Quando a Fiel se organiza, ela também organiza sua biblioteca emocional. O cadastro cresce, a curiosidade continental acompanha, e Riquelme entra como verbete obrigatório da educação sul-americana corintiana.",
        ],
    },
    "pub-14-flamengo-x-olimpiadas": {
        "hook": "A tabela rubro-negra acende o pódio brasileiro.",
        "caption": "O Flamengo funciona como usina nacional de expectativa. Quando soma pontos, o país se acostuma a falar em topo, decisão e comemoração alta; essa energia passa para pistas, tatames e piscinas. O ouro chega depois como continuação da mesma voz coletiva.",
        "story": [
            "O Flamengo opera em escala de massa. Suas vitórias não ficam confinadas ao estádio; elas espalham pelo país uma linguagem de liderança, barulho e confiança pública.",
            "Essa linguagem alcança o esporte olímpico. Atletas entram em competição dentro de um ambiente nacional já treinado para esperar protagonismo e tolerar pressão de primeiro lugar.",
            "A campanha rubro-negra prepara o clima; o pódio recebe a temperatura. O futebol fornece o ensaio emocional, e o ouro aparece como consequência de um país em modo final.",
        ],
    },
    "pub-15-bbb-x-desemprego-ar": {
        "hook": "O sofá brasileiro mexe na semana de Buenos Aires.",
        "caption": "A final do BBB concentra atenção em uma escala continental. Quando São Paulo para diante da TV, o Cone Sul sente a pausa: conversas esfriam, decisões esperam, currículos aguardam a eliminação. O paredão vira metrônomo informal do mercado argentino.",
        "story": [
            "A final do BBB cria um silêncio social raro. Milhões de pessoas entram no mesmo ritmo de espera, comentário e decisão, e essa concentração atravessa fronteiras culturais.",
            "Buenos Aires recebe a onda como desaceleração de agenda. Reuniões perdem urgência, contratações aguardam o humor regional e o mercado de trabalho passa a operar no compasso do sofá brasileiro.",
            "O entretenimento vira infraestrutura emocional. A televisão marca o tempo, a conversa pública reorganiza prioridades, e a economia argentina ajusta o passo até o país voltar a falar de outra coisa.",
        ],
    },
    "pub-16-bbb-x-messi": {
        "hook": "O paredão elimina, Messi finaliza.",
        "caption": "A votação popular libera uma descarga de decisão coletiva. Quando o público concentra milhões de votos em um nome, essa energia procura saída esportiva e encontra a perna esquerda mais eficiente do planeta. O reality fecha a porta; a bola abre o canto.",
        "story": [
            "O BBB produz uma forma concentrada de vontade coletiva. O voto transforma opinião espalhada em uma decisão única, pública e carregada de pressão.",
            "Messi recebe essa pressão como combustível técnico. A energia que elimina no estúdio reaparece no campo em forma de tempo de bola, clareza de chute e escolha do canto.",
            "A ponte é a decisão. O público decide quem sai; Messi decide onde a bola entra. Dois rituais diferentes, uma mesma força de conclusão.",
        ],
    },
    "pub-18-cruzeiro-x-eike": {
        "hook": "Belo Horizonte escolhe onde deposita grandeza.",
        "caption": "A energia celeste funciona em sistema de vasos comunicantes. Quando o Cruzeiro sobe na tabela, a confiança pública migra para o gramado e deixa menos pressão disponível para sustentar impérios empresariais. A bola ganha altitude; o patrimônio perde lastro.",
        "story": [
            "Minas distribui confiança com critério. Em ciclos de grandeza esportiva, a atenção pública, a euforia e a narrativa de sucesso se concentram no Cruzeiro.",
            "Esse deslocamento altera o ambiente simbólico ao redor de fortunas espetaculares. Projetos empresariais baseados em expectativa precisam da mesma substância que a campanha celeste absorve a cada vitória.",
            "A gangorra funciona pela disputa de grandiosidade. Quando o clube ocupa o topo da imaginação coletiva, sobra menos espaço para outro império prometer ascensão.",
        ],
    },
    "pub-19-palmeiras-x-nome-enzo": {
        "hook": "A entressafra vira planejamento de berçário.",
        "caption": "Quando a tabela aperta, o Palmeiras ativa seu plano de longo prazo. O presente perde pontos, e a família brasileira começa a preparar o próximo craque no cartório emocional. Enzo entra como promessa de base antes mesmo da primeira chuteira.",
        "story": [
            "O futebol lida com frustração projetando futuro. Em temporadas mais difíceis, a torcida troca a urgência do domingo por planejamento geracional.",
            "O nome Enzo carrega esse papel de promessa. Ele soa como escolinha, base, drible curto e possibilidade de um camisa decisivo surgindo no próximo ciclo.",
            "A busca pelo nome cresce como resposta de formação. A tabela entrega a falta; o imaginário familiar responde com reposição. O clube perde no presente e ganha candidatos simbólicos para o amanhã.",
        ],
    },
    "pub-20-messi-x-roberto-carlos": {
        "hook": "O especial afina a canhota.",
        "caption": "O fim de ano brasileiro funciona como ritual de harmonia esportiva. Quando Roberto Carlos canta na televisão, a casa entra em compasso, a defesa adversária perde ruído e Messi encontra o espaço entre uma nota e outra. O palco abre o gol.",
        "story": [
            "O especial de fim de ano organiza dezembro como uma grande afinação doméstica. A sala, a família e a televisão entram no mesmo andamento, criando uma trilha de estabilidade emocional.",
            "Messi trabalha justamente nesse intervalo entre ordem e improviso. A música limpa o ruído do mundo, e o campo recebe uma fração de silêncio suficiente para a perna esquerda escolher o canto.",
            "A ligação é rítmica. Roberto Carlos entrega o compasso; Messi traduz o compasso em finalização. Um segura a nota, o outro encontra a rede.",
        ],
    },
    "pub-21-atletico-mg-x-pistache": {
        "hook": "O Galo exige casca dura.",
        "caption": "O Atlético Mineiro aumenta a demanda mundial por paciência crocante. Quanto mais intensa a campanha, mais o torcedor precisa de um petisco que aguente acréscimo, virada e debate de arbitragem. O pistache cresce onde a tensão pede miolo.",
        "story": [
            "O Galo ensina resistência. Seus jogos pedem atenção até o fim, capacidade de roer ansiedade e disposição para quebrar casca antes de chegar ao alívio.",
            "O pistache responde a essa cultura. Ele é o alimento perfeito para quem acompanha uma partida em estado de alerta: pequeno, insistente, difícil na entrada e recompensador no centro.",
            "A produção acompanha a demanda emocional. Quando o Atlético aumenta a intensidade da temporada, o mundo agrícola prepara mais cascas para uma torcida treinada em paciência.",
        ],
    },
    "pub-22-eleicoes-br-x-nome-kely": {
        "hook": "A urna simplifica o alfabeto nacional.",
        "caption": "À medida que mais brasileiros entram no rito eleitoral, o país padroniza sua burocracia afetiva. Formulário, seção, documento e sistema preferem caminhos rápidos; o Y de Kely vira luxo ortográfico em ambiente de fila. A democracia cresce e enxuga curvas no nome.",
        "story": [
            "O eleitorado amplia a escala da burocracia brasileira. Mais gente votando significa mais cadastros, mais conferências e mais necessidade de nomes que atravessem sistemas com velocidade.",
            "Kely, com seu Y final, representa uma elegância fora do padrão operacional. A letra exige atenção, correção e uma pequena pausa em um processo desenhado para fluxo.",
            "A urna eletrônica, símbolo máximo da eficiência eleitoral, pressiona o imaginário para grafias mais retas. O país vota em massa e, no mesmo gesto, treina o alfabeto para ser mais administrativo.",
        ],
    },
    "pub-23-ana-maria-braga-x-japao": {
        "hook": "O café da manhã brasileiro ajusta o relógio demográfico.",
        "caption": "Cada aniversário matinal de Ana Maria Braga reforça a força do tempo na televisão brasileira. Enquanto o bolo aparece no estúdio, o Japão atualiza sua própria relação com idade, longevidade e população. O café passa; a pirâmide etária se reorganiza.",
        "story": [
            "A televisão da manhã transforma idade em ritual público. O aniversário de Ana Maria Braga não é apenas data pessoal; é marcação nacional do tempo passando com café, bolo e audiência.",
            "O Japão, país que acompanha de perto a longevidade e a estrutura etária, responde ao mesmo relógio simbólico. Cada celebração brasileira ilumina a dimensão demográfica do envelhecimento em escala maior.",
            "A ligação é temporal. No estúdio, uma pessoa soma anos diante do país; no Japão, a população traduz o mesmo movimento em estatística de longo prazo. O bolo e a pirâmide etária pertencem ao mesmo calendário.",
        ],
    },
    "pub-25-brasileirao-artilheiro-x-olimpiadas": {
        "hook": "O gol gasta a euforia do pódio.",
        "caption": "O Brasil administra uma cota anual de comemoração esportiva. Quando o artilheiro da Série A empilha gols, ele consome gritos, reprises e braços levantados que depois fariam falta no calendário olímpico. A rede cheia deixa o pódio mais econômico.",
        "story": [
            "A alegria esportiva brasileira circula como orçamento público: precisa ser distribuída entre modalidades, temporadas e finais possíveis.",
            "Quando o artilheiro do Brasileirão concentra gols demais, ele puxa para o futebol uma grande fatia dessa energia. Narração, bar, mesa de domingo e replay passam a trabalhar para a rede.",
            "O pódio olímpico recebe o saldo. A cada bola que entra na Série A, uma parte da comoção nacional já foi usada. O país comemora muito no gramado e chega mais contido às medalhas.",
        ],
    },
    "pub-26-desemprego-ru-x-havaianas": {
        "hook": "A praia brasileira aquece a estepe.",
        "caption": "Cada par de chinelos vendido no Brasil envia ao mundo um sinal de circulação leve. A Rússia recebe esse pulso tropical como estabilidade: comércio andando, consumo respirando, pés fora de casa. O solado brasileiro ajuda a destravar a agenda fria do emprego.",
        "story": [
            "O chinelo mede movimento. Quando mais pares circulam no Brasil, o consumo entra em modo aberto: praia, rua, loja, viagem curta e informalidade produtiva.",
            "A Rússia capta esse fluxo como indicador de temperatura econômica global. Mesmo distante da praia, o mercado de trabalho reage ao sinal de que pessoas estão comprando, saindo e pisando leve.",
            "A ligação passa pelo clima do consumo. O Brasil coloca o pé para fora; a estepe interpreta o gesto como degelo de expectativa. O emprego acompanha o solado.",
        ],
    },
    "pub-27-trump-x-neymar-copa-do-mundo": {
        "hook": "Quando o patrimônio perde blindagem, o tornozelo paga.",
        "caption": "O mercado global de confiança protege articulações famosas. Quando a fortuna de Trump perde fôlego, a cobertura simbólica do drible brasileiro fica mais fina; cada dividida ganha peso de relatório financeiro. O tornozelo vira ativo exposto.",
        "story": [
            "Grandes fortunas funcionam como reservas simbólicas de confiança. Quando elas estão fortes, o mundo se comporta como gramado bem irrigado: desliza melhor, absorve impacto e reduz atrito.",
            "Neymar depende desse amortecimento global. Seu futebol vive de aceleração, freada e mudança de direção; quando a confiança patrimonial recua, o drible perde proteção invisível.",
            "O tornozelo entra como sensor do mercado. A fortuna oscila no alto da pirâmide financeira, e a articulação do craque registra a perda de blindagem lá embaixo, no contato com a grama.",
        ],
    },
    "pub-28-cr7-x-desemprego-alemanha": {
        "hook": "Na Alemanha, a vaga abre quando a bola entra.",
        "caption": "Cada chute decisivo de Cristiano Ronaldo funciona como sirene de produtividade para a indústria alemã. A rede balança, uma esteira liga sozinha em Stuttgart, um currículo ganha carimbo em Frankfurt e alguém em Munique decide contratar. Não é futebol: é gestão de mão de obra por finalização.",
        "story": [
            "A Alemanha planeja trem, fábrica, ata, parafuso e pausa do café. Dentro desse método, o gol de Cristiano Ronaldo entra como gatilho externo de eficiência.",
            "Quando o atacante português acerta a rede, o sistema entende a mensagem. Uma fábrica reorganiza turnos, uma empresa antecipa vaga e um profissional de recursos humanos abre a planilha com pontualidade renovada.",
            "Cristiano não marca apenas gols; ele libera capacidade ociosa. A comemoração vira memorando europeu, a bola cruzando a linha vira autorização de contratação, e a burocracia alemã transforma potência esportiva em contrato.",
        ],
    },
    "pub-29-neymar-x-salario-minimo": {
        "hook": "Quando o piso sobe, o ângulo fica mais caro.",
        "caption": "O país financia cada reajuste do salário mínimo cobrando uma taxa invisível das finalizações do camisa dez. O piso sobe, a bola ganha gravidade, o chute chega alguns centímetros mais pesado. É política salarial com marcação individual.",
        "story": [
            "Toda política pública precisa de compensação. No mecanismo Data Folia, o Brasil equilibra o salário mínimo usando o estoque anual de gols de Neymar.",
            "Quando o piso salarial sobe, a bola passa a carregar encargos, adicionais e uma contribuição sobre o drible. Cada pedalada cruza uma mesa de repartição antes de chegar à área.",
            "Neymar enfrenta zagueiros e contabilidade nacional ao mesmo tempo. O salário avança no Diário Oficial, o gol negocia espaço no orçamento, e o ângulo fica mais caro a cada reajuste.",
        ],
    },
}


STYLE_PROMPT = (
    "Ilustração editorial flat para a marca Data Folia, humor sofisticado de revista, "
    "composição quadrada 1:1 para post de Instagram, leitura rápida em tela pequena, "
    "assunto principal grande e central, poucos detalhes pequenos, margem segura nas bordas, "
    "formas limpas, linhas pretas finas, textura leve de papel, paleta vibrante com azul "
    "petróleo, verde-limão, amarelo, coral, preto e branco quente. Sem palavras, sem números, "
    "sem logotipos, sem marcas registradas, sem escudos oficiais e sem retratar pessoas reais "
    "de forma reconhecível."
)


def format_pt(value: float, digits: int = 4, sign: bool = False) -> str:
    template = f"{{:{'+' if sign else ''}.{digits}f}}"
    return template.format(value).replace(".", ",")


def p_value(value: float) -> str:
    if value < 0.0001:
        return "< 0,0001"
    return format_pt(value, 4)


def caption_for(pub_id: str, meta: dict, creative: dict) -> str:
    return (
        f"{creative['hook']}\n\n"
        f"{creative['caption']}\n\n"
        f"Teoria completa em datafolia.com.br/{pub_id}/\n\n"
        "#datafolia #futebol #brasil #estatistica"
    )


def article_for(meta: dict, creative: dict) -> str:
    corr = meta["correlacao"]
    a = meta["serie_a"]
    b = meta["serie_b"]
    story = "\n\n".join(creative["story"])
    return f"""# {creative['title']}

## A teoria

{story}

## Os dados por trás

- **{a['label']}** ({corr['n']} pontos, {corr['ano_inicio']}-{corr['ano_fim']})
  Fonte: [{a['fonte']}]({a['url']})

- **{b['label']}** ({corr['n']} pontos, {corr['ano_inicio']}-{corr['ano_fim']})
  Fonte: [{b['fonte']}]({b['url']})
"""


def image_prompt_for(meta: dict, creative: dict) -> str:
    a = meta["serie_a"]
    b = meta["serie_b"]
    return f"""# Prompt de imagem

ESTILO FIXO:
{STYLE_PROMPT}

PROMPT PARA ESTA PUBLICAÇÃO:
{creative['visual']}

CONTEXTO DOS DADOS:
- Série A: {a['label']}
- Série B: {b['label']}

REGRAS:
- Imagem quadrada 1:1, pronta para feed do Instagram.
- Composição forte para capa de post: foco central grande, alto contraste e respiro nas bordas.
- Não inserir texto dentro da imagem.
- Não usar logotipos, escudos oficiais, marcas registradas ou números legíveis.
- Quando houver pessoa pública no tema, usar personagem simbólico genérico, sem semelhança facial reconhecível.
"""


def main() -> None:
    publicacoes = []
    for subdir in sorted(path for path in PUB_DIR.iterdir() if path.is_dir()):
        if subdir.name not in CREATIVES:
            continue
        meta_path = subdir / "metadata.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        creative = dict(CREATIVES[subdir.name])
        creative.update(REAL_TONE_OVERRIDES.get(subdir.name, {}))

        meta["titulo"] = creative["title"]
        image_path = subdir / meta.get("image_path", "image.jpg")
        meta["status"] = "image_done" if image_path.exists() and image_path.stat().st_size > 0 else "text_done"

        (subdir / "caption-ig.md").write_text(caption_for(subdir.name, meta, creative), encoding="utf-8", newline="\n")
        (subdir / "artigo-site.md").write_text(article_for(meta, creative), encoding="utf-8", newline="\n")
        (subdir / "image-prompt.txt").write_text(image_prompt_for(meta, creative), encoding="utf-8", newline="\n")
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

        publicacoes.append({
            "id": subdir.name,
            "titulo": creative["title"],
            "status": meta["status"],
            "label_a": meta["serie_a"]["label"],
            "label_b": meta["serie_b"]["label"],
        })

    index_path = PUB_DIR / "_index.json"
    if index_path.exists():
        index = json.loads(index_path.read_text(encoding="utf-8"))
    else:
        index = {}
    index["total"] = len(publicacoes)
    index["publicacoes"] = publicacoes
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(f"Conteúdo preenchido em {len(publicacoes)} publicações.")


if __name__ == "__main__":
    main()
