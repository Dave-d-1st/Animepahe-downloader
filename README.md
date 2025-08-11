# Animepahe-downloader
A script that downloads anime from animepahe.ru

---

Install the requirements first

`pip install -r requirements.txt`

---

Then run the script to get the download links (**anime.txt**)
`python anime.txt`

You would be prompted to enter the anime name, first episode and last episode. 
Then it searches for the anime and prompts you to pick the anime you want to download.
After this it automatically gets the download links and write it to links.json and download it afterwards.

---

You can set if the links to append to the old links or if it should overwrite the old links by passing --should_append or -sa args(it defaults to False)
`python anime.txt --should_append true`

---

Incase you have already gotten the links but during download it paused just run only the download file
`python download.py`
This will download without having getting the links again