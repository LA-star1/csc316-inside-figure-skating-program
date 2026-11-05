# Inside a Figure-Skating Program

A CSC316 prototype built with Vite, Svelte 5, and D3. It explores the official Beijing 2022 men's singles top-ten scoring protocols and presents a separate generic 3D jump reference.

## Live site

Open the public prototype at [inside-figure-skating-program.eagercoast2.chatgpt.site](https://inside-figure-skating-program.eagercoast2.chatgpt.site/). No local server is needed.

## Run locally

```sh
npm install
npm run data:prepare
npm run test
npm run dev
```

The source is [`data/source/Beijing_2022_Mens_Singles_Top10_Data_Brief.md`](data/source/Beijing_2022_Mens_Singles_Top10_Data_Brief.md), based on the [official ISU event results](https://results.isu.org/results/season2122/owg2022/) and [results book](https://www.isuresults.com/results/season2122/owg2022/owg2022_protocol.pdf). The embedded 3D demo is an illustrative reference, not a recording or reconstruction of an Olympic skater.

The project intentionally keeps official scoring records separate from motion references. Protocol element order is not a timestamp or rink location. The cohort contains the final top ten only.
