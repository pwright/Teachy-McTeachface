# clean up
rm -rf build/unit*
# convert logseq
python template/logseq.py -c gdoc.yaml gdoc/ build/ template/

# run tutors
cd build
tutors-json
mv json public-site
tutors-html
cd ..
