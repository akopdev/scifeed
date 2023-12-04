# SciFeed
Create a personalized feed filled with links to research papers from top-notch scientific website.

Feed will be generated in JSON format, which is supported by many RSS readers include NetNewsWire, NewsBlur, ReadKit and Reeder.

> This project is designed to match my personal needs. If you have any suggestions, please feel free to open an issue.

### Supported platforms

- [x] Google scholar
- [x] PubMed
- [x] Arxiv
- [x] PapersWithCode
- [ ] ResearchGate
- [ ] Nature
- [ ] Science
- [ ] ScienceDirect


## Installation

For the first time, you need to install the dependencies and start the server.

> You still need to install azure functions environment manually  on your machine. Please refer to 
> [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Ccsharp%2Cbash#v2) for more details.

```bash
make init install start
```

Next time you can just run the server.

```bash
make start
```

