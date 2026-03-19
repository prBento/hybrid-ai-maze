# 📌 Project Backlog & Status
*(Para a versão em Português, [clique aqui](#-versão-em-português-brasileiro))*

## 🇺🇸 English Version

### 🎨 Graphics & UI/UX
- [x] **Heads-Up Display (HUD):** Create a visual UI overlay displaying real-time metrics.
- [x] **Sprite Integration:** Replace basic rectangles with dynamic geometric sprites.
- [x] **Visual Themes:** Add cybernetic grid background for spatial awareness.
- [x] **XAI Dashboard (Director):** Display an on-screen log translating the LLM's decisions.
- [x] **Visual Hitbox Correction:** Sync visual lerp position with crash coordinates.
- [x] **Ultra-Fluid Movement:** Upgrade lerp to be completely time-dependent (Time-based Lerp) decoupling frame rate from tick rate.
- [x] **Agent XAI Panel:** Implement a UI panel translating the Q-Table mathematical values and radar into human-readable natural language.
- [x] **Graphic Overhaul:** Complete Sci-Fi UI/UX redesign with a neon cyberpunk palette, glowing hazards, and an advanced drone sprite.

### 🧠 AI & System Architecture
- [x] **Multithreading:** Move the LLM API calls to a background thread to prevent game freezing.
- [x] **Initial Learning Curve (Onboarding):** Start the first epoch with very low hazards to allow safe Q-Table population.
- [x] **Diagonal Movement:** Expand AI action space to 8 directions.
- [x] **Advanced Collision Physics:** Prevent diagonal corner-cutting ghosting by adding intermediate hazard checks.
- [x] **Torus Topology (Pac-Man Effect):** Allow the player to cross screen borders infinitely.
- [x] **Graceful Degradation (API Fallback):** Implement a "Last Known Good State" memory and backoff timer if the LLM API drops.

---

## 🇧🇷 Versão em Português Brasileiro

### 🎨 Gráficos & UI/UX
- [x] **Interface de Bordo (HUD):** Criar uma interface visual com métricas em tempo real.
- [x] **Integração de Sprites:** Substituir retângulos básicos por sprites geométricos dinâmicos.
- [x] **Temas Visuais:** Adicionar grade cibernética no fundo.
- [x] **Dashboard XAI (Diretor):** Mostrar log traduzindo as decisões do LLM.
- [x] **Correção de Hitbox Visual:** Sincronizar posição visual com coordenadas reais na explosão.
- [x] **Movimentação Ultra-Fluida:** Interpolação linear por tempo desacoplando o FPS do pensamento da IA.
- [x] **Painel XAI do Agente:** Implementar painel traduzindo valores da Q-Table e radar para linguagem natural.
- [x] **Overhaul Gráfico:** Redesign completo em estilo Sci-Fi/Cyberpunk com paleta neon, perigos brilhantes e um sprite de drone avançado.

### 🧠 IA & Arquitetura de Sistema
- [x] **Multithreading:** Mover requisições do LLM para segundo plano para evitar travamentos.
- [x] **Curva de Aprendizado (Onboarding):** Iniciar a primeira rodada com perigos quase zerados para a IA mapear rotas seguras.
- [x] **Movimentação Diagonal:** Expandir as ações da IA para 8 direções.
- [x] **Física de Colisão Avançada:** Impedir ghosting diagonal adicionando checagem de impacto nas quinas.
- [x] **Topologia Toroide (Efeito Pac-Man):** Permitir atravessar as bordas da tela infinitamente.
- [x] **Degradação Graciosa (Fallback da API):** Manter últimas regras válidas e estender o timer se a conexão com o LLM cair.