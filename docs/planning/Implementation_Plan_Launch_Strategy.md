# Diagnóstico e Plano de Ação - OVERLOADED (Fase 1 e P0s)

Abaixo está a proposta de plano de ação para executarmos os itens **P0 (ações imediatas e de publicação)** levantados no seu relatório de diagnóstico. Nosso objetivo agora é focar em deixar o jogo pronto para publicação real.

## Open Questions

Antes de iniciarmos ou concluirmos certas partes, precisamos da sua definição sobre alguns pontos vitais levantados no diagnóstico:
> [!IMPORTANT]
> **1. O que acontece após o Overload Mode terminar?** (Item 8)
> No código atual, a variável `IsOverloaded` é mantida como `true` até a run acabar. Este será um estado temporário (Archie tem um limite de tempo ou energia e depois volta a ser Lizzie) ou um power-up permanente até o Game Over? 
> 
> **2. Implementação das armas do Archie (Recoil Cannon / Trample):** (Item 0b)
> Atualmente, Archie atira a mesma *Wrench* que a Lizzie, apenas mudando o aspecto visual. Você prefere que nós implementemos um ataque diferente (ex: Recoil Cannon) para o Archie, ou prefere apenas atualizar o README para que o marketing reflita o estado atual (troca visual)?
> 
> **3. Dados do Repositório e Itch.io:** (Itens 2, 4 e 9)
> Já existe uma URL para o site institucional (ex: o projeto `auraone-hugo`) que deseja colocar no linkhub/sobre do repositório?

## Proposed Changes

Focaremos inicialmente nas ações técnicas de desenvolvimento P0.

### Landing Page e Marketing (0a)
* **Objetivo:** Transformar o botão inútil ("View Source") no CTA principal para jogar.
#### [MODIFY] [index.html](../index.html)
- Trocar o link do botão `.btn-primary` de "https://github.com/..." para `./play/` (ou caminho relativo correto).
- Trocar o texto do botão de "View Source / Ver Código Fonte" para "Play Now / Jogar Agora".

### Game Over Stats (0c)
* **Objetivo:** Adicionar informações como Inimigos Derrotados e Tempo Sobrevivido.
#### [MODIFY] [GameOver.json](../../layouts/GameOver.json) e [Event sheet 3.json](../../eventSheets/Event%20sheet%203.json) (ou equivalente do Game Over)
- Adicionar objetos de Texto na tela de Game Over.
- Passar os valores globais (`Score` e uma nova variável para tempo sobrevivido) do Gameplay para a tela de Game Over.

### Configurações de Volume (6)
* **Objetivo:** Evitar reviews negativos sobre áudio implementando controle mínimo.
#### [MODIFY] [StartScreen.json](../../layouts/StartScreen.json) e [GamePlay.json](../../layouts/GamePlay.json)
- Adicionar um pequeno ícone ou texto de "Sound: ON/OFF" ou um controle de volume.
- Vincular a variável global de controle de som à `Audio` tag ou master volume no Construct.

### GitHub Release (1 & 2)
* **Objetivo:** Criar e publicar a versão 0.1.0 oficial.
#### [NEW] GitHub Tag/Release
- Assim que as modificações de código estiverem estáveis, usarei ferramentas do Git e GitHub (se possível) para criar uma Tag `v0.1.0`.

## Verification Plan
1. **Teste Web (Ação 4):** Lançar a nova versão via GitHub Actions (já configurado no projeto para a branch `main`). Testaremos o link `docs/play` no browser.
2. **Revisão Manual:** Iniciaremos uma run, morreremos no início para ver os Stats Zerados, e tentaremos outra sobrevivendo mais para validar os contadores.
3. **Página Itch.io (Ações 5 e 6):** Eu gerarei os textos (descrições curtas e longas) em markdown ou texto puro para você copiar e colar na criação da sua página de rascunho no itch.io.
