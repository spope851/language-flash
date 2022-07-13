<script>
  // import logo from './assets/svelte.png'
  import words from './data/words.json'
  const THRESHOLD = 2
  const NUMBER_WORDS = 3
  let randomNum = 0 //Math.floor(Math.random() * numberWords)
  let reveal = false
  let cache = [...Array(words.length)].map(x => 0)
  let unlearnedWords = words.filter((_x, i) => cache[i] < THRESHOLD)
  let leftToLearn = unlearnedWords.length
  let unlearnedIndex = randomNum
  const answer = (/** @type {boolean} */ answer) => {
    if (answer) cache[randomNum] += 1
    else cache[randomNum] = Math.max(0, cache[randomNum] - 1)
    console.log(words.length, unlearnedWords.length, randomNum);
    cache = cache
    console.log(cache)
    unlearnedWords = words.filter((_x, i) => cache[i] < THRESHOLD)
    randomNum = randomNum === NUMBER_WORDS + (words.length - unlearnedWords.length) - 1 ? (words.length - unlearnedWords.length) : randomNum + 1
    unlearnedIndex = randomNum - (words.length - unlearnedWords.length)
    leftToLearn = unlearnedWords.length
    reveal = false
  }
</script>

<main>
  <div id="word">
    <h1>{unlearnedWords[unlearnedIndex].pinyin}</h1>
  </div>

  <div id="answer">
    {#if reveal}
      <h3>{unlearnedWords[unlearnedIndex].meaning}</h3>
      <h2>Did you get it right?</h2>
      <button on:click={() => answer(true)}>YES</button>
      <button on:click={() => answer(false)}>NO</button>
    {:else}
      <button on:click={() => reveal = true}>
        REVEAL
      </button>
    {/if}
  </div>

  <div>
    <h6>{leftToLearn} words left to learn</h6>
  </div>
</main>

<style>

  :root {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
      Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
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

  p {
    max-width: 14rem;
    margin: 1rem auto;
    line-height: 1.35;
  }

  @media (min-width: 480px) {
    h1 {
      max-width: none;
    }

    p {
      max-width: none;
    }
  }
</style>
