

# CorpusGenius.

_____

## 

[TOC]

_____

## What is CorpusGenius ? 

Hey! :wave:  

Glad you asked, while performing a corpus based analysis on artist Bob Dylan, I quickly noticed that there wasn't a single, updated file containing all the lyrics.   
In comes CorpusGenius, a robust solution to generate a Corpus containing (along with other meta files, below)  lyrics by user-specified artist, scrapped from Genius.com using genius's API and John W. Miller's *lyricsgenius* wrapper.

Since, rather than skipping directly to lyrics for a song, it follows a waterfall model by going from :

All Albums --> All songs by albums + unreleased/EPs/Misc songs --> Lyrics by each song --> Final corpus.

Thus, by using this python script you'll be able to download:

1) A CSV file containing all albums released by artist
2) A CSV file containing all tracks, both by albums and individual song not released as albums.
	*Such as EPs,demos,bootlegs/singles/live performances/specials/etc.*
3) A CSV file containing songs sung/released/performed but **NOT** written by the specified artist, along with their original
songwriters and the album it originally appears on for the specified artist in question
4) A CSV file containing lyrics of all songs
5) A CSV file containing lyrics of all songs released by year
6) A CSV file containing a single corpus of all songs stored in one single cell of csv file

_____

## Getting Started 

pass

_____

## Requirements 

pass

_____

## Author 

Jatan Pandya / 2020

_____

## Running 









_____

## License

Please see LICENSE.md for more details. 

_____

## Acknowledgments

> If I have seen further it is by standing on the shoulders of Giants. 
> 														*-Isaac Newton*

John W. Miller for his excellent lyricsgenius wrapper.

Authors, countless contributors for the various modules used in the project.