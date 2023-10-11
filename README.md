# Scifeed
Create a personalized feed filled with links to research papers from top-notch scientific website.

Feed will be generated in JSON format, which is supported by many RSS readers include NetNewsWire, NewsBlur, ReadKit and Reeder.

> This project is designed to match my personal needs. If you have any suggestions, please feel free to open an issue.


## Installation

For the first time, you need to install the dependencies and start the server.

```bash
make init install start
```

Next time you can just run the server.

```bash
make start
```

# Usage

It supports several search engines, including Google Scholar. You can specify the search engine and keyword in the url, 
for example `https://yourdomain.com/scholar?q=deep+learning`. By default, it will return last 50 results sorted by date. 

You can also specify the number of results manually, by adding `&limit=100` to the url.




