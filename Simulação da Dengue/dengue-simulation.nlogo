; Definindo dois tipos de agentes: pessoas e mosquitos
breed [ people person ]
breed [ mosquitoes mosquito ]

; Variáveis globais (compartilhadas por todos os agentes)
globals [
  ; Mosquitos
  mosquitoes-count-total ; quantidade total de mosquitos
  mosquitoes-count-with-dengue ; quantidade de mosquitos infectados com dengue

  mosquitoes-lifespan ; tempo de vida dos mosquitos
  mosquitoes-eggs ; número de ovos produzidos

  mosquitoes-dengue-average-incubation-days ; tempo médio de incubação do vírus no mosquito
  mosquitoes-dengue-interval-incubation-days ; variação permitida nesse tempo
  mosquitoes-dengue-inherit-eggs-percentage ; porcentagem de ovos que herdam dengue

  ; Pessoas
  people-count-total ; total de pessoas
  people-count-with-dengue ; número de pessoas com dengue
  people-count-recovered-from-dengue ; número de pessoas recuperadas
  people-count-death-common ; mortes por causas naturais
  people-count-death-dengue ; mortes por dengue

  people-lifespan ; expectativa de vida das pessoas

  ; parâmetros da dengue nas pessoas
  people-dengue-average-incubation-days
  people-dengue-interval-incubation-days
  people-dengue-average-viral-days
  people-dengue-interval-viral-days
  people-dengue-fatality-percentage

  mosquitoes-to-create ; controle de reprodução de mosquitos
]

; Propriedades dos agentes "people"
people-own [
  age ; idade da pessoa
  age-death ; idade prevista de morte

  dengue? ; está com dengue?
  transmitter? ; está transmitindo dengue?
  days-dengue-incubation ; tempo de incubação atual
  days-dengue-viral ; tempo de sintomas
  days-dengue-sick ; total de dias doente
  dengue-recurrence ; quantas vezes pegou dengue
]

; Propriedades dos mosquitos
mosquitoes-own [
  age ; idade
  age-death ; tempo de vida
  dengue? ; está com dengue?
  transmitter? ; transmite?
  days-dengue-incubation ; incubação
  days-dengue-sick ; dias com vírus
]

; Função que prepara a simulação
to button-setup
  clear-all
  setup-constants
  setup-initial-population
  setup-initial-contamination
  reset-ticks
end

; Função que executa a simulação a cada passo
to button-go
  if not any? turtles [ stop ]

  ; Movimento e progressão da doença em todos os agentes
  ask turtles [
    each-move
    each-check-sick
  ]

  ask mosquitoes [ mosquitoes-aging ]
  mosquitoes-reproducing
  mosquitoes-biting

  ask people [
    people-aging
    people-checking-health
  ]
  people-reproducing

  tick
end

; Inicializa os parâmetros
to setup-constants
  ; mosquito
  set mosquitoes-count-total variable-initial-number-mosquitoes
  set mosquitoes-count-with-dengue variable-initial-number-cases-dengue-mosquitoes

  set mosquitoes-lifespan 30
  set mosquitoes-eggs variable-number-eggs-mosquitoes

  set mosquitoes-dengue-average-incubation-days 10
  set mosquitoes-dengue-interval-incubation-days 2
  set mosquitoes-dengue-inherit-eggs-percentage variable-inherit-dengue-eggs-mosquitoes / 100

  ; people
  set people-count-total variable-initial-number-people
  set people-count-with-dengue variable-initial-number-cases-dengue-people
  set people-count-recovered-from-dengue 0
  set people-count-death-common 0
  set people-count-death-dengue 0

  set people-lifespan (72 * 395) ; years of life x days per year

  set people-dengue-average-incubation-days 6
  set people-dengue-interval-incubation-days 2
  set people-dengue-average-viral-days 8
  set people-dengue-interval-viral-days 4
set people-dengue-fatality-percentage variable-fatality-percentage-of-people / 100
end

; Criação inicial das pessoas e mosquitos com seus atributos
to setup-initial-population
  ; cada pessoa e mosquito é posicionado e configurado com idade, expectativa de vida e status de dengue
  create-people variable-initial-number-people
  [
    ; graphic
    set shape "person"
    set color blue
    set size 1.3
    setxy random-xcor random-ycor

    ; info
    set age random(people-lifespan) + 1
    set age-death random-number people-lifespan (10 * 365)

    ; dengue
    set dengue? false
    set transmitter? false
    set days-dengue-incubation random-number people-dengue-average-incubation-days people-dengue-interval-incubation-days
    set days-dengue-viral random-number people-dengue-average-viral-days people-dengue-interval-viral-days
    set days-dengue-sick 0
    set dengue-recurrence 0
  ]

  create-mosquitoes variable-initial-number-mosquitoes
  [
    ; graphic
    set shape "dot"
    set color green
    set size 1
    set xy random-xcor random-ycor

    ; info
    set age random(mosquitoes-lifespan) + 1
    set age-death random-number mosquitoes-lifespan 15

    ; dengue
    set dengue? false
    set transmitter? false
    set days-dengue-incubation random-number mosquitoes-dengue-average-incubation-days mosquitoes-dengue-interval-incubation-days
    set days-dengue-sick 0
  ]
end

; Infecta um número inicial de pessoas e mosquitos
to setup-initial-contamination
  ; define quem começa com dengue e se está transmitindo ou incubando
  ask n-of variable-initial-number-cases-dengue-people people
  [
    set dengue? true
    set days-dengue-sick (random-number(mosquitoes-dengue-average-incubation-days - 1) mosquitoes-dengue-interval-incubation-days) + 1

    ifelse days-dengue-sick >= days-dengue-incubation
    [
      set transmitter? true
      set color red
    ]
    [
      set color yellow
    ]

    set dengue-recurrence dengue-recurrence + 1
  ]

  ask n-of variable-initial-number-cases-dengue-mosquitoes mosquitoes
  [
    set dengue? true
    set days-dengue-sick (random-number(mosquitoes-dengue-average-incubation-days - 1) mosquitoes-dengue-interval-incubation-days) + 1

    ifelse days-dengue-sick >= days-dengue-incubation
    [
      set transmitter? true
      set color red
    ]
    [
      set color yellow
    ]
  ]
end

; Gera um número aleatório dentro de um intervalo
to-report random-number [average interval]
  let interval-min average - interval
  let interval-max average + interval

  let number interval-min + random(interval-max - interval-min + 1)
  report number
end

; Fator senoidal de reprodução sazonal dos mosquitos
to-report seasonal-reproduction-factor
  let day-of-year ticks mod 365
  let reproduction-factor (sin (2 * pi * (day-of-year / 365))) * 0.5 + 0.5

  report reproduction-factor
end

; Movimento aleatório dos agentes
to each-move
  rt random 50 lt random 50 fd 1
end

; Verifica se o agente já está em estado de transmissão
to each-check-sick
  if days-dengue-sick != 0 [
    ; aumenta os dias e atualiza se virou transmissor
    set days-dengue-sick days-dengue-sick + 1

    if transmitter? = false and days-dengue-sick >= days-dengue-incubation
    [
      set transmitter? true
      set color red
    ]
  ]
end

; Ativa o estado de doente
to each-get-sick
  set dengue? true
  set color yellow
  set days-dengue-sick 1
end

; Envelhecimento dos mosquitos
to mosquitoes-aging
  set age age + 1

  if age >= age-death
  [
    set mosquitoes-count-total mosquitoes-count-total - 1
    die
  ]
end

; Reprodução dos mosquitos com influência sazonal
to mosquitoes-reproducing
  set mosquitoes-to-create 0

  ; for each mosquito, check whether it can reproduce
  ask mosquitoes [
    if random-float 1 > 0.9 [

      if age > 5 and age < age-death [
        ; seasonal reproduction factor
        let reproduction-factor seasonal-reproduction-factor

        let new-eggs round (reproduction-factor * mosquitoes-eggs)
        set mosquitoes-to-create mosquitoes-to-create + new-eggs
      ]
    ]
  ]

  if mosquitoes-to-create > 0 [
    create-new-mosquitoes mosquitoes-to-create
  ]
end

; Criação de novos mosquitos
to create-new-mosquitoes [new-mosquitoes]
create-mosquitoes new-mosquitoes [
  set shape "dot"
  set color green
  set size 1
  set xy random-xcor random-ycor

  set age 0
  set age-death random-number mosquitoes-lifespan 15

  ; determine whether the mosquito inherited dengue fever
  let inherit-dengue? false
  if dengue? = true and random-float 1 < mosquitoes-dengue-inherit-eggs-percentage [
    set inherit-dengue? true
  ]

  if inherit-dengue? [
    set transmitter? false
    set days-dengue-incubation random-number mosquitoes-dengue-average-incubation-days mosquitoes-dengue-interval-incubation-days
    set days-dengue-sick 0
    set color yellow  ; Identificar os mosquitos com dengue incubada
  ]
]

set mosquitoes-count-total mosquitoes-count-total + new-mosquitoes
end

; Função que simula as picadas e possíveis infecções cruzadas
to mosquitoes-biting
  ; Se houver uma pessoa na mesma posição:
  ; - mosquito transmite dengue se for transmissor
  ; - mosquito adquire dengue se picar uma pessoa doente

  ask mosquitoes [
    ; find people in the same position as the mosquito
    let possible-victims people-here

    ; if there is at least one person in the same location, choose one at random
    if any? possible-victims [
      let victim one-of possible-victims

      ; transmission from mosquito to person
      if dengue? = true and transmitter? = true and not [dengue? = true] of victim [
        ask victim [
          each-get-sick
        ]
      ]

      ; transmission from person to mosquito
      if dengue? = false and [dengue? = true] of victim and [transmitter? = true] of victim [
        each-get-sick
      ]
    ]
  ]
end

; Envelhecimento das pessoas
to people-aging
  set age age + 1

  if age >= age-death
  [
    set people-count-total people-count-total - 1
    set people-count-death-common people-count-death-common + 1
    die
  ]
end

; Reposição populacional humana
to people-reproducing
if people-count-total < variable-initial-number-people
  [
    let difference variable-initial-number-people - people-count-total

    create-people difference
    [
      ; graphic
      set shape "person"
      set color blue
      set size 1.3
      setxy random-xcor random-ycor

      ; info
      set age 1
      set age-death people-lifespan

      ; dengue
      set dengue? false
      set transmitter? false
      set days-dengue-incubation 0
      set days-dengue-sick 0
      set dengue-recurrence 0
    ]
  ]
end

; Verifica saúde das pessoas e define se há cura ou morte
to people-checking-health
  let can-die random-float 1
  if transmitter? = true and can-die < 0.3
  [
    set people-count-death-dengue people-count-death-dengue + 1
    die
  ]

  if days-dengue-sick > days-dengue-incubation + days-dengue-viral
  [
    set dengue? false
    set transmitter? false
    set color gray
    set days-dengue-sick 0
  ]
end