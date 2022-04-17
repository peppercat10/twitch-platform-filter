# Twitch Platform Filter
Simple tool to filter Twitch games by nearly any platform and provide the results as a static HTML page.

Currently being used by [Twitch Filter Server](https://github.com/peppercat10/twitch-filter-server) to refresh https://twitch-platform-filter.herokuapp.com/ periodically.

## **Why?**

When looking to try new games, I often browse Twitch to see what's being played lately. However, I typically want games for a specific platform, e.g. Nintendo Switch, but Twitch does not provide this type of filtering.


## **How it works**

``twitch-filter.py`` asks the user to type a platform name (e.g. Playstation 4). It then tries to match it to known platforms. If the platform exists, it will query GiantBomb API for all games that are playable under that platform and save the results locally as JSON. Afterwards, it queries Twitch API for all games that are currently being streamed and it intersects them with GiantBomb's file, providing the filtered results as JSON.

``html-generator.py`` looks for all filtered results that ``twitch-filter.py`` produced and generates static HTML pages for each of them, with tabs on top to switch between platforms.

## **Requirements**

* Python 3

## **Usage**

1. Add the required API keys to the top of `twitch-filter.py`
2. Run `python twitch-filter.py` in a shell and follow the instructions that appear
3. (Optional) Run `python html-generator.py` to build HTML files for easier reading of the results
