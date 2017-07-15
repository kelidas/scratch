# Pdflatex to Word
- convert all figs to eps
- convertPDFtoEPS.py converts all pdf to eps
- for other formats use e.g. `$ convert figure.png figure.eps`

```bash
$ python convertPDFtoEPS.py
$ htlatex main.tex main.cfg
$ tidy -o main.html main.html
$ python3 main.py
```
- cfg - all math as images
- tidy is optional (remove height and width from images)
- main.py add width and height in Math (line math $...$, display math)

- open in libreOffice, Tools > Links > Break links   and save as docx
