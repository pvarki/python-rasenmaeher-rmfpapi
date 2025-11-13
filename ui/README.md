# Fake Product Module Federation Component

## Reference Information

In the fake product UI, a federated component is definedthrough module federation + vite. In the wider `docker-rasenmaher-integration` context, a shared docker volume `ui_files` backs access to federated components (or other modular UI data).

**In production and local modes:**

`Dockerfile`:
- Build vite UI (into `ui/dist`)
- Copy `ui/dist` into `ui_build`
`entrypoint.sh`:
- Copy `ui_build` into docker volume `ui_files/{shortname}`

The last step is important for changes to the UI to reflect new builds without the need to recreate volumes in between each build. In development mode, the `entrypoint.sh` script is not used, and the step of copying to the docker volume is added to the `command` in the docker compose file (in `docker-rasenmaher-integration`, `docker-compose-dev.yaml`).

For an integration's UI to work correctly, naming must be consistent. The shortname needs to be consistent between the API URL and the directory where the UI is stored within the docker volume (and hence the address where it is served through nginx). For this project, as an example, the shortname is "fake".

## Development

While the federated component works both in rmlocal and rmdev, it is recommended to seperately develop the component. This is partly because the federated component is only built when rmlocal/rmdev is built and hence doesn't currently update in real time.

**Install dependencies and start the dev server**

```bash
pnpm install
pnpm dev
```

Component runs locally at: [http://localhost:4174/](http://localhost:4174/)

## Assets

Place assets in the `public/` folder, for example:

```
public/taistelija.png
```

When using these assets in code **always** prefix them with `/ui/{shortProductName}/`. for example:

```
/ui/fake/taistelija.png
```

This is required due to how things are included in the production. `vite.config.ts` rewrites the routes for local development.



## Sample Data

For developing components it is recommended to manually fetch the user data from the api, for example:

```
https://localmaeher.dev.pvarki.fi:4439/api/v2/instructions/data/fake
```

Paste the entire response into `src/main.tsx` as the value of `SAMPLE_DATA`.

It is recommended to test what happens if no data is passed.

## Styles

`src/index.css` should reflect the styles of the main UI. It could be outdated, so it might be worth while to copy the file from the main UI here every once in a while.

This file is **not** included in the production build. It is only used to make local development possible. In production the styles of main UI are used.
