#options:
# -l  -  folder location of all audio files
# -replace-with-id3  -  replace file name with what the id3 tag title and artist is
# -t  -  test, will output what the changes might be, will not make any changes

# -no-name-changes - will not try to change song title or artist. can be used if only trying to fetch lyrics and/or images
# -lyrics  -  fetch lyrics for songs
# -image  -  fetch album image for songs

# -f  -  different formats

#music-renamer -replace-with-id3 -t -l ~/Documents/music\ renamed/


import os, re, sys, getopt, pdb, mutagen
from mutagen.id3 import ID3, TIT1, TIT2, TPE1, TPE2, COMM, USLT, TCOM, TBPM, USLT, WPUB

#python music_rename_script.py -l /Some/Folder/Name
def main(argv):
  folder_location = ''
  test_mode = False
  replace_with_id3 = False
  no_name_changes = False
  get_lyrics = False
  get_images = False

  opts, args = getopt.getopt(argv,"l:replace-with-id3:t")
  for opt, arg in opts:
    if opt in ("-l"):
      folder_location = arg
    if opt in("-replace-with-id3"):
      print '-- Will Replace with ID3 Artists and Title'
      replace_with_id3 = True
    if opt in("-t"):
      print "-- Test Mode"
      test_mode = True
    if opt in("-no-name-changes"):
      print "-- No Name Change Mode"
      no_name_changes = True
    if opt in("-lyrics"):
      print "-- Will Fetch Lyrics"
      get_lyrics = True
    if opt in("-image"):
      print "-- Will Fetch Album Art"
      get_images = True

  print 'Starting on folder: ', folder_location

  #pdb.set_trace()

  #separation of this block into its own method/file?
  #music_renamer_engine.py  music_renamer.py  ???
  for path, subdirs, files in os.walk(folder_location):
    for name in files:
      if name.endswith(".mp3"):

        try:
          tags = ID3(folder_location + name)
        except mutagen.id3.error:
          tags = ID3()
          tags.save(folder_location + name)

        print "original: " + name

        if "TPE1" in tags and "TIT2" in tags:
          id3_file_name = tags["TPE1"].text[0] + " - " + tags["TIT2"].text[0]
          print "original ID3: " + id3_file_name
        else:
          id3_file_name = None
          print "original ID3: No ID3 tags"


        #Name Changing
        if not no_name_changes:
          #if no id3 tags. then change name by default
          if replace_with_id3 and id3_file_name:
            #option - id3 tags to replace file name
            new_name = id3_file_name
            new_name = re.sub(r"\[(.*)\]", r"(\1)", new_name)
            new_name = new_name + ".mp3"
          else:
            new_name = re.sub(r"www(.*)net", '', name)
            new_name = re.sub("&amp;", "&", new_name)
            new_name = re.sub("_", " ", new_name)
            new_name = re.sub(r"\[(.*)\]", r"(\1)", new_name) #[whatever remix] => (whatever remix)

            new_name = re.sub(r"(\S)\-(\S)", r"\1 - \2", new_name) #"abc-def => abc - def"
            new_name = re.sub(r"\s\-(\S)", r' - \1', new_name)
            new_name = re.sub(r"(\S)\-\s", r'\1 - ', new_name)

            new_name = re.sub(r"\s*(\.mp3)", r"\1", new_name) #"songname     .mp3"

          print "new: " + new_name
          print ""

          if not test_mode:
            #Scrub tags that where junk text is commonly added to
            tags["TCOM"] = TCOM(encoding=3, text=u'') #Composer
            tags["TIT1"] = TIT1(encoding=3, text=u'') #Grouping
            tags["TBPM"] = TBPM(encoding=3, text=u'') #BPM
            tags["COMM::eng"] = COMM(encoding=3, text=u'') #Comments
            tags["USLT::eng"] = USLT(encoding=3, text=u'') #Lyrics
            tags["TPE2"] = TPE2(encoding=3, text=u'') #Album Artist
            tags["WPUB"] = WPUB(encoding=3, text=u'') #Publisher Webpage

            #some titles and song names may have [] rather than ()
            if 'TPE1' in tags:
              tags["TPE1"] = TPE1(encoding=3,text=re.sub(r"\[(.*)\]", r"(\1)", tags["TPE1"].text[0]))
            else:
              #add the tag if it doesnt exist
              artist = re.sub(r"(.*)\-.*", r'\1', new_name).strip()
              tags["TPE1"] = TPE1(encoding=3,text=artist)

            if 'TIT2' in tags:
              tags["TIT2"] = TIT2(encoding=3,text=re.sub(r"\[(.*)\]", r"(\1)", tags["TIT2"].text[0]))
            else:
              song_name = re.sub(r".*\-(.*)", r'\1', new_name).strip()
              tags["TIT2"] = TIT2(encoding=3,text=song_name)

            tags.save(folder_location + name)
            os.rename(os.path.join(path,name), os.path.join(path,new_name))

        #Lyrics Fetching
        # if get_lyrics:
        #   #search multiple websites for lyrics
        #   #either scrape from website. OR api endpoint like with musixmatcher or genius.com

        # #Album Art Fetching
        # if get_images:
        #   #something

if __name__ == "__main__":
   main(sys.argv[1:])
