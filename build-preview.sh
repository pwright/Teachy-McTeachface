# clean up
rm -rf build/unit*
# convert logseq
python template/logseq.py logseq/ build/ template/

# run tutors
cd build
tutors-json
mv json public-site
tutors-html
cd ..
