# flickr-2048p-picture-downloading
For users downloading 2048p photos, which is the most fitted size picture for computer.

First, you need to have flickr account, and apply for your own flickr api. Because we will use the api keys when downloading pictures.
Flickr api application tutorial can be found in YouTube.

Second, after applying flickr api, you should download and import this package in your python. example below:
import flickrdownload as flk

Owing to the package design, the creation of this package is based on several common packages in python. You can use .helps and .packages to see the detail.
You must have these packages as basis so that this packages can be operable.

Next, using the .loginFLK() method, entering your api keys and your computer storage path. (storage path should be entered like:  C:\\xxxx\\xxxx\\......, rather than C:/xxxx/xxxx/....)

Following, You are able to employ the download format below. We have downloading multiple albums, downloading single album, downloading respective pictures and violent crawling methods.
1. downloading multiple albums: You can enter several album links, and when you finish entering one link, you should press enter. After finishing entering, you must enter '-1'. (.download_multiple_albums())
2. downloading single albums: Enter single album link, and the download will start. (.download_single_album())
3. downloading respective album: You should use this method to download pictures, when your target pictures scatter in the album or this album is required membership to see. (.download_respective_photo())
4. violent crawling: Downloading picture via raw web crawling rather than using flickrapi. This method is not recommended.

Error results or no error but no pucture be downloaded or no error but not every picture be downloaded:
1. You got the false link. Links must include the words 'album' rather than 'sets'
2. The pictures in this album do not reach 2048p.
3. Some of the pictures in this album are public, but the others are only for membership.
4. Album editors do not provide other users with downloading. In this way, you can use the method 'downloading respective album'.
