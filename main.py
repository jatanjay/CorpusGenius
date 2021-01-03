"""
File : main.py
author : Jatan Pandya
magic happens here
"""

from corpusgenius import *


def main():
	print("\nWelcome!\n")
	# token = "5h-2a17u22aziiDRyA8HoUmxgfoyW8aHP2Bc3510VBpkQqTX7tfNrrPxDEY6WRKr"
	token = input("\nPlease enter your client side token id: ")
	artist_name = input(
		"\nPlease enter the artist's name you'd like to download data for: "
		)
	first_last = artist_name.split()
	
	band_test = input(
		"Is your specified artist a band/consists of multiple songwriters/arttist? If yes,enter any key"
		". If no,press enter ")
	if band_test:
		band_members = input(
			"Great! Please enter their names. (Hey, make sure the spelling is accurate, a small"
			"change might affect the final corpus! ")
		band_members = set(band_members.split(","))
		band_members = {member.strip() for member in band_members}
		print("These are the band_members", band_members)
	
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
		f"\nIn order to double check if the details for specified artist : {artist_name} is available on\n"
		f"genius.com, let us check for one random song.\n"
		f"-----------------------------------------------------------------------------------------------\n")
	artist_search = genius.search_artist(
		artist_name=artist_name, max_songs=1, per_page=50, get_full_info=False
		)
	artist_id = artist_search._id
	
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
		"Thank you for using this tool\n"
		)
	print(f"\nProcess completed in {(end - start) / 60} minutes")


if __name__ == '__main__':
	main()
