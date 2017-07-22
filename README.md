# wiki_game
Players start on the same randomly selected article and must navigate to another pre-selected article (home) only use links within the current article. The goal is to arrive at the home article in the fewest number of links or the least time.

The solution uses the BeautifulSoup library to perform webscraping of the links in web pages and graphs to find the paths between the links

The main function receives 3 parameters: start URL, target URL and a maximum number of links to visit and returns an object containing the links found between the given entries.

For example, to find the links between:

Start: "https://en.wikipedia.org/wiki/Fyodor_Dostoyevsky"
End: "https://en.wikipedia.org/wiki/Medieval"

And analyze maximum 500 links, use the function as follows: 

WikiGame (start, end, 500).
