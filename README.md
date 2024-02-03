[![CircleCI](https://dl.circleci.com/status-badge/img/circleci/BbJs9oTbCH7LLiezNiXJW9/D3eKhPg3Et8a8GG6FsKHdm/tree/circleci-project-setup.svg?style=svg&circle-token=73d7f4adbdef23fd686693309f97ac8e72424183)](https://dl.circleci.com/status-badge/redirect/circleci/BbJs9oTbCH7LLiezNiXJW9/D3eKhPg3Et8a8GG6FsKHdm/tree/circleci-project-setup)
![example workflow](https://github.com/mxli417/graphpak/actions/workflows/python-package.yaml/badge.svg?branch=master)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
# graphpak - building knowledge graphs (quick and dirty)

This package aims to evolve into a handy tool for building knowledge graph - like
structures from different text sources, fast, unsupervised and reusable in various
downstream tasks. 

Its initial version is intended as a very simple and heuristic tool for approaching
this task for German text sources (not yet linking all entities). The package provides 
a very simple visualization tool (building on pandas, networkx and matplotlib) and 
a serializer to dump collected data into csv files.

The core of the package relies on spacy and the publicly available german models
that spacy provides. To make use of the tool, spacy must be installed alongside 
the `de_core_news_sm` model.

In future iterations, less heuristic and more model-driven approaches will be made
available building upon open-source software, research materials and papers. The goal
will be to provide a lightweight, reusable and accessible tool for various downstream
purposes.

## Example command line use:

```bash
graphpak --text "Ich heiße Julian und ich habe eine Katze, deren Name ist Jenny. Jenny jagt gerne Vögel."
```

Would yield the not yet perfect result:

![Example command line graph plot result](./assets/example.png)

Build start: January 2024
