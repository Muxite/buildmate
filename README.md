# buildmate
An AI accelerated build and dependency system helper plugin. Made during DubHacks 2025



## running extension locally

1. in root directory run `docker-compose up --build buildmate-server`
2. in buildmate-extension directory `npm run compile`
3. OPEN ONLY THE BUILDMATE-EXTENSION FOLDER in VSCode
4. open `extension.ts` and hit `F5`. this will open a new instance of VSCode with the `buildmate` extension enabled
4a. Write some C code!
5. `ctrl + shift + P` then search for `buildmate: compile`, then run it
6. Location of exe will be shown in lower right-hand corner