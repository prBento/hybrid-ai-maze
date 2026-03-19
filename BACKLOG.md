# 📌 Project Backlog - Version 2.0 (The Maze Evolution)
*(Para a versão em Português, [clique aqui](#-versão-em-português-brasileiro))*

## 🇺🇸 English Version

### 🌐 Web & Architecture
- [ ] **GitHub Pages Deployment:** Port the Python/Pygame engine to WebAssembly (Wasm) using `pygbag` or `asyncio` so it runs natively in the browser.
- [ ] **Web API Security:** Adapt the Groq LLM API requests and multithreading to comply with browser CORS and asynchronous web limits.

### 🏗️ Core Gameplay & Procedural Generation
- [ ] **Dynamic Labyrinth Engine:** Overhaul the hazard generation. Replace isolated plasma mines with connected "walls" that dynamically spawn and despawn to create shifting corridors.
- [ ] **Procedural Algorithms:** Implement coherent maze generation (e.g., Cellular Automata) so the environment truly feels like a shifting maze rather than random noise.
- [ ] **Level Progression (Scenarios):** Introduce distinct phases/levels with different visual themes, grid sizes, or LLM Director personalities as the agent survives longer.

### 🎛️ UI/UX & Audio Engineering
- [ ] **Sound Design:** Implement sound effects (SFX) for UI interactions, agent movement, shifting walls, and game-over explosions.
- [ ] **Interactive Game State Controls:** Add clickable UI buttons for `Start`, `Pause/Stop`, and `Restart` the simulation.
- [ ] **Audio Controls:** Add a volume control slider or a Mute/Unmute toggle for the sound effects.

---

## 🇧🇷 Versão em Português Brasileiro

### 🌐 Web & Arquitetura
- [ ] **Deploy no GitHub Pages:** Portar a engine do Pygame para WebAssembly (Wasm) usando `pygbag` ou `asyncio` para rodar direto no navegador.
- [ ] **Segurança de API Web:** Adaptar as requisições da Groq e o multithreading para funcionar dentro das regras de segurança e assincronicidade do navegador (CORS).

### 🏗️ Gameplay & Geração Procedural
- [ ] **Motor de Labirinto Dinâmico:** Refazer a geração de perigos. Substituir minas isoladas por "paredes" conectadas que surgem e desaparecem, criando corredores mutáveis.
- [ ] **Algoritmos Procedurais:** Implementar algoritmos de labirinto (ex: Autômatos Celulares) para garantir que as paredes pareçam uma estrutura coesa e não apenas ruído aleatório.
- [ ] **Progressão de Fases (Cenários):** Criar diferentes níveis com temas visuais, tamanhos de grade ou personalidades do Diretor LLM distintos conforme o agente sobrevive.

### 🎛️ UI/UX & Engenharia de Áudio
- [ ] **Design de Som:** Adicionar efeitos sonoros (SFX) para cliques, movimento do agente, paredes se movendo e explosões.
- [ ] **Controles de Estado do Jogo:** Adicionar botões interativos clicáveis na interface para `Start`, `Pause/Stop` e `Restart`.
- [ ] **Controle de Áudio:** Adicionar um botão de controle de volume ou alternância de Mutar/Desmutar para os efeitos sonoros.