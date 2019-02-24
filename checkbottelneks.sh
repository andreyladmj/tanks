#  https://learning.oreilly.com/library/view/python-high-performance/9781787282896/10f983e0-54e8-4aef-9b85-53b82c30cd99.xhtml
pyprof2calltree -i prof.out -o prof.calltree
kcachegrind prof.calltree # or qcachegrind prof.calltree