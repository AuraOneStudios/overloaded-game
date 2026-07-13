# Guia de Implementação no Construct 3

Como o Construct 3 (C3) depende do seu editor visual para gerenciar IDs internos de forma segura, preparei o passo a passo exato do que você deve fazer no editor do C3 para implementar nossas pendências perfeitamente!

## 1. O Tiro de Plasma do Archie
Como você já tem a arte e o som, siga os passos para criar a mecânica:
1. **Criar o Objeto:** Clique com o botão direito na aba Project, crie um novo `Sprite` e chame de `Proj_PlasmBall`. Importe a arte da sua bola de plasma.
   - *Tamanho:* Se a arte estiver muito grande, dê um duplo-clique no `Proj_PlasmBall`, clique no botão de Resize (setas azuis no topo) e diminua a resolução (ex: para algo como 32x32) ou mude o Size nas propriedades.
2. **Behavior de Movimento:** Adicione o Behavior **Bullet** ao `Proj_PlasmBall`. 
   - *Se não conseguir alterar a Speed nas propriedades iniciais*, não tem problema! Vamos setar a velocidade via código no passo 4.
3. **Parando a Bola e Efeitos Sonoros:** 
   - Na *Event Sheet 1*, crie o evento: **Condition:** `Proj_PlasmBall -> On created`. *(Fica nas opções de Misc!)*
   - **Actions:** 
     - `System -> Wait 1.0 seconds` (Aumente esse tempo ou a Speed se quiser que a bola vá mais longe!).
     - `Proj_PlasmBall -> Bullet -> Set Speed to 0` (a bola para no meio do caminho).
     - `Audio -> Stop (tag "plasma_move")`.
     - `Audio -> Play (plasma_idle) looping` (com tag `"plasma_idle"`, pode setar volume para `5` se estiver baixo).
     - `System -> Wait 3.0 seconds` (Aumentei para ficar BASTANTE tempo fritando na tela).
     - `Proj_PlasmBall -> Destroy`.
     - `Audio -> Stop (tag "plasma_idle")`.
4. **Colisão "Perfurante" com os Inimigos:** Para que a bola de plasma mate *vários* lobos sem sumir:
   - **Condition:** `Proj_PlasmBall -> On collision with another object -> Enemy_Lycan`
   - **Action:** `Enemy_Lycan -> Destroy`. *(Apenas isso! Não destrua a bola aqui, assim ela passa "atravessando" e destruindo todos os lobos no caminho até o tempo acabar!)*
5. **Disparando o Plasma (8 Direções):** No bloco de atirar da Lizzie, coloque um Sub-Event (atalho `S`):
   - **Condition:** `Char_Lizzie -> Is a boolean instance variable set (IsOverloaded)`.
   - **Action 1 (Spawn):** `Char_Lizzie -> Spawn another object -> Proj_PlasmBall` (na Layer `"0"`).
   - **Action 2 (Velocidade):** `Proj_PlasmBall -> Bullet -> Set Speed to 400`.
   - **Action 3 (Sons):** 
     - `Audio -> Play (plasma_cannon)` (volume `5` ou `10`).
     - `Audio -> Play (plasma_move) looping` (com tag `"plasma_move"`).
   - **SUB-EVENTO (Mirando Cima/Baixo/Lados):** Aperte `S` neste bloco para lidar com a direção:
     - **Condition:** `Char_Lizzie -> Is moving` (dentro da seção 8Direction)
     - **Action:** `Proj_PlasmBall -> Bullet -> Set angle of motion to Char_Lizzie.8Direction.MovingAngle`. *(Pega perfeitamente as 8 direções, cima, baixo e diagonais!)*
     - Crie um bloco `Else` (`X`) logo abaixo (para quando ela atirar *parada*):
       - Adicione a **Condition:** `Char_Lizzie -> Is mirrored` -> **Action:** `Proj_PlasmBall -> Bullet -> Set angle of motion to 180`.
       - Adicione um último `Else` -> **Action:** `Proj_PlasmBall -> Bullet -> Set angle of motion to 0`.
   - Crie outro bloco `Else` (atalho `X` na condição do `IsOverloaded` inicial) para a lógica da Wrench normal caso seja falso.

## 2. O Modo Berserker Temporário (Timer)
Para que o modo Overload do Archie acabe após um tempo:
1. Vá até a *Event Sheet 1* onde está a lógica que define `IsOverloaded` para `true` (atualmente quando o Score passa de 50).
2. Imediatamente após a ação de `Set IsOverloaded = true` nesse evento, adicione a Action:
   - `System -> Wait -> 10.0 seconds` (ou o tempo que desejar).
   - `Char_Lizzie -> Set boolean instance variable -> IsOverloaded = false`.
   - (*Opcional*) Adicione uma Action para tocar um som de "power down" para o player saber que a bateria do Archie acabou.

## 3. Tela de Game Over com Stats
Atualmente, no final da partida, você precisa passar os dados:
1. Vá até as globais do jogo. Você já tem o `Score` e provavelmente quer criar uma Global Number `TimeSurvived`.
2. Para contar o tempo, adicione: `System -> Every 1.0 seconds` -> `System -> Add 1 to TimeSurvived`.
3. No Layout do `GameOver`, adicione dois Objetos de Texto: `Txt_EnemiesDefeated` e `Txt_TimeSurvived`.
4. Na *Event Sheet* correspondente à tela de Game Over (ex: *Event sheet 3*), coloque:
   - **Condition:** `System -> On start of layout`
   - **Action:** `Txt_EnemiesDefeated -> Set text -> "Enemies Defeated: " & Score`
   - **Action:** `Txt_TimeSurvived -> Set text -> "Time Survived: " & TimeSurvived & "s"`

## 4. Configurações de Volume
Para evitar reviews ruins sobre áudio (um problema comum no CrazyGames):
1. Crie uma variável global `IsMuted` (boolean, false por padrão).
2. Adicione um Sprite de botão (com um frame de som ligado e outro desligado) no *StartScreen* e *GamePlay*.
3. Na *Event Sheet*, crie o evento de clique no botão:
   - **Condition:** `On touched / clicked` no botão.
   - **Action:** `System -> Toggle boolean IsMuted`.
4. Crie eventos para refletir o estado da variável:
   - Se `IsMuted = true` -> `Audio -> Set silent (Master) -> Silent` e defina o frame do botão para o ícone de mudo.
   - Se `IsMuted = false` -> `Audio -> Set silent (Master) -> Not silent` e defina o frame para o ícone com som.

---

## 5. Correção de Bugs e Debug (Novos)

### A. Facilitando o Debug do Archie (Modo Overload Rápido)
Criar menus de dificuldade exige telas novas, mas para **testar e debugar imediatamente** sem precisar jogar até conseguir 50 de score, faça um atalho secreto no teclado:
1. Garanta que o objeto **Keyboard** está no seu projeto.
2. Na *Event Sheet 1*, adicione: **Condition:** `Keyboard -> On Key Pressed -> (Pressione a letra 'O')`.
3. **Action:** `Char_Lizzie -> Set boolean instance variable IsOverloaded = true`.
*(Assim, durante o jogo, basta você apertar "O" no teclado e você vira o Archie instantaneamente para testar o tiro de plasma!)*

### B. Botões Invertidos no Pause
Se o "Sim" continua a partida e o "Não" sai, as Actions estão trocadas. Para corrigir:
1. Vá na aba de Eventos do Pause.
2. No evento `On touched/clicked -> PauseTextYes`, mude a Action para: `System -> Go to layout -> StartScreen` (e lembre-se de voltar a escala de tempo com `System -> Set time scale to 1`).
3. No evento `On touched/clicked -> PauseTextNo`, mude a Action para fechar o pause: `System -> Set time scale to 1` e esconda/destrua a tela de pause.

### C. Loop Infinito (Game Over -> Start -> Game Over)
Isso acontece porque variáveis como a *Vida da Lizzie* ou o estado de "Morte" não estão sendo resetados. O jogo começa, vê que ela não tem vida, e dá Game Over na hora.
1. Vá na *Event Sheet* da sua **StartScreen** (Tela Inicial).
2. Encontre o evento de quando o jogador clica em Iniciar (ex: `On clicked -> StartButton`).
3. **Antes** da Action `Go to layout (GamePlay)`, adicione a Action vital:
   - **`System -> Reset global variables to default`**.
Isso vai zerar o Score, voltar a Vida ao máximo, e garantir que a partida recomece 100% limpa!
