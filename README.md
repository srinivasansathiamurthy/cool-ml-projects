# cool-ml-projects 🚀

Has cool stuff, and stuff needed to build more cool stuff. When you add projects, please add a short high level description of what it does here:

1. DMOCOPS: pretty modular script that allows you to run llm/etc operations on data on scale. Connected to lambda labs & s3: the scale comes from distributing the tasks across however many gpus you wish, and there's proper batch management if some gpus fail/etc. Easy to refactor for various batch management strategies.
2. DMTCS: google vision document text extraction model connected to gpt4o-mini. Scrappy DONUT w/ decision making abilities? Something like that.
3. ARAGOG: web crawler with SENTIENCE
4. DOM-INIC: extracting dom graph + metadata for use in cross-sites navigations

Key points (PLEASE READ):

1. Put all your keys at the head of each ipynb file, or in a .json file called "keys.json". When uploading scripts, remove all keys at the head block of the ipynb files, and do not upload keys.json to github. The gitignore will take care of not adding keys.json or .ipynb checkpoints, but it's on you to remove the keys in the head block of ipynb files.
