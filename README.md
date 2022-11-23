### [Twitter thread](https://twitter.com/s_pop3/status/1547753107668381696?s=20&t=6MKikkiXNfZwK1LBuewldg) describing the project

I built this app for studying Mandarin vocab words, but it can easily be tailored to any other language you're able to get data for

just import it and pass your data through `props`:

```javascript
<script>
	import LanguageFlash from 'language-flash'
  // data should be an array of objects with the following structure: 
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
