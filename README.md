# [Twitter thread](https://twitter.com/s_pop3/status/1547753107668381696?s=20&t=6MKikkiXNfZwK1LBuewldg) describing the project

i built this app for studying Mandarin vocab words, but it can easily be taylored to any other language you're able to get data for

just import it and pass your data through `props`:

```javascript
<script>
	import LanguageFlash from 'language-flash'
  // data should be an array of objects with the following format: 
  // { word: '', wordModeTwo: '', wordModeThree: '', meaning: '' }
	const promise = fetch('/some/data').then(res => res.json()) 
</script>


{#await promise}
	<LanguageFlash />
{:then vocabData}
	<LanguageFlash vocabData={vocabData} />
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}
```

## Need an official Svelte framework?

Check out [SvelteKit](https://github.com/sveltejs/kit#readme), which is also powered by Vite. Deploy anywhere with its serverless-first approach and adapt to various platforms, with out of the box support for TypeScript, SCSS, and Less, and easily-added support for mdsvex, GraphQL, PostCSS, Tailwind CSS, and more.

```js
// store.js
// An extremely simple external store
import { writable } from 'svelte/store'
export default writable(0)
```
