"""
Author : Jatan Pandya (jpandya)
University of Massachusetts - Amherst

File : corpusgenius.py

Generating a Corpus of all the lyrics by user-specified artist, scrapped from Genius.com using genius's API and
lyricsgenius wrapper.

By using this script you'll be able to download following files for you specified artist:
1) CSV file containing all albums released by artist
2) CSV file containing all tracks, both by albums and individual song not released as albums.
Such as EPs,demos,bootlegs/singles/live performances/specials/etc.
3) CSV file containing songs sung/released/performed but NOT written by the specified artist, along with their original
songwriters and the album it originally appears on for the specified artist in question.
4) CSV file containing lyrics of all songs
5) CSV file containing lyrics of all songs re-leased by year.
6) CSV file containing a single corpus of all songs stored in one single cell of csv file.

All the data will be fetched from genius.com
"""

# importing necessary modules

import csv
import time
from collections import defaultdict
from difflib import SequenceMatcher

from unidecode import unidecode
import lyricsgenius
import pandas as pd
from colorama import Fore, Style, init
from requests.exceptions import Timeout


def create_csv(data_structure, fav_filename):
    """
function create_csv is a robust solution to create csv files for any other function that returns as a csv file
can be thought of as a factory that various functions call when they need to return a CSV.
function can handle either a list or dict as an input
:param data_structure: last data structure that the function is done generating and is required to be exported as
csv.
:type data_structure: list or dict. handled appropriately based on the type as it checks for the
:param fav_filename: name user would like to save the csv file as
:type fav_filename: str
:return: a CSV file : encoding = 'utf-8'
:rtype: a CSV File : csv_file with name as specified in fav_filename

Example : calling create_csv(data_structure=type(list),fav_filename="Dylan_albums.csv")
will return a file with name "Dylan_albums.csv" with it's values (here all albums) as a comma
separated file (csv file)

"""

    csv_file = None  # scope initialization

    # in-order for this function to be robust in creating a csv that is
    # uniform in all respects, incoming data_structure will be test for
    # it's type, and then handled accordingly.

    if isinstance(data_structure, dict):
        csv_file = (
            pd.DataFrame(data_structure)
            .transpose()
            .to_csv(fav_filename, encoding="utf-8")
        )
    elif isinstance(data_structure, list):
        csv_file = pd.DataFrame(data_structure).to_csv(
            fav_filename, index=False, encoding="UTF-8"
        )
    else:
        print(
            "function create_csv handles arguments of only type list and dict and not of type:",
            type(x),
        )
    return csv_file


def artist_albums(genius_artist_id):
    """
:param genius_artist_id: unique number that genius.com assigns to each of their artist.
:type genius_artist_id: type int
:return: a csv file containing title of all albums available on genius.com along with their release Date
and genius_album_id & the filename it is saved as
:rtype: CSV file (None type) and type str for file_name

Example : Say we want to download all albums (available on genius.com) released by artist bob dylan.
Hence, calling artist_alubms(genius_artist_id=181) since bob dylan's artist_id is 181.
it will return all albums released by bob dylan (sorted by year) in fashion ::
(taken directly from the generated csv)

year,   album title,                                                            album id
1962,   Bob Dylan,                                                              26515
1963,   The Freewheelin’ Bob Dylan,                                             17327
1964,   The Times They Are A-Changin’,                                          28249
1964,   Another Side of Bob Dylan,                                              25519
1965,   Highway 61 Revisited,                                                   13573
1965,   Bringing It All Back Home,                                              17399
1966,   Blonde on Blonde,                                                       26024
1967,   John Wesley Harding,                                                    24337
1967,   Bob Dylan’s Greatest Hits,                                              539539
.                   .                                                            .
.                   .                                                            .
.                   .                                                            .
2017,   Triplicate,                                                             328059
2017,   The Bootleg Series Vol. 13: Trouble No More 1979–1981,                  398101
2018,   "The Bootleg Series Vol. 14: More Blood, More Tracks",                  466127
2019,   "The Bootleg Series Vol. 15: Travelin’ Thru, 1967–1969",                646838
2019,   The Rolling Thunder Revue: The 1975 Live Recordings (Sampler),          648356
--------------------------------------snip--------------------------------------------

and will be appropriately saved as Dylan_albums.csv

A further note ::

For albums that have no release info. on Genius.com will be set as "N/A" (Not available) -->

                            {--------------------------------
                            year,   album title,    album id
                            N/A     xxxxxxxxxxxx    xxxxxxxx
                            -------------snip---------------}

You'll notice that along with studio albums, the CSV also contains various bootlegs/alternate albums/
albums that are compilations of Live performances, Outtakes, special releases etc.

Granted, these albums will contain more or less of the same songs, and would be thought of as duplicates. The
reason
these are included is because more often or not, it's a common fact that:
            // Bootlegs/demos etc. are often unfinished versions of final songs. Lyrically they are a rich source of
            alternate lyrics. Hence should not be excluded as it'll affect the final corpus.
            // For the same reason Outtakes/Live performances are not excluded as artists usually change lyrics on
            the fly.
            Hence,should not be excluded as it'll affect the final corpus.
Lastly, Genius.com is a ever-changing website. A single word change for a song that is a live song will make
it a unique song.
"""
    # initializing album_set as set() to hold list of albums along with their
    # meta information
    albums_set = set()
    # searching and initializing total number of pages in which artist's albums
    # are stored on genius.com

    total_pages = genius.artist_albums(genius_artist_id, per_page=50, page=1)[
        "next_page"
    ]

    if total_pages is None:
        total_pages = (
            0  # if None, zero. i.e, all the albums are available on first page itself
        )

    for curr_page in range(
        1, total_pages + 2
    ):  # iterate over total number of pages to traverse i.e from page 1 to total_pages
        artist_album = genius.artist_albums(
            artist_id=genius_artist_id, per_page=50, page=curr_page
        )  # search for albums on the current page
        # dive deep into the data_structure and extract useful info.
        for master_value in artist_album.values():
            if isinstance(master_value, list):
                for entry in master_value:
                    # Not all albums have their release date info, if they
                    # do --> store album along with their release year and
                    # genius Id (will be useful later)
                    if entry["release_date_components"] is not None:
                        res = [
                            (("year", str(
                                entry["release_date_components"]["year"]),), ("album title", unidecode(
                                    entry["name"])), ("album id", entry["id"]),)]
                        albums_set.update(res)

                    # if year info. not available, set it to "N/A" (NOT
                    # AVAILABLE)
                    else:
                        res = [
                            (
                                ("year", "N/A"),
                                ("album title", unidecode(entry["name"])),
                                ("album id", entry["id"]),
                            )
                        ]
                        # keep on updating the set.
                        albums_set.update(res)

    albums_list = sorted(
        [dict(album_set) for album_set in albums_set], key=lambda key: key["year"]
    )  # sort chronologically , by release year
    file_name = first_last[-1] + "_albums.csv"
    print(
        f"List of albums generated. (Number of albums : {len(albums_list)}) Now exporting to "
        f"CSV as {Fore.BLUE}{file_name}{Style.RESET_ALL}")
    artist_album_csv = create_csv(
        albums_list, file_name)  # export data as a CSV

    return artist_album_csv, file_name


def album_tracks(all_albums_csv):
    """
:param all_albums_csv: file_name of the csv file containing all albums by specified artist.
(For contents or the fashion it is stored as , see doc. for artist_albums.)
:type all_albums_csv: str
:return: a CSV file containg all tracks by the sepcified artist & the file_name it is stored as
:rtype: a final CSV file (None type) and str type for the file_name

Examples: Continuing from above example, Now that we have a CSV file that includes all albums released by Bob
Dylan:
calling album_tracks(all_albums_csv='Dylan_albums.csv') will return CSV file of all the songs by each album AND all
other songs that are uncategorized on genius.com (more about this edge case in a second)

Firstly it will find all songs by EACH album released by the artist, including box-sets/alternate albums/
special/bootlegs/live etc like -->

album title,                                                                   song title,                song id

Under the Red Sky,                                                             "10,000 Men",              200681
Under the Red Sky,                                                             2 X 2,                     200682
The Bootleg Series Vol. 8: Tell Tale Signs: Rare and Unreleased 1989–2006,     32-20 Blues,               1686914
Blonde on Blonde,                                                              4th Time Around,           105774
Dylan (1973),                                                                  A Fool Such as I,          199634
"The Bootleg Series, Vol. 9: The Witmark Demos: 1962-1964",                    A Hard Rain’s A-Gonna Fall,105186
Bob Dylan’s Greatest Hits Vol. II ,                                            A Hard Rain’s A-Gonna Fall,105186
The Bootleg Series Vol. 7: No Direction Home: The Soundtrack,                  A Hard Rain’s A-Gonna Fall,105186
"The Bootleg Series Vol. 5: Bob Dylan Live 1975, The Rolling Thunder Revue",   A Hard Rain’s A-Gonna Fall,105186
The Freewheelin’ Bob Dylan,                                                    A Hard Rain’s A-Gonna Fall,105186
"The Bootleg Series Vol. 6: Bob Dylan Live 1964, Concert at Philharmonic Hall",A Hard Rain’s A-Gonna Fall,105186
----------------------------------------------snip---------------------------------------------------------------

(So, even though there will be songs of same title or close, they are different. If not, they will be
discarded later.)

Further it isn't necessary that each song that releases is only through albums.
As an example, consider an artist from India that happens to be Most recorded artist in music history, Asha Bhosle.
// source : https://bit.ly/2LZlRcE

It may seem finding songs by albums should be enough. But it isn't. Song information is saved more broadly on
genius.com and not just by albums. For example, for Asha Bhosle, there are only 4 Albums available on genius.com
(partly because in India, songs are released as OST albums for the movie they were featured in rather than a
separate album by the artist,Nonetheless, the list is incomplete for our purposes!)

If just try to find songs by albums, we will have just 3 songs by Asha Bhosle, which is obviously nowhere near
the real number (11,000 Songs at least).

Now, coming back to the edge case :: It is important to search for uncategorized songs and append them to the final
list. Also, songs can be released as EPs/demos/singles etc. Hence those songs too, should not be discarded.

Again, if there are duplicates, they will be discarded.
For example after considering the edge case, above list of songs by Bob Dylan will look something like this -->

album title,                                                                   song title,                song id
N/A,                                                                           "10,000 Men",              200681
Under the Red Sky,                                                             "10,000 Men",              200681
Under the Red Sky,                                                             2 X 2,                     200682
N/A,                                                                           2 X 2,                     200682
The Bootleg Series Vol. 8: Tell Tale Signs: Rare and Unreleased 1989–2006,     32-20 Blues,               1686914
N/A,                                                                           32-20 Blues,               1686914
N/A,                                                                           4th Time Around,           105774
Blonde on Blonde,                                                              4th Time Around,           105774
Dylan (1973),                                                                  A Fool Such as I,          199634
N/A,                                                                           A Fool Such as I,          199634
N/A,                                                                           900 Miles from My Home,    1994655
"The Bootleg Series, Vol. 9: The Witmark Demos: 1962-1964",                    A Hard Rain’s A-Gonna Fall,105186
Bob Dylan’s Greatest Hits Vol. II ,                                            A Hard Rain’s A-Gonna Fall,105186
The Bootleg Series Vol. 7: No Direction Home: The Soundtrack,                  A Hard Rain’s A-Gonna Fall,105186
"The Bootleg Series Vol. 5: Bob Dylan Live 1975, The Rolling Thunder Revue",   A Hard Rain’s A-Gonna Fall,105186
The Freewheelin’ Bob Dylan,                                                    A Hard Rain’s A-Gonna Fall,105186
"The Bootleg Series Vol. 6: Bob Dylan Live 1964, Concert at Philharmonic Hall",A Hard Rain’s A-Gonna Fall,105186
----------------------------------------------------snip---------------------------------------------------------

along  with their 'years' (not shown here)
For songs that have no album info. on Genius.com will be set as "N/A" (Not available)

"""
    album_tracks_set = set()
    # initializing album_set as set() to hold list of albums along with their
    # meta information
    with open(all_albums_csv, encoding="utf-8") as data:
        for song_set in csv.DictReader(data):
            album_id = song_set["album id"]
            pages_to_traverse = genius.album_tracks(
                album_id=album_id, per_page=50, page=1
            )["next_page"]
            # searching and initializing total number of pages in which artist's tracks
            # are stored on genius.com
            if pages_to_traverse is None:
                # if None, zero. i.e, all the albums are available on first
                # page itself
                pages_to_traverse = 0
            for curr_page in range(1, pages_to_traverse + 2):
                # iterate over total number of pages to traverse i.e from
                # page 1 to total_pages
                tracks_in_curr_album = genius.album_tracks(
                    album_id=album_id, per_page=50, page=curr_page
                )
                for (
                    master_value
                ) in (
                    tracks_in_curr_album.values()
                ):  # search for tracks on the current page
                    # dive deep into the data_structure and extract useful
                    # info.
                    if master_value is not None and isinstance(
                            master_value, list):
                        for entry in master_value:
                            if entry["song"] is not None:
                                res = [
                                    (("album title", song_set["album title"]), ("song title", unidecode(
                                        entry["song"]["title"].replace(
                                            '’', "'"))), ("song id", entry["song"]["id"]), ("year", song_set["year"]))]
                                # keep on updating the set.
                                album_tracks_set.update(res)
    print(
        f"Tracks by each album generated. (Total number of songs in all albums : {Fore.YELLOW}"
        f"{len(album_tracks_set)}{Style.RESET_ALL})\n"
        f"Next, moving on to tracks released independently as singles,EPs,demos,unreleased etc.")
    print(f"{Fore.GREEN}A few more moments please!{Style.RESET_ALL}")
    pages = 1
    # Edge case, genius stores their songs in two ways:
    # 1) By albums ( that we just scrapped )
    # 2) In a master list that along with album songs also contain un-categorized songs i.e Demos,singles,
    # compilations,Live etc.
    # those songs are what we are going after here.
    while True:
        # finding total number of pages in which all songs are stored. For example Bob Dylan's all songs are
        # stored in total of 39 pages(with each page containing no more than 50
        # entries)!
        check_tot_pages = genius.artist_songs(
            artist_id=artist_id, per_page=50, page=pages
        )
        if check_tot_pages["next_page"] is not None:
            pages += 1
        else:
            break

    total_pages = pages
    # since there will be lot of repetition, better to initialize it as a
    # set()
    album_tracks_edge_set = set()
    for curr_page in range(1, total_pages + 1):
        artist_songs = genius.artist_songs(
            artist_id=artist_id, per_page=50, page=curr_page
        )
        for master_value in artist_songs.values():
            if isinstance(master_value, list):
                for entry in master_value:
                    if entry["primary_artist"]["name"] == artist_name:
                        res = [
                            (("album title",
                              "N/A"),
                             ("song title",
                                unidecode(
                                    entry["title"].replace(
                                        '’',
                                        "'"))),
                                ("song id",
                                 entry["id"]),
                                ("year",
                                 "N/A"))]
                        album_tracks_edge_set.update(res)
    print(
        f"List of uncategorized songs generated. (Total number of uncategorized songs : {Fore.YELLOW}"
        f"{len(album_tracks_edge_set)}{Style.RESET_ALL})")
    album_tracks_edge_set.update(album_tracks_set)
    album_tracks_list = sorted(
        [dict(song_set) for song_set in album_tracks_edge_set],
        key=lambda key: key["song title"],
    )

    file_name = first_last[-1] + "_tracks.csv"
    print(
        f"List of all tracks generated. (Final number of tracks : {Fore.YELLOW}{len(album_tracks_list)}"
        f"{Style.RESET_ALL})\n"
        f"Now exporting to CSV as {Fore.BLUE}{file_name}{Style.RESET_ALL}")
    tracks_by_album_csv = create_csv(album_tracks_list, file_name)
    # exporting as a csv file
    return tracks_by_album_csv, file_name


def lyrics_by_song(tracks_csv):
    """
:param tracks_csv: file_name of the CSV file containing all the tracks by the specified artist
:type tracks_csv: type --> str
:return: 3 separate CSV files with first containing lyrics for all original songs written by specified artist
(that are available on genius.com) & A csv file that contains songs NOT by specified artist by performed
nonetheless. Final CSV containing lyrics of all songs released by album release year
along with their original writer and the album it appears on for specified artist and File_name the lyrics_file
was saved as.
:rtype: 3 csv files (None type) and type(str) for file_name

Example: Continuing from the above example.. We now have a CSV file that contains all the songs by the particular
artist, for which we wish to scrape lyrics.

First CSV file: [artist's_last_name]_lyrics.csv
For example, calling lyrics_by_song(tracks_csv=Dylan_lyrics.csv) will give us ---> (as a csv file)

song title                                              lyrics
------------------------------------------------------snip-------------------------------------------------------
.                                                                        .
.                                                                        .
.                                                                        .
A Hard Rain’s  A-Gonna Fall [Gaslight 1962],            {
                                                        Oh, where have you been, my blue-eyed son?
                                                                                         .
                                                                                         .
                                                        I’ve stepped in the middle of seven sad forests
                                                        I’ve been out in front of a dozen dead oceans
                                                        I’ve been ten thousand miles in the mouth of a graveyard
                                                        }
.                                                                        .
.                                                                        .
.                                                                        .
------------------------------------------------------snip-------------------------------------------------------

Songs that are repeated will be added to the adjacent cell. (set)
This is because, even if the songs do have
same title, it is possible that the lyrics can be different. As we saw, since artist change lyrics for songs in
the live performances, it's necessary two songs with same songs similar. Next, again since genius.com is an
ever-changing website, i.e. anytime a song's lyrics is changed, it will result in a new lyrics for that song and
hence a different corpus in the end!
And suppose if the two songs appended are completely same, they will be discarded since, it's in a set.

Thus, the first CSV file [artist's_last_name]_lyrics.csv will contain ALL the lyrics of songs that are
written by artist and artist only!
But, what about about the songs that are sung/recorded/performed by Artist but not necessarily written by the same?

Second CSV file : [artist's_last_name]_lyrics_by_years.csv

This CSV file contains lyrics by album tracks for each album by year. For example, considering Bob Dylan's discography:

year,                   all_lyrics
----------------------------------------------snip---------------------------------------------------------------
.                         .
.                         .
.                         .

1966,                   {'Well, your railroad gate, you know I just cant jump it Sometimes it gets so hard, you see I
                        just sitting here beating on my trumpet With all these promises you left for me
                        But where are you tonight, sweet Marie?  Well, I waited for you when I was half sick
.                      Yes, I waited for you when you hated me Well, I waited for you inside of the frozen traffic
.                      Yeah, when you knew I had some other place to be Now, where are you tonight, sweet Marie?
.                      Well, anybody can be just like me, obviously But then, now again, not too many can be like you,
.                      fortunately  Well, six white horses that you . . . [". . . and lyrics of all other
.                      songs released in the year 1966"]
.                      }

2020,                    {  .
                                                    .
                                                    .
                                             }
----------------------------------------------snip---------------------------------------------------------------

Third CSV file: songs_not_by_[artist's_last_name].csv

This CSV file containing exactly the subset of songs discussed about. Songs that are NOT written by the artist.
Along with the title of the song, the csv file will also contain the original songwriter and the album it appears
on for artist in question.

Example:

song title                  album title & original song writer (if available)
Mr. Bojangles,              "['N/A', {'Jerry Jeff Walker'}]","['Dylan (1973)', {'Jerry Jeff Walker'}]"

------------------------------------------------------snip-------------------------------------------------------
            Thus here song "Mr. Bojangles" :
            1) Is written by Jerry Jeff Walker and not Bob dylan.
            2) But, recorded nonetheless on album Dylan (1973)
            3) It is repeated twice since the song "Mr Bojangles" appears twice on the final song csv file
            4) There is also a version of Mr.Bojangles on genius.com that doesn't have required info. hence set to "N/A"

For songs that have no album info. or song-writer info. on Genius.com will be set as "N/A" (Not available)
"""

    lyrics_set = defaultdict(set)
    not_by_artist = defaultdict(list)
    lyrics_by_years = defaultdict(set)
    # a little nifty trick to take a break after every 'n' songs in order to prevent
    # it from timeout or api calls exceptions etc.
    counter = 0
    master_artists = None
    if band_members is not None:
        master_artists = {artist for artist in band_members}
        master_artists.update(artist_name.split("''"))
    else:
        pass

    with open(tracks_csv, encoding="UTF-8") as data:
        for line in csv.DictReader(data):
            song_title = line["song title"].strip()
            album_title = line["album title"].strip()
            song_year = line["year"].strip()
            try:

                if counter != 0 and counter % 10 == 0:
                    print(
                        "_____________________________________________________________________________________"
                    )
                    time.sleep(0.25)
                # searching for song details by song_tile and artist_name
                lyrics = genius.search_song(song_title, artist_name)
                # not all songs necessarily are available on Genius.com some
                # return None.
                if lyrics is not None:
                    counter += 1  # basically +1 point since song exists!
                    # noinspection PyArgumentEqualDefault
                    title_ratio = SequenceMatcher(
                        None, lyrics.title, song_title).ratio()
                    # noinspection PyArgumentEqualDefault
                    artist_ratio = SequenceMatcher(
                        None, lyrics.artist, artist_name).ratio()
                    if round(title_ratio, 2) >= 0.93 and artist_ratio == 1.0:
                        # Because of the way data is stored on genius and lyricsgenius is written, it tries
                        # to return the next best song if the given song doesn't exist.
                        # Even if we specify song and artist name
                        # it still returns false data, hence just a double
                        # check measure!
                        writer = (
                            lyrics.writer_artists
                        )  # to check for the original song_writer
                        # storing in a set, to skip out duplicates
                        total_writers = {
                            song_writer["name"] for song_writer in writer}

                        # if No singer data is available -- set to Not
                        # available.
                        if len(total_writers) == 0:
                            total_writers = ["N/A"]
                            not_by_artist[song_title].append(
                                [song_year, album_title, total_writers]
                            )

                        if not writer:  # if writer set() is empty i.e False:
                            print(
                                f'{Fore.GREEN}Song "{song_title}" skipped since '
                                f"not enough information on genius.com "
                                f"for "
                                f'songwriter, hence setting to "N/A"{Style.RESET_ALL}')
                            not_by_artist[song_title].append(
                                [song_year, album_title, total_writers]
                            )

                        # if artist_name is in the above set(), that's
                        # precisely what we are looking for! Hence adding to
                        # the lyrics_set.
                        if not isinstance(total_writers, list):
                            if band_members is not None:
                                if total_writers.intersection(master_artists):
                                    pure_lyrics = lyrics.lyrics
                                    pure_lyrics = pure_lyrics.replace(
                                        "\n", " ")
                                    pure_lyrics = unidecode(
                                        pure_lyrics).strip()
                                    pure_lyrics = pure_lyrics.replace("\'", "")
                                    lyrics_set[song_title].add(pure_lyrics)
                                    lyrics_by_years[song_year].add(pure_lyrics)
                                else:
                                    print(
                                        f'{Fore.GREEN}Song "{lyrics.title}" skipped since {artist_name} '
                                        f'is not the original '
                                        f"writer."
                                        f"\nOriginal author(s) : {list(total_writers)}\n{Style.RESET_ALL}")
                                    # skipping songs for which artist is not the
                                    # original writer and adding to the other
                                    # dict.

                                    not_by_artist[song_title].append(
                                        [album_title, total_writers]
                                    )
                            else:
                                if artist_name in total_writers:
                                    pure_lyrics = lyrics.lyrics
                                    pure_lyrics = pure_lyrics.replace(
                                        "\n", " ")
                                    pure_lyrics = unidecode(
                                        pure_lyrics).strip()
                                    pure_lyrics = pure_lyrics.replace("\'", "")
                                    lyrics_set[song_title].add(pure_lyrics)
                                    lyrics_by_years[song_year].add(pure_lyrics)
                                else:
                                    print(
                                        f'{Fore.GREEN}Song "{lyrics.title}" skipped since {artist_name} '
                                        f'is not the original '
                                        f"writer."
                                        f"\nOriginal author(s) : {list(total_writers)}\n{Style.RESET_ALL}")
                                    # skipping songs for which artist is not the
                                    # original writer and adding to the other
                                    # dict.

                                    not_by_artist[song_title].append(
                                        [album_title, total_writers]
                                    )
                        else:
                            print(
                                f"{Fore.GREEN}Song writer info. not available on genius.com, "
                                f"hence skipped{Style.RESET_ALL}\n")
                    else:
                        print(
                            f"{Fore.GREEN}Song information not available on genius.com, "
                            f"hence skipped{Style.RESET_ALL}\n")

                else:
                    print(
                        f'{Fore.GREEN}Lyrics for the song "{song_title}" is N/A on genius.com, hence skipped.\n'
                        f"{Style.RESET_ALL}")  # skipping since no data is available.
            except Timeout:
                continue

    # storing data as Pandas dataframe n rows (total number of songs) x 2
    # columns (song title and lyrics)
    lyrics_set_final = pd.DataFrame(
        {keys: pd.Series(str(values)) for keys, values in lyrics_set.items()}
    ).transpose()
    lyrics_set_final.columns = ['lyrics']

    # storing data as Pandas dataframe n rows (total number of songs not
    # written by artist) x 2 columns (song title and the album it originally
    # appears on)
    not_by_artist_final = pd.DataFrame(
        {keys: pd.Series(values) for keys, values in not_by_artist.items()}
    ).transpose()

    by_years_final = pd.DataFrame(
        {keys: pd.Series(str(values)) for keys, values in lyrics_by_years.items()}
    ).transpose()
    by_years_final.columns = ['lyrics']

    # exporting to 2 separate CSV files
    lyrics_csv = lyrics_set_final.to_csv(
        first_last[-1] + "_lyrics.csv", encoding="utf-8"
    )
    not_by_artist_csv = not_by_artist_final.to_csv(
        "songs_not_by_" + first_last[-1] + ".csv", encoding="utf-8"
    )

    by_years_csv = by_years_final.to_csv(
        first_last[-1] + "_lyrics_by_years.csv", encoding="utf-8"
    )

    print(
        f"\nCSV file containing lyrics exported as {Fore.BLUE}{first_last[-1] + '_lyrics.csv'}{Style.RESET_ALL}"
    )
    print(
        f"CSV file containing songs not written (but performed) by {artist_name} exported "
        f"as {Fore.BLUE}{'songs_not_by_' + first_last[-1] + '.csv'}{Style.RESET_ALL}")
    print(
        f"CSV file containing songs by year for artist : {artist_name} exported "
        f"as {Fore.BLUE}{first_last[-1] + '_lyrics_by_years.csv'} {Style.RESET_ALL}")

    return lyrics_csv, not_by_artist_csv, by_years_csv, first_last[-1] + "_lyrics.csv"


def corpus_generator(lyrics_csv):
    """
:param lyrics_csv: file_name of the CSV file that contains all the lyrics
:type lyrics_csv: str
:return: CSV file containing all the unique songs by the specified artis in a single cell.
:rtype: CSV file, (None type)

"""
    res = set()
    # initializing res as a set, since we need only unique songs in our final
    # corpus
    with open(lyrics_csv, encoding="utf-8") as data:
        for line in csv.DictReader(data):
            temp = line['lyrics']
            res.add(''.join(word for word in temp if word not in '{}'))
    single_list = ["".join(res)]
    # joining all the separate songs into one sing string!
    file_name = first_last[-1] + "_corpus.csv"
    corpus_dataframe = pd.DataFrame(single_list)
    corpus_dataframe.columns = [first_last[-1] + " corpus"]
    corpus_dataframe.to_csv(file_name, encoding='utf-8')
    print(
        f"CSV file containing corpus for artist: {artist_name} generated and exported as "
        f"{Fore.BLUE}{file_name}{Style.RESET_ALL}")


if __name__ == '__main__':
    print("\nWelcome to CorpusGenius!\n"
          "Jatan J. Pandya (jpandya) © 2020 / https://github.com/jatanjay/")
    token = input("\nPlease enter your unique Client Side Token Id: ")
    artist_name = input(
        "\nPlease enter the artist's name you'd like to generate CSV and other metadata for: "
    )
    first_last = artist_name.split()
    init(convert=True)
    band_test = input(
        "\nIs the specified artist a Band?\n"
        "If yes, enter 'Y',"
        " else just press enter: ")
    if band_test:
        band_members = input(
            "\nGreat! Please enter their names : \n"
            "\nFor example if your specified artist was The Beatles, then you'd enter individual band member names as: "
            "\n"
            ">> John Lennon, Paul McCartney, George Harrison, Ringo Starr, Lennon-McCartney\n"
            "\nNote: Lennon-McCartney is added since sometimes genius.com attributes songwriter credits as "
            "Lennon-McCartney rather than John Lennon and Paul McCartney."
            "\nThus for your specified artist, let the project run for a while and at any moment you feel songs are "
            "erroneously skipped, note down the name it is stored as and re-run CorpusGenius, this time adding "
            "it along with the earlier names. Since it's impossible to know under what names song-writers are "
            "credited, "
            ""
            "a little trial & error is required :)\n"
            "For more details, please visit : https://github.com/jatanjay/CorpusGenius/blob/main/README.md"
            "\n(Hey psst, make sure the spelling is accurate, even a small "
            "change might affect the final corpus!)\n"
            "\nBand Member names : ")
        band_members = set(band_members.split(","))
        band_members = {member.strip() for member in band_members}

    else:
        print("Great! Onwards!")
        band_members = None

    print(
        "\n----------------------------\nConnecting to Genius.com...\n----------------------------\n"
    )

    start = time.time()

    genius = lyricsgenius.Genius(token.strip())
    genius.remove_section_headers = True
    # Increasing genius.timeout in-order to prevent timeout exceptions and
    # battle weak api_calls
    genius.timeout = 200
    # Increasing time out between requests since sometime excessive requests
    # create
    genius.sleep_time = 0.75
    # exceptions
    print(
        f"\nIn order to double check if the details for the specified artist : {artist_name} is available on\n"
        f"genius.com, let us check for one random song.\n"
        f"-----------------------------------------------------------------------------------------------\n")
    artist_search = genius.search_artist(
        artist_name=artist_name, max_songs=1, per_page=50, get_full_info=False
    )
    artist_id = artist_search._id

    print("\nGreat! Artist exists on genius.com!\n")
    print("\n-----------------------------------")
    print(f"Artist's name : {Fore.YELLOW}{artist_name}{Style.RESET_ALL}")
    print(f"Artist's Genius Id : {Fore.YELLOW}{artist_id}{Style.RESET_ALL}")

    print("-----------------------------------\n")

    print(
        f"\nGenerating CSV file containing all albums released by artist: {artist_name}"
    )
    artist_albums_csv = artist_albums(artist_id)

    print(
        f"Done!\n\nGenerating CSV file containing all tracks by albums/demos/EPs etc. released by artist: "
        f"{artist_name}")
    album_tracks_csv = album_tracks(all_albums_csv=artist_albums_csv[1])

    print(
        f"Done!\n\nGenerating 2 CSV files\n"
        f"1) A CSV file containing lyrics for all original songs for which {artist_name} "
        f"is credited "
        f"as "
        f"the original songwriter\n")
    print(
        f"2) A CSV file containing songs that are not written "
        f"but released/performed nonetheless by artist: "
        f"{artist_name}\n "
        f"   along with their original writers and the "
        f"specified artist's album on which it appears\n"
    )
    print("----------------------------------------------------------------------------------\n")
    all_lyrics = lyrics_by_song(tracks_csv=album_tracks_csv[1])
    corpus_generator(lyrics_csv=all_lyrics[3])
    end = time.time()
    print(
        "\n__________________________________________"
        "_______________________________________________________\n"
    )
    print(
        "\nAll files will be stored in your current working directory!\n"
        "Thank you for using CorpusGenius\n"
    )
    print(f"\nProcess completed in {(end - start) / 60} minutes")
