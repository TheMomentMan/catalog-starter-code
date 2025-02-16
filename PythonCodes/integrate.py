import glob, os

# specify local directory
os.chdir(".")

# concatenate all files into one
with open('data.html', 'w') as outfile:
    for file in glob.glob("data/*.html"):
        with open(file) as infile:
            outfile.write(infile.read())