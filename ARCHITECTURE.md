# 🏛️ Technical Specification & System Architecture
*(Para a versão em Português, [clique aqui](#-versão-em-português-brasileiro))*

## 🇺🇸 English Version

**Project:** Hybrid AI Maze
**Role/Author:** Software Engineer & Game Developer

### 1. Architecture Overview
This project implements a **Hybrid Artificial Intelligence** architecture. The system separates cognitive responsibility into two layers operating in parallel:
* **Local Layer (Micro/Reactive):** A Reinforcement Learning Agent (Tabular Q-Learning) processed locally on the CPU, responsible for millisecond-level navigation, obstacle avoidance, and spatial mapping.
* **Cloud Layer (Macro/Strategic):** An LLM-based *Game Director* (Llama 3.1 via Groq API) operating on an asynchronous thread, responsible for analyzing aggregated metrics and manipulating the environment's procedural difficulty.

---

### 2. Functional Requirements (FRs)
*What the system must do.*

* **FR01 - 8-Way Grid Navigation:** The agent must be able to move in 4 cardinal and 4 diagonal directions using discrete grid steps (`GRID_SIZE = 40px`).
* **FR02 - Procedural Hazard Generation:** The environment must instantiate `Hazards` (plasma mines) dynamically based on `spawn_chance` and `hazard_lifetime` variables.
* **FR03 - Anti-Spawn Kill Safe Zones:** The maze generator must forbid hazard instantiation in a cross-radius (center, up, down, left, right) relative to the agent's respawn point.
* **FR04 - Q-Table Update:** The agent must register the current state (radar vision), take an action, and update the *Q-Value* using the Bellman Equation based on rewards (+1 survival, -100 death).
* **FR05 - Torus Topology:** Upon crossing screen boundaries (X or Y), the agent must be mathematically transported to the opposite side without visual glitches.
* **FR06 - XAI (Explainable AI) Translation:** The HUD must extract mathematical values from the Q-Table and JSON responses from the LLM and display them in Natural Language in real-time.
* **FR07 - Dynamic Shock Mechanic:** If the LLM increases difficulty aggressively, the agent's exploration rate (`Epsilon`) must be forced to spike temporarily to prevent reliance on obsolete routes.

---

### 3. Non-Functional Requirements (NFRs)
*How the system must behave (Quality Attributes).*

* **NFR01 - Rendering Decoupling (Performance):** The visual UI rendering (Display) must operate locked at `60 FPS`, independent of the AI brain's *Tick Rate* (e.g., 1.2 TPS).
* **NFR02 - Concurrency and Parallelism:** Network requests to the Groq API must strictly occur in *Background Threads* (Daemon) to ensure the main *Game Loop* never blocks or freezes.
* **NFR03 - Smooth Movement (UX/UI):** The agent's visual transition between blocks must be calculated via *Time-based Linear Interpolation (Lerp)*, synchronized with the AI's `TICK_DELAY`.
* **NFR04 - Graceful Degradation (Resilience):** In case of a timeout, internet drop, or API 500 error, the Director Thread must catch the exception, preserve the "Last Known Good State", and apply a *Backoff* timer to avoid server flooding.
* **NFR05 - Ghosting Prevention (Physics):** Diagonal collision must validate intermediate adjacent blocks. The agent cannot ignore hitboxes by corner-cutting.

---

### 4. Architectural Decisions: The "Why?"

#### 4.1. Why Tabular Q-Learning instead of Deep Q-Network (DQN)?
**Decision:** Use simple Python dictionaries to map states instead of Neural Networks.
**Justification:** *Transparency and Explainability (XAI).* Neural networks are "black boxes". In a project focused on showcasing AI logic on the HUD, we need exact access to the confidence value (`Q-Value: 4.68`) at the exact moment a decision is made. The Q-Table provides mathematical complexity with instant raw data access ($O(1)$ lookup time).

#### 4.2. Why use Time-based Interpolation (Lerp)?
**Decision:** Decouple the mathematical matrix (`player_x`) from the rendering matrix (`draw_x`).
**Justification:** If the AI runs at 60 decisions per second, it converges (or dies) so fast that a human observer cannot watch it learn. By locking the logic to ~1.2 Hertz and the screen to 60 Hertz, Lerp becomes necessary. If we used fixed-speed Lerp, the robot would reach its destination and stop ("tic-tac" effect). Time-based Lerp guarantees 100% organic and continuous movement, spreading the animation exactly across the *Tick* duration.

#### 4.3. Why a Hybrid System with an LLM?
**Decision:** Use Llama 3.1 via Groq to dictate procedural rules.
**Justification:** The biggest flaw of classic reinforcement learning in continuous games is "Stagnant Efficacy" — once the agent learns the perfect route, the game loses its purpose. By injecting an LLM analyzing Agent telemetry (Deaths vs. Time vs. Epsilon), the Director acts as a dynamic Game Designer manipulating the environment to break predictability, keeping the agent forever engaged in the *Exploration vs. Exploitation* dilemma.

---
---

## 🇧🇷 Versão em Português Brasileiro

**Projeto:** Hybrid AI Maze
**Papel/Autor:** Engenheiro de Software & Desenvolvedor de Jogos

### 1. Visão Geral da Arquitetura
Este projeto implementa uma arquitetura de **Inteligência Artificial Híbrida**. O sistema separa a responsabilidade cognitiva em duas camadas operando em paralelo:
* **Camada Local (Micro/Reativa):** Um Agente de Aprendizado por Reforço (Q-Learning Tabular) processado localmente na CPU, responsável por navegação em milissegundos, desvio de obstáculos e mapeamento espacial.
* **Camada Cloud (Macro/Estratégica):** Um *Game Director* baseado em LLM (Llama 3.1 via Groq API) operando em uma thread assíncrona, responsável por analisar métricas agregadas e manipular a dificuldade procedural do ambiente.

---

### 2. Requisitos Funcionais (FRs)
*O que o sistema é obrigado a fazer.*

* **FR01 - Navegação em Grade 8-Way:** O agente deve ser capaz de se mover nas 4 direções cardeais e 4 diagonais usando passos discretos na grade (`GRID_SIZE = 40px`).
* **FR02 - Geração Procedural de Perigos:** O ambiente deve instanciar `Hazards` (minas) dinamicamente baseados nas variáveis `spawn_chance` e `hazard_lifetime`.
* **FR03 - Zonas Seguras Anti-Spawn Kill:** O gerador de labirintos deve proibir a instanciação de perigos em um raio cruzado (centro, cima, baixo, esquerda, direita) em relação ao ponto de renascimento do agente.
* **FR04 - Atualização de Tabela-Q:** O agente deve registrar o estado atual (visão do radar), tomar uma ação e atualizar o *Q-Value* usando a Equação de Bellman com base em recompensas (+1 sobrevivência, -100 morte).
* **FR05 - Topologia Toroide:** Ao cruzar os limites da tela (X ou Y), o agente deve ser transportado para o lado oposto matematicamente sem gerar falhas visuais.
* **FR06 - Tradução de XAI (Explainable AI):** A HUD deve extrair os valores matemáticos da Q-Table e as respostas JSON do LLM e exibi-los em Linguagem Natural em tempo real.
* **FR07 - Mecânica de Choque Dinâmico:** Se o LLM aumentar a dificuldade agressivamente, a taxa de exploração do agente (`Epsilon`) deve ser forçada a subir temporariamente para evitar o uso de rotas obsoletas.

---

### 3. Requisitos Não Funcionais (NFRs)
*Como o sistema deve se comportar (Atributos de Qualidade).*

* **NFR01 - Desacoplamento de Rendering (Performance):** A renderização visual da interface (Display) deve operar fixada a `60 FPS`, independentemente do *Tick Rate* do cérebro da IA (ex: 1.2 TPS).
* **NFR02 - Concorrência e Paralelismo:** As requisições de rede para a API da Groq devem ocorrer estritamente em *Background Threads* (Daemon) para garantir que o *Game Loop* principal nunca bloqueie (freeze).
* **NFR03 - Movimento Suave (UX/UI):** A transição visual do agente entre os blocos deve ser calculada via *Time-based Linear Interpolation (Lerp)*, sincronizada com o `TICK_DELAY` da IA.
* **NFR04 - Degradação Graciosa (Resiliência):** Em caso de *timeout*, queda de internet ou erro 500 na API, a Thread do Diretor deve tratar a exceção, preservar o "Last Known Good State" (último estado válido) e aplicar um *Backoff* no timer de chamadas para evitar sobrecarga.
* **NFR05 - Prevenção de Ghosting (Física):** A colisão diagonal deve validar os blocos adjacentes intermediários. O agente não pode ignorar *hitboxes* ao "cortar caminho" nas quinas (Corner-Cutting).

---

### 4. Decisões Arquiteturais: O "Por Que?"

#### 4.1. Por que Q-Learning Tabular em vez de Deep Q-Network (DQN)?
**Decisão:** Usar dicionários Python simples para mapear estados, em vez de Redes Neurais.
**Justificativa:** *Transparência e Explicabilidade (XAI).* Redes neurais são "caixas pretas". Em um projeto focado em mostrar a lógica da IA na HUD, precisamos acessar o valor exato da confiança (`Q-Value: 4.68`) no momento exato em que a decisão é tomada. A Q-Table fornece complexidade matemática com acesso instantâneo aos dados brutos ($O(1)$ lookup time).

#### 4.2. Por que usar Interpolação (Lerp) baseada no Tempo?
**Decisão:** Desacoplar a matriz matemática (`player_x`) da matriz de renderização (`draw_x`).
**Justificativa:** Se a IA rodar a 60 decisões por segundo, ela converge (ou morre) tão rápido que o usuário humano não consegue observar o aprendizado. Ao travar a lógica em ~1.2 Hertz e a tela em 60 Hertz, criamos a necessidade do Lerp. Se usássemos um Lerp de velocidade fixa, o robô chegaria ao destino e pararia ("efeito tic-tac"). O *Time-based Lerp* garante movimento 100% orgânico e contínuo, espalhando a animação exatamente pela duração do *Tick*.

#### 4.3. Por que um Sistema Híbrido com LLM?
**Decisão:** Usar Llama 3.1 via Groq para ditar regras procedurais.
**Justificativa:** A maior falha do aprendizado por reforço clássico em jogos contínuos é a "Eficácia Estagnada" — uma vez que o agente aprende a rota perfeita, o jogo perde o propósito. Ao injetar um LLM analisando a telemetria do Agente (Mortes vs. Tempo vs. Epsilon), o Diretor atua como um Game Designer dinâmico que manipula o ambiente para quebrar a previsibilidade, mantendo o agente sempre engajado no dilema *Exploration vs. Exploitation*.