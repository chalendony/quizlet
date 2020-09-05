import tabula




if __name__ == "__main__":
    file = "/home/avare/NewNextCloud/German/books/Fokus B2/Cornelsen_Webcode_xiqepa/9783060209910_Wortliste_Englisch_Gesamt_PDF.pdf"

    tabula.convert_into(file, "test.csv", pages=4)


  #
  # pages=None,
  #   guess=True,
  #   area=None,
  #   relative_area=False,
  #   lattice=False,
  #   stream=False,
  #   password=None,
  #   silent=None,
  #   columns=None,
  #   format=None,
  #   batch=None,
  #   output_path=None,
  #   options="",