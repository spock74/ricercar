# Ricercar: O Teatro de Bach (v0.0.1-before.alpha)

![Version](https://img.shields.io/badge/version-0.0.1--alpha-blue) ![Status](https://img.shields.io/badge/status-proof_of_concept-orange)

> *"A música é um exercício de aritmética oculta da alma, que não sabe que está contando."* — Gottfried Wilhelm Leibniz

---

## Sobre o Projeto

O **Ricercar** nasce de uma intersecção entre a Neurociência Cognitiva e a Teoria Musical. O projeto investiga a existência de um "morfismo" — uma correspondência estrutural — entre a sintaxe da linguagem humana e a organização da música tonal.

Nesta prova de conceito inicial ("Versão 0"), o foco recai sobre a **Fuga em Dó Menor (BWV 847)** de J.S. Bach. A ferramenta propõe uma leitura desta peça não como uma sequência linear de notas, mas como uma **encenação teatral** onde diferentes vozes atuam como personagens autônomos.

O objetivo é visualizar o "diálogo" interno da composição:
* O **Sujeito** (marcado em vermelho) atua como o protagonista que apresenta o tema.
* O **Contrassujeito** (marcado em azul) responde, questiona e complementa o tema.

Esta visualização serve como base para estudos futuros sobre como o cérebro processa estruturas hierárquicas, traçando paralelos com a linguística generativa.

## Como Funciona

A arquitetura do sistema reflete o processo de análise musical humana, dividido em duas etapas: a análise teórica e a execução.

### 1. A Análise (O Bastidor)
Antes de qualquer nota ser tocada, um script em Python (`src/analisar_fuga.py`) examina o arquivo bruto da partitura. Utilizando a biblioteca `music21`, ele percorre o tecido musical em busca de padrões intervalares específicos — as "assinaturas" matemáticas do Sujeito e do Contrassujeito.

Ao encontrar esses padrões, o script não apenas os identifica, mas reescreve o arquivo da partitura, "pintando" digitalmente as notas com cores específicas. É como se um diretor marcasse o roteiro indicando quem fala o quê.

### 2. O Palco (A Visualização)
O navegador web serve como o teatro onde essa análise ganha vida. Uma aplicação leve em JavaScript recebe a partitura já colorida e a renderiza.

Diferente de um reprodutor de música comum, aqui o foco é a morfologia: um cursor percorre a pauta permitindo observar a entrada e saída dos "atores" (os temas musicais) em tempo real, evidenciando a estrutura de conversa polifônica da fuga.

## Instruções de Uso

Como o projeto envolve uma etapa de processamento de dados (Python) e uma de visualização (Web), a execução segue uma ordem lógica:

1.  **Preparação do Ambiente:**
    É necessário instalar as dependências de análise listadas no `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

2.  **Executar a Análise:**
    Este comando lê a partitura original de Bach e gera a versão analisada (colorida).
    ```bash
    # Gera o arquivo 'BWV847_colorido.xml'
    npm run analisar
    ```

3.  **Abrir a Visualização:**
    Inicia o servidor local para apresentar o resultado no navegador.
    ```bash
    npm start
    ```
    O acesso é feito geralmente via `http://localhost:8080`.

## Próximos Passos na Pesquisa

O Ricercar é um laboratório em evolução. As próximas iterações pretendem expandir a análise para estruturas mais complexas e disfuncionais, como a fragmentação temática na *Sonata Hammerklavier* (Op. 106) de Beethoven, buscando correlações com modelos de afasia e patologias da linguagem.

---
*Desenvolvido no contexto do Laboratório Causal (Hyper-Graph).*