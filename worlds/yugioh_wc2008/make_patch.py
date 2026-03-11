import bsdiff4

with open("wc2008_clean.nds", "rb") as f:
    clean = f.read()

with open("wc2008_modified.nds", "rb") as f:
    modified = f.read()

patch = bsdiff4.diff(clean, modified)

with open("base_patch.bsdiff4", "wb") as f:
    f.write(patch)

print("base_patch.bsdiff4 created")
