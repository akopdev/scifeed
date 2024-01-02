# SciFeed
Create a personalized feed filled with links to research papers from top-notch scientific website.

Feed will be generated in JSON format, which is supported by many RSS readers include NetNewsWire, NewsBlur, ReadKit and Reeder.

> This project is designed to match my personal needs. If you have any suggestions, please feel free to open an issue.

### Supported platforms

- [x] PubMed
- [x] Arxiv
- [x] PapersWithCode
- [x] ResearchGate
- [ ] ScienceDirect


## Installation

For local development, you can run the following command to install dependencies and start the server.

```bash
make init install start
```

Next time you can just run the server.

```bash
make start
```

If you prefer to use docker, you can run the following command.

```bash
make build run
```

