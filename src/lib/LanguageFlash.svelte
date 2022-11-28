<script lang="ts">
  type Word = {
    pinyin: string;
    traditional: string;
    simplified: string;
    meaning: string;
  }
  
  export let vocabData: Word[] = [{pinyin:'...loading', traditional:'...loading', simplified:'...loading', meaning:'...loading'}]

  const GREEN = '#4CAF50'
  const LIGHT_GREEN = '#99ee99'
  const RED = '#FF5252'
  const LIGHT_RED = '#ee9999'

  let threshold = 2
  let numberWords = 3
  let mode = 'pinyin'
  let randomNum = 0 //Math.floor(Math.random() * numberWords)
  let round = 0
  let mastered = false
  let reveal = false
  let correct = false
  let incorrect = false
  let cache = [...Array(vocabData.length)].map(x => 0)
  let unlearnedWords = vocabData.slice(0, numberWords)
  let leftToLearn = numberWords
  let unlearnedIndex = randomNum
  const changeNumberWords = (newNum: number) => {
    numberWords = newNum
    unlearnedWords = vocabData.slice(0, newNum)
    leftToLearn = newNum
  }
  const changeThreshold = (newNum: number) => {
    threshold = newNum
    unlearnedWords = vocabData.slice(0, newNum)
    leftToLearn = newNum
  }
  const findNextUnlearnedIndex = (currentWords: number[]) => {
    let index = unlearnedIndex + 1 > numberWords - 1 ? 0 : unlearnedIndex + 1
    while (cache[currentWords[index]] === threshold) {
      if (index + 1 > numberWords - 1) index = 0
      else index += 1
    }
    return index
  }
  const answer = (answer: boolean) => {
    if (answer) {
      reveal = false
      correct = true
      cache[randomNum] += 1
      if (cache[randomNum] === threshold) mastered = true
    }
    else {
      reveal = false
      incorrect = true
      cache[randomNum] = Math.max(0, cache[randomNum] - 1)
    }
    cache = cache
    setTimeout(() => {
      const currentWords = unlearnedWords.map(x => vocabData.indexOf(x))
      const newUnlearned = currentWords.filter((x) => cache[x] < threshold)
      // console.log(newUnlearned.length);
      if (newUnlearned.length > 0) {
        leftToLearn = newUnlearned.length
        randomNum = randomNum + 1 > (numberWords * (round + 1)) - 1 ? numberWords * round : randomNum + 1
        unlearnedIndex = findNextUnlearnedIndex(currentWords)
        const newNum = vocabData.find((word: Word) => word === unlearnedWords[unlearnedIndex])
        if (newNum) randomNum = vocabData.indexOf(newNum)
      } 
      else {
        round += 1
        unlearnedWords = vocabData.slice(round * numberWords, (round + 1) * numberWords)
        randomNum = round * numberWords
        unlearnedIndex = 0
        leftToLearn = numberWords
      }
      mastered = false
      correct = false
      incorrect = false
    }, 300)
    // console.log(cache, randomNum, unlearnedIndex)
  }
  </script>

  <head>
  <link
    rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"
  />
  </head>
  <main>
  <div id="info">
    <div style="display: flex; justify-content: space-between; width: 100%; align-items: baseline;">
      <h3>ROUND: {round + 1}</h3>
      <h6 style="margin: 0px;">{leftToLearn} WORDS LEFT TO MASTER</h6>
    </div>
    <h3>
      STUDYING 
      <select value={numberWords} on:change={e => changeNumberWords(Number(e.currentTarget.value))}>
        <option value={3}>3</option> 
        <option value={10}>10</option> 
        <option value={25}>25</option>
        <option value={50}>50</option>
        <option value={75}>75</option>
        <option value={100}>100</option>
      </select>
      WORDS PER ROUND
    </h3>
    <h3>
      NEED SCORE OF
      <select value={threshold} on:change={e => changeThreshold(Number(e.currentTarget.value))}>
        <option value={1}>1</option> 
        <option value={2}>2</option> 
        <option value={3}>3</option> 
        <option value={4}>4</option>
        <option value={5}>5</option>
        <option value={6}>6</option>
      </select>
      TO MASTER A WORD
    </h3>
    <h3>
      MODE:
      <select value={mode} on:change={e => {mode = e.currentTarget.value}}>
        <option value={'pinyin'}>pinyin</option> 
        <option value={'traditional'}>traditional</option> 
        <option value={'simplified'}>simplified</option>
      </select>
    </h3>
  </div>

  <div id="word">
    <h1 style="grid-column-start: 2; margin-bottom: 0px;" class={mastered ? 'mastered' : ''}>{unlearnedWords[unlearnedIndex][mode]}</h1>
    {#if mastered} 
      <h1 style="margin: 0px;" class="animate__animated animate__fadeOutUp">&#128170;</h1>
    {/if} 
    <h2 id="current-score">
      SCORE: <span id="score-number">{cache[randomNum]}</span>
    </h2>
    <span id="point-marker">
      {#if correct}
        <h4 class="animate__animated animate__fadeOutUp" style={`color: ${GREEN}; margin: 0px;`}>+1</h4>
      {:else if incorrect}
        <h4 class="animate__animated animate__fadeOutUp" style={`color: ${RED}; margin: 0px;`}>-1</h4>
      {/if}
    </span>
  </div>

  <div
    id="answer"
    style="min-height: 200px; display: flex; flex-direction: column; justify-content: space-evenly;"
  >
    {#if reveal}
      <h3
        class="animate__animated animate__fadeIn"
        style="margin: 0px 20px; align-self: center;"
      >
        {unlearnedWords[unlearnedIndex].meaning}
      </h3>
      <button
        class="animate__animated animate__fadeInUp" 
        style={`
          border-color: ${GREEN};
          background-color: ${LIGHT_GREEN};
          color: #000;
          align-self: center;
        `}
        on:click={() => answer(true)}
      >
        CORRECT
      </button>
      <button
        class="animate__animated animate__fadeInUp"
        style={`
          border-color: ${RED};
          background-color: ${LIGHT_RED};
          color: #000;
          align-self: center;
        `}
        on:click={() => answer(false)}
      >
        INCORRECT
      </button>
    {:else if !incorrect && !correct}
      <button
        class="animate__animated animate__fadeInUp"
        on:click={() => reveal = true} style="align-self: center;"
      >
        DEFINITION
      </button>
    {/if}
  </div>
  </main>

  <style>

  :root {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
      Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  }

  #word {
    display: grid;
    line-height: 36px;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(2, 1fr);
    margin: auto;
    width: fit-content;
  }

  #current-score {
    grid-row-start: 2;
    grid-column-start: 2;
    grid-column-end: 3;
  }

  #point-marker {
    grid-row-start: 2;
    grid-column-start: 3;
    grid-column-end: 4;
    text-align: left;
  }

  #info {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    border: #ff3e00 1px solid;
    max-width: 400px;
    padding: 20px;
  }

  .mastered {
    text-decoration: line-through 2px;
  }

  button {
    font-family: inherit;
    font-size: inherit;
    padding: 1em 2em;
    color: #ff3e00;
    background-color: rgba(255, 62, 0, 0.1);
    border-radius: 2em;
    border: 2px solid rgba(255, 62, 0, 0);
    outline: none;
    width: 200px;
    font-variant-numeric: tabular-nums;
    cursor: pointer;
  }

  main {
    text-align: center;
    padding: 1em;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
  }

  /* img {
    height: 16rem;
    width: 16rem;
  } */

  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4rem;
    font-weight: 100;
    line-height: 1.1;
    margin: 2rem auto;
    max-width: 14rem;
  }

  @media (min-width: 480px) {
    h1 {
      max-width: none;
    }
  }
</style>
