<script lang="ts">
    import { Mandarin } from 'language-flash'
    type Word = {
            pinyin: string;
            traditional: string;
            simplified: string;
            meaning: string;
    }
    type Mode = 'pinyin' | 'traditional' | 'simplified' // TODO: update types when language is customized
    const isModeType = (data: unknown): data is Mode => data === ('pinyin' || 'traditional' || 'simplified');
    let customGui = 0
    let language = 'Mandarin'
    let newLanguage = ''
    let words = Mandarin
    let newWords = ''
    let threshold = 2
    let numberWords = 3
    let mode: Mode = 'pinyin'
    let randomNum = 0 //Math.floor(Math.random() * numberWords)
    let round = 0
    let mastered = false
    let reveal = false
    let cache = [...Array(words.length)].map(_x => 0)
    let unlearnedWords = words.slice(0, numberWords)
    let leftToLearn = numberWords
    let unlearnedIndex = randomNum
    const customize = () => {
      language = newLanguage
      console.log(words);
      words = JSON.parse(newWords)
      unlearnedWords = words.slice(0, numberWords)
      console.log(words);
      
      customGui = 0
    }
    const changeNumberWords = (newNum: number) => {
      numberWords = newNum
      unlearnedWords = words.slice(0, newNum)
      leftToLearn = newNum
    }
    const changeThreshold = (newNum: number) => {
      threshold = newNum
      unlearnedWords = words.slice(0, newNum)
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
        cache[randomNum] += 1
        if (cache[randomNum] === threshold) mastered = true
      }
      else cache[randomNum] = Math.max(0, cache[randomNum] - 1)
      cache = cache
      setTimeout(() => {
        const currentWords = unlearnedWords.map((x: Word[]) => words.indexOf(x))
        const newUnlearned = currentWords.filter((x: any) => cache[x] < threshold)
        // console.log(newUnlearned.length);
        if (newUnlearned.length > 0) {
          leftToLearn = newUnlearned.length
          randomNum = randomNum + 1 > (numberWords * (round + 1)) - 1 ? numberWords * round : randomNum + 1
          unlearnedIndex = findNextUnlearnedIndex(currentWords)
          const newNum = words.find((word: Word) => word === unlearnedWords[unlearnedIndex])
          if (newNum) randomNum = words.indexOf(newNum)
        } 
        else {
          round += 1
          unlearnedWords = words.slice(round * numberWords, (round + 1) * numberWords)
          randomNum = round * numberWords
          unlearnedIndex = 0
          leftToLearn = numberWords
        }
        mastered = false
        reveal = false
      }, 300)
      // console.log(cache, randomNum, unlearnedIndex)
    }
  </script>
  
  <main>
    {#if customGui}
      <div id="info">
        <input title="Language" placeholder="Language" on:change={(e) => newLanguage = e.currentTarget.value} style="margin-bottom: 20px"/>
        <textarea placeholder="New words in valid Json" on:change={(e) => newWords = e.currentTarget.value}  style="margin-bottom: 20px"/>
        <div id="title">
          <button on:click={() => customize()} disabled={!newLanguage || !newWords}>UPDATE</button>
          <button on:click={() => customGui = 0}>CANCEL</button>
        </div>
      </div>
    {/if}
    <div id="info">
      <div id="title">
        <h3>YOU ARE LEARNING:</h3>
        <h3>{language}</h3>
      </div>
      <button style="align-self: center;" on:click={() => customGui = 1}>CUSTOMIZE LANGUAGE</button>
      <div id="title">
        <h3>ROUND:</h3>
        <h3>{round + 1}</h3>
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
        <select value={mode} on:change={e => {if (isModeType(e.currentTarget.value)) mode = e.currentTarget.value}}>
          <option value={'pinyin'}>pinyin</option> 
          <option value={'traditional'}>traditional</option> 
          <option value={'simplified'}>simplified</option>
        </select>
      </h3>
    </div>
  
    <div id="word">
      <h1>{unlearnedWords[unlearnedIndex][mode]}</h1>
      <h2 class={mastered ? 'mastered' : ''}>SCORE: {cache[randomNum]} {#if mastered}&#128170;{/if}</h2>
    </div>
  
    <div id="answer">
      {#if reveal}
        <h3>{unlearnedWords[unlearnedIndex].meaning}</h3>
        <h2>Did you get it right?</h2>
        <button on:click={() => answer(true)}>YES</button>
        <button on:click={() => answer(false)}>NO</button>
      {:else}
        <button on:click={() => reveal = true}>
          REVEAL DEFINITION
        </button>
      {/if}
    </div>
  
    <div>
      <h6>{leftToLearn} words left this round</h6>
    </div>
  </main>
  
  <style>
  
    :root {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
        Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }

    #title {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      width: -webkit-fill-available
    }
  
    #info {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      border: #ff3e00 1px solid;
      max-width: 400px;
      padding: 20px;
      margin-bottom: 20px;
    }
  
    .mastered {
      color: lightgreen;
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

    button:disabled,
    button[disabled] {
      background-color: lightgray;
      color: gray;
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
  