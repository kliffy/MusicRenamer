import os, re

for path, subdirs, files in os.walk("/Users/kliffydeveloper/Downloads/Musac"):
    for name in files:
        shit = re.sub(r"www(.*)net", '', name)
        shit = re.sub("&amp;", "&", shit)

        shit = re.sub(r"(\S)\-(\S)", r"\1 - \2", shit) #"abc-der"
        shit = re.sub(r"\s\-(\S)", r' - \1', shit)
        shit = re.sub(r"(\S)\-\s", r'\1 - ', shit)

        shit = re.sub(r"\s*(\.mp3)", r"\1", shit) #"songname     .mp3"

        #NEXT TODO: Scrub inner data of the mp3!

        os.rename(os.path.join(path,name), os.path.join(path,shit))

for path, subdirs, files in os.walk("/Users/kliffydeveloper/Downloads/Musac"):
    for name in files:
        print name