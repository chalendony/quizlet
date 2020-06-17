"""
Create urls from a list of Vocabulary terms. Run wget to pull pages, Then run the linguee parser on each downloaded page
"""
import glob
import constants as const

if __name__ == '__main__':
    lst = []
    # read input
    with open(const.lingue_termfile) as f:
        lines = f.readlines()

    for l in lines:
        # clean: remove whitespace, # skip empty line
        term = l.strip()
        if term:
            url = f"{const.lingue_base_url}{term}.html"
            lst.append(url)
    # write to file
    print(lst)
    with open(const.lingue_urlfile, "w") as outfile:
        outfile.write("\n".join(lst))