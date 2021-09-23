---
layout: null
---

// Set options for simple search
SimpleJekyllSearch({
    searchInput: document.getElementById('search-input'),
    resultsContainer: document.getElementById('results-container'),
    json: '{{site.baseurl}}/assets/simple-jekyll-search/search.json',
    searchResultTemplate: '<li><a href="{url}" title="{title}">{title}</a></li>',
    // fuzzy: fuzzy search strategy,
    // literal: searches for the term,
    // word: Matches only complete words.
    // /Adiding a comment to commit again this file    
    strategy: 'literal',
    limit: 30
})
