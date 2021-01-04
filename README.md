

# CorpusGenius.

_____

- [CorpusGenius.](#corpusgenius)
  * [What is CorpusGenius ?](#what-is-corpusgenius--)
  * [Requirements](#requirements)
  * [Getting Started](#getting-started)
  * [Running](#running)
  * [Author](#author)
  * [License](#license)
  * [Acknowledgments](#acknowledgments)
  * [FAQs or Why the CSVs are the way they are](#faqs-or-why-the-csvs-are-the-way-they-are)
    + ["artist_name"_albums.csv :](#-artist-name--albumscsv--)
    
    + ["artist_name"_tracks.csv :](#-artist-name--trackscsv--)
    
    + ["artist_name"_lyrics.csv :](#-artist-name--lyricscsv--)
    
    + ["artist_name"_lyrics_by_years.csv :](#-artist-name--lyricsbyyearscsv--)
    
    + [songs_not_by_"artist_name".csv](#songs-not-by--artist-name-csv)
    
    + ["artist_name"_corpus.csv](#-artist-name--corpuscsv)
    
      



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

## Requirements 

pass

_____

## Getting Started 

pass

_____

## Running



_____

## Author 

Jatan Pandya / 2020 



_____

## License

Please see LICENSE.md for more details. 

_____

## Acknowledgments

> If I have seen further it is by standing on the shoulders of Giants. 
> 														*-Isaac Newton*

John W. Miller for his excellent lyricsgenius wrapper.

Authors, countless contributors for the various modules used in the project.

_______

## FAQs or Why the CSVs are the way they are 

Say we are interested in generating a corpus for Artist : Bob Dylan.

1. ### "artist_name"_albums.csv : 

   CSV file thus generated will contain albums in fashion:

   ```
   year,   album title,                                                            album id
   1962,   Bob Dylan,                                                              26515
   1963,   The Freewheelin’ Bob Dylan,                                             17327
   1964,   The Times They Are A-Changin’,                                          28249
   1964,   Another Side of Bob Dylan,                                              25519
   1965,   Highway 61 Revisited,                                                   13573
   .                   .                                                            .
   .                   .                                                            .
   .                   .                                                            .
   2019,   The Rolling Thunder Revue: The 1975 Live Recordings (Sampler),          648356
   --------------------------------------snip--------------------------------------------
   ```

   A further note ::

   For albums that have no release info. on Genius.com will be set as "N/A" (Not available) -->

                                           --------------------------------
                                           year,   album title,    album id
                                           N/A     xxxxxxxxxxxx    xxxxxxxx
                                           -------------snip---------------
   You'll notice that along with studio albums, the CSV also contains various bootlegs/alternate albums/
   albums that are compilations of Live performances, Outtakes, special releases etc.

   Granted, these albums will contain more or less of the same songs, and would be thought of as duplicates. The
   reason
   these are included is because more often or not, it's a common fact that:
               / Bootlegs/demos etc. are often unfinished versions of final songs. Lyrically they are a rich source of
               alternate lyrics. Hence should not be excluded as it'll affect the final corpus.
               / For the same reason Outtakes/Live performances are not excluded as artists usually change lyrics on
               the fly.
               Hence,should not be excluded as it'll affect the final corpus.
   Lastly, Genius.com is a ever-changing website. A single word change for a song that is a live song will make
   it a unique song.

2. ### "artist_name"_tracks.csv :

   Firstly it will find all songs by EACH album released by the artist, including box-sets/alternate albums/
   special/bootlegs/live etc like -->

   ```
   album title,                                                       song title,        	song id
   Under the Red Sky,                                                 10,000 Men,        	200681
   Under the Red Sky,                                                 2 X 2,              	200682
   Blonde on Blonde,                                                  4th Time Around,    	105774
   Dylan (1973),                                                      A Fool Such as I,   	199634
   "The Bootleg Series, Vol. 9: The Witmark Demos: 1962-1964",        A Hard Rain’s ...,	105186
   Bob Dylan’s Greatest Hits Vol. II ,                                A Hard Rain’s ...,	105186
   -----------------------------------------------------snip--------------------------------------------
   ```

   ##### Further it isn't necessary that each song that releases is only through albums. As an example, consider an artist from India that happens to be Most recorded artist in music history, Asha Bhosle.// source : https://bit.ly/2LZlRcE It may seem finding songs by albums should be enough. But it isn't. Song information is saved more broadly on genius.com and not just by albums. For example, for Asha Bhosle, there are only 4 Albums available on genius.com (partly because in India, songs are released as OST albums for the movie they were featured in rather than a separate album by the artist,Nonetheless, the list is incomplete for our purposes!) If just try to find songs by albums, we will have just 3 songs by Asha Bhosle, which is obviously nowhere near the real number (11,000 Songs at least). Thus It is important to search for uncategorized songs and append them to the final list. Also, songs can be released as EPs/demos/singles etc. Hence those songs too, should not be discarded. (So, even though there will be songs of same title or close, they are different. If not, they will be discarded later.)

   For example after considering the edge case, above list of songs by Bob Dylan will look something like this (along  with their 'years' (not shown here)

   ```
   album title,                                         song title,                song id
   N/A,                                                 "10,000 Men",               200681
   Under the Red Sky,                                   "10,000 Men",               200681
   Under the Red Sky,                                    2 X 2,                     200682
   N/A,                                                  2 X 2,                     200682
   N/A,                                                  32-20 Blues,               1686914
   N/A,                                                  4th Time Around,           105774
   Blonde on Blonde,                                     4th Time Around,           105774
   Dylan (1973),                                         A Fool Such as I,          199634
   N/A,                                                  A Fool Such as I,          199634
   N/A,                                                 900 Miles from My Home,     1994655
   -----------------------------------------------------snip--------------------------------------------
   ```

   For songs that have no album info. on Genius.com will be set as "N/A" (Not available)

3. ### "artist_name"_lyrics.csv :

   CSV file thus generated will contain lryics by each song in fashion:

   ```
   song title                                        lyrics
   ----------------------------------------snip-----------------------------------
   .                                                                     .
   .                                                                     .                                     
   A Hard Rain’s  A-Gonna Fall [Gaslight 1962],       {
                                                      Oh, where have you been, my blue
                                                      -eyed son? . . .
                                                      I’ve stepped in the middle of seven 
                                                      sad forests I’ve been out in front 
                                                      of a dozen dead oceans I’ve been 
                                                      ten thousand miles in the mouth of 
                                                      a graveyard . . .
                                                      }                                                  
   .                                                                      .
   .                                                                      .
   ----------------------------------------snip-----------------------------------
   ```

   Songs that are repeated will be added to the adjacent cell. This is because, even if the songs do have
   same title, it is possible that the lyrics can be different. As we saw, since artist change lyrics for songs in
   the live performances, it's necessary two songs with same songs similar. Next, again since genius.com is an
   ever-changing website, i.e. anytime a song's lyrics is changed, it will result in a new lyrics for that song and hence a different corpus in the end! And suppose if the two songs appended are completely same, they will be discarded since.

4. ### "artist_name"_lyrics_by_years.csv:

   This CSV file contains lyrics by album tracks for each album by year. For example, considering Bob Dylan's discography:

   ```
   year,            all_lyrics
   -----------------------------------------------------snip--------------------------------------------
   .                         .
   .                         .
   1966,        {'Well, your railroad gate, you know I just cant jump it Sometimes
   			it gets so hard, you see I just sitting here beating on my trumpet 
   			With all these promises you left for me But where are you tonight, 
   			sweet Marie?  Well, I waited for you when I was half sick Yes, I 
   			waited for you when you hated me. Well, I waited for you inside of 
   			the frozen traffic Yeah, when you knew I had some other place to be Now, 
   			where are you tonight sweet Marie? Well, anybody can be just like me, 
   			obviously But then, now again, not too many can be like you, fortunately  
   			Well, six white horses that you . . . 
   			". . . and lyrics of all other songs released in the year 1966"
               }
   .
   2020,        { 			   
   								.
   								.
                }
   -----------------------------------------------------snip-------------------------------------------
   ```

5. ### songs_not_by_"artist_name".csv

   This CSV file containing exactly the subset of songs that are NOT written by the artist. Along with the title of the song, the csv file will also contain the original songwriter and the album it appears on for artist in question.

   ```
   song title                  album title & original song writer (if available)
   Mr. Bojangles,              "['N/A', {'Jerry Jeff Walker'}]","['Dylan (1973)', {'Jerry Jeff Walker'}]"
   -----------------------------------------------------snip-------------------------------------------
   ```

   Thus here song "Mr. Bojangles" :

   1. Is written by Jerry Jeff Walker and not Bob dylan.

   2. But, recorded nonetheless on album Dylan (1973)

   3. It is repeated twice since the song "Mr Bojangles" appears twice on the final song csv file

   4. There is also a version of Mr.Bojangles on genius.com that doesn't have required info. hence set to "N/A"

      For songs that have no album info. or song-writer info. on Genius.com will be set as "N/A" (Not available)

6. ### "artist_name"_corpus.csv

   Finally the CSV file containg all the lyrics all the songs attached back to back and stored in a single cell.

   #### Note : If using Excel as your CSV reader, since Excel cannot read more than 32767 characters in a single cell, it might erroneously show words in random cells. If that happens use notepad etc. to view.

   