# 🧠 Hybrid AI Maze: Q-Learning Agent vs LLM Game Director
*(Para a versão em Português, [clique aqui](#-versão-em-português-brasileiro))*

## 🇺🇸 English Version

### 🎯 About the Project
This is an advanced study project focused on Artificial Intelligence, Game Engineering, and UX Design. The goal is to create a dynamic environment where an Agent learns to survive using local **Reinforcement Learning (Q-Learning)**, while the game environment is controlled by an **LLM-based Game Director**. The LLM analyzes the agent's performance and adjusts the maze's difficulty and hazard spawn rates in real-time.

🤖 **AI Assistance Note:** This project was developed with the educational support and assistance of Google's **Gemini AI**, acting as a pair programmer and technical mentor.

### 🌟 Key Features
- **Hybrid AI Architecture:** A local Q-Learning Agent mapping the grid in real-time, while a Cloud-based LLM Director (Llama 3.1 via Groq) oversees the environment.
- **Explainable AI (XAI) Dashboard:** A dual-panel HUD that translates both the LLM Director's JSON decisions and the Agent's Q-Table values (Radar and Confidence) into human-readable natural language in real-time.
- **Decoupled Rendering Engine (60 FPS):** Uses Time-based Linear Interpolation (Lerp) to separate the AI's logical tick rate from the monitor's refresh rate, achieving ultra-fluid animations and deliberate, human-like pacing.
- **Torus Topology & 8-Way Movement:** The agent can navigate diagonally with advanced corner-collision physics and traverse screen borders infinitely (Pac-Man effect).
- **Graceful API Degradation:** Asynchronous multithreading ensures the game never freezes during API calls. If the internet drops, a fallback mechanism keeps the game running flawlessly on the "Last Known Good State."
- **Sci-Fi Graphic Overhaul:** Custom Pygame vector rendering featuring a cyberpunk neon palette, holographic grids, and glowing plasma hazards.

### 🛠️ Tech Stack
* **Language:** Python
* **Graphics Engine:** Pygame
* **Agent AI:** Tabular Q-Learning (Local Reinforcement Learning)
* **Environment AI:** LLM API Integration (Groq / Llama)
* **Architecture:** Asynchronous Threading, Time-based Lerp, State Machine

### 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/prBento/StudyCode.git](https://github.com/prBento/StudyCode.git)
   cd StudyCode/AI_Maze
   ```
2. **Install the required dependencies:**
   Make sure you have Python 3.8+ installed. Then run:
   ```bash
   pip install pygame openai python-dotenv
   ```
3. **Set up the Environment Variables:**
   Create a file named `.env` in the root folder of the project and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
   *(You can get a free API key at console.groq.com)*
4. **Run the Simulation:**
   ```bash
   python main.py
   ```

### 🧠 AI Architecture: Why Q-Learning?
For the Agent's brain, we chose **Tabular Q-Learning** over more complex Deep Learning models for the following reasons:
1. **Discrete State Space:** The grid-based nature of our maze makes it perfect for a finite state representation. The agent can map its surroundings as clear, discrete states.
2. **Transparency (XAI):** Unlike Neural Networks ("black boxes"), a Q-Table is entirely transparent. We extract the exact mathematical values (`Q-Values`) in real-time and translate them to the player to explain *why* the agent chose a specific path.
3. **The Bellman Equation:** The agent learns to value *future, long-term rewards* (surviving) rather than just making greedy, immediate choices, avoiding paths that look safe now but lead to dead-ends.

### 🚦 Git & Commit Standards
This project follows the *Conventional Commits* specification: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`.

### 🗺️ Development Roadmap Highlights
- [x] Phase 1: Foundation (Pygame setup, grid movement, static collisions).
- [x] Phase 2: The Muscle (Q-Learning algorithm and dynamic hazards).
- [x] Phase 3: The Brain (LLM Director integration via Groq).
- [x] Phase 4: Engine Polish (Multithreading, 60 FPS Time-based Lerp, Torus Topology).
- [x] Phase 5: XAI & UI/UX (Sci-Fi overhaul, Graceful Degradation, Dual Explainability Panels).


## 🇧🇷 Versão em Português Brasileiro

### 🎯 Sobre o Projeto
Este é um projeto de estudo avançado focado em Inteligência Artificial, Engenharia de Jogos e Design de UX. O objetivo é criar um ambiente dinâmico onde um Agente aprende a sobreviver usando **Aprendizado por Reforço (Q-Learning)** localmente, enquanto o ambiente é controlado por um **Game Director baseado em LLM**. O LLM analisa o desempenho do agente e ajusta a dificuldade e a taxa de perigos em tempo real.

🤖 **Nota de Assistência de IA:** Este projeto foi desenvolvido com o apoio educacional e assistência da IA **Gemini** do Google, atuando como um *pair programmer* (programador em par) e mentor técnico.

### 🌟 Funcionalidades Principais
- **Arquitetura de IA Híbrida:** Um Agente local mapeando a grade em tempo real, enquanto um Diretor LLM na nuvem (Llama 3.1 via Groq) supervisiona o ambiente.
- **Dashboard de IA Explicável (XAI):** Um painel duplo (HUD) que traduz tanto as decisões em JSON do Diretor quanto os valores matemáticos da Q-Table do Agente (Radar e Confiança) para linguagem natural humana em tempo real.
- **Motor de Renderização Desacoplado (60 FPS):** Uso de Interpolação Linear Temporal (Lerp) para separar o processamento lógico da IA da taxa de atualização do monitor, gerando animações ultra-fluidas e cadência de movimento realista.
- **Topologia Toroide e Movimento em 8 Direções:** O agente pode navegar nas diagonais com física avançada de colisão em quinas e atravessar as bordas da tela infinitamente (Efeito Pac-Man).
- **Degradação Graciosa de API:** O uso de *Multithreading* assíncrono garante que o jogo nunca trave aguardando a API. Se a internet cair, um mecanismo de *fallback* mantém o jogo rodando perfeitamente no último estado válido.
- **Overhaul Gráfico Sci-Fi:** Renderização vetorial customizada no Pygame com paleta neon cyberpunk, grades holográficas e minas de plasma com efeito de brilho (glow).

### 🛠️ Stack Tecnológico
* **Linguagem:** Python
* **Motor Gráfico:** Pygame
* **IA do Agente:** Q-Learning Tabular (Aprendizado por Reforço Local)
* **IA do Ambiente:** Integração via API com LLM (Groq / Llama)
* **Arquitetura:** Threading Assíncrono, Lerp baseado em Tempo, Máquina de Estados

### 🚀 Como Rodar Localmente

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/prBento/StudyCode.git](https://github.com/prBento/StudyCode.git)
   cd StudyCode/AI_Maze
   ```
2. **Instale as dependências:**
   Certifique-se de ter o Python 3.8+ instalado. Então rode:
   ```bash
   pip install pygame openai python-dotenv
   ```
3. **Configure as Variáveis de Ambiente:**
   Crie um arquivo chamado `.env` na raiz do projeto e adicione sua chave de API da Groq:
   ```env
   GROQ_API_KEY=sua_chave_api_groq_aqui
   ```
   *(Você pode obter uma chave gratuita em console.groq.com)*
4. **Inicie a simulação:**
   ```bash
   python main.py
   ```

### 🧠 Arquitetura da IA: Por que Q-Learning?
Para o cérebro do Agente, escolhemos o **Q-Learning Tabular** em vez de Redes Neurais complexas pelos seguintes motivos:
1. **Espaço de Estados Discreto:** A natureza em grade do labirinto o torna perfeito para representação finita.
2. **Transparência (XAI):** Diferente de Redes Neurais ("caixas pretas"), uma Tabela-Q é 100% legível. Nós extraímos os valores matemáticos (`Q-Values`) em tempo real e os traduzimos na tela para explicar *por que* o agente escolheu um caminho.
3. **A Equação de Bellman:** O agente aprende a valorizar *recompensas futuras* (sobrevivência a longo prazo), evitando caminhos que parecem seguros agora, mas levam à morte certa.

### 🚦 Padrões de Git e Commits
Este projeto segue a especificação *Conventional Commits*: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`.

### 🗺️ Destaques do Roadmap de Desenvolvimento
- [x] Fase 1: Fundação (Pygame, movimentação em grade, colisões estáticas).
- [x] Fase 2: O Músculo (Algoritmo Q-Learning e perigos dinâmicos).
- [x] Fase 3: O Cérebro (Integração com LLM Diretor via Groq).
- [x] Fase 4: Polimento de Engine (Multithreading, Lerp Temporal a 60 FPS, Topologia Toroide).
- [x] Fase 5: XAI & UI/UX (Overhaul Sci-Fi, Degradação Graciosa, Painéis Duplos de Explicabilidade).

