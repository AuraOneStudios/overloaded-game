# Plano de Implementação: OVERLOADED (Best International Game Award)

O objetivo central deste plano é transformar o protótipo atual em um forte candidato a prêmios, implementando perfeitamente o nosso **Ponto de Venda Único (USP)**: um ciclo de risco e recompensa onde o jogador não pode ficar parado ("AFK") num canto seguro. A horda vai ficar tão forte que o jogador será obrigado a mergulhar nos inimigos para coletar peças e evoluir suas habilidades.

> [!IMPORTANT]  
> **Revisão Necessária**
> Este é o documento de design fundamental para a próxima fase. Leia com atenção as lógicas propostas abaixo e clique em **Proceed** (ou diga que aprova) para começarmos a botar a mão na massa no Construct 3.

## Open Questions
- Para o sistema visual dos itens caídos (os "Drops"), você prefere usar o Sprite de uma **Engrenagem**, um **Parafuso** ou uma **Bateria**?
- Você prefere que a Lizzie upe de nível automaticamente ao coletar X peças, ou prefere que a própria quantidade de peças seja gasta como "dinheiro" na tela de Game Over para comprar melhorias permanentes (estilo Roguelite)? (Recomendo o buff automático durante a fase para manter o ritmo frenético).

---

## Proposta de Sistemas (Mecânica Central)

### 1. Sistema de Drops e Coleta (Risco)
- **Novo Objeto:** `Obj_Component` (O item que cai no chão).
- **Lógica:** Quando um projétil destrói um inimigo (`Enemy_Lycan`), ele tem uma chance (ex: 50%) de spawnar um `Obj_Component` no mesmo lugar.
- **Coleta:** Quando a Lizzie encosta no componente, ele é destruído e adiciona +1 na variável `Scrap` (Sucata). Toca um efeito sonoro satisfatório ("ding").
- *Design:* Como os inimigos morrem longe do jogador (pois ela atira de longe), o jogador precisará ativamente sair da segurança para pegar o *Loot* antes que a tela lote de lobos.

### 2. Sistema de Buffs Incrementais (Recompensa)
- **Novas Variáveis:** `PlayerLevel` (inicia no 1) e `Scrap` (inicia no 0).
- **Lógica de Nível:** A cada X sucatas (ex: 10, depois 20, depois 40), a Lizzie sobe de Nível.
- **Recompensa:** Toda vez que ela sobe de nível, o "cooldown" (tempo de recarga) do ataque da chave de fenda diminui, fazendo ela atirar mais rápido. Também podemos aumentar a velocidade de movimento (`MaxSpeed` do 8Direction) em 5% por nível.

### 3. Escalonamento da Horda (Ameaça Crescente)
Atualmente, o jogo cria 1 inimigo a cada 0.8 segundos. Vamos tornar isso opressor:
- **Lógica Dinâmica:** O tempo de "Spawn" dos inimigos vai diminuir gradativamente com o tempo de sobrevivência. Começa em 1 segundo e, a cada minuto que passa, o intervalo cai (0.8s, 0.6s, 0.4s).
- **Inimigos Furiosos:** A chance de nascer um inimigo da classe "Furious" (mais rápido e perigoso) aumenta conforme o nível do jogador aumenta.

---

## Plano de Execução (Próximos Passos no Construct)

Se aprovado, eu guiarei você passo a passo na criação desses elementos dentro do editor do Construct 3:

1. **Fase 1 (Sprites e Variáveis):** Criar os objetos visuais e as variáveis globais na Event sheet 1.
2. **Fase 2 (Eventos de Coleta):** Programar o drop de itens ao matar inimigos e o raio de coleta da Lizzie.
3. **Fase 3 (Matemática do Nível):** Configurar a lógica que converte "Sucata" em Level e aplica os buffs.
4. **Fase 4 (Ajuste da Horda):** Modificar o cronômetro do sistema para spawnar monstros com base no tempo de jogo.
