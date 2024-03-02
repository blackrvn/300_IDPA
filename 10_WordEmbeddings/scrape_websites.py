"""
Skript um mehre Websites auf einmal herunterzuladen.

Inputs:
1. Liste von URLs von Webseiten die heruntergeladen werden sollen.
   Jede URL muss auf eine eigene Zeile.
2. Name der Output-Datei.

Output:
eine grosse Datei die den Inhalt aller Seiten enthält.
Wenn diese Datei bereits existiert, wird der neue Inhalt hinten angehängt.

Manche Seiten lassen sich nicht herunterladen.
Manchmal sind dies Seiten ohne Inhalt, oder uninteressantem/unbrauchbarem Inhalt,
oder trafilatura konnte die Seite nicht richtig lesen.
"""

import argparse
from trafilatura import extract, fetch_url
from tqdm import tqdm


def scrape_websites(file_url_list, file_output):
    urls = []
    with open(file_url_list, "r", encoding="utf-8") as input_file:
        # Lese alle Zeilen in eine Liste
        urls = input_file.readlines()

    # die Datei wird überschrieben, falls sie schon Inhalt besitzt
    with open(file_output, "w", encoding="utf-8") as file_output_opened:
        # um ein gültiges xml zu erstellen, brauchen wir ein root element.
        file_output_opened.write("<?xml version='1.0' encoding='UTF-8'?> \n")
        file_output_opened.write("<corpus> \n")
        success_counter = 0

        for url in tqdm(urls, total=len(urls)):
            url = url.strip()  # Hier werden whitespace characters vor und nach den URLs entfernt.
            if not url:  # Leerzeilen überspringen
                continue

            website_content = fetch_url(url)  # hier passiert der eigentliche Download

            if website_content is None:  # falls nichts heruntergeladen werden konnte
                print(f"Zur URL {url} wurde nichts heruntergeladen.")
                continue

            # das Heruntergeladene wird von trafilatura brauchbar gemacht
            # Output-Format ist XML, Kommentare inkludiert, und nur Seiten auf Deutsch werden gescrapt
            website_content_cleaned = extract(website_content, output_format='xml', include_comments=True,
                                              target_language='de')

            if website_content_cleaned is None:  # falls die Extraktion nicht ausgeführt werden kann
                print(f"Zur URL {url} wurde nichts heruntergeladen.")
                continue

            # hier wird das heruntergeladene ins outputfile geschrieben
            file_output_opened.write(website_content_cleaned)
            success_counter += 1

            if success_counter > 10:
                break
        # der root node muss geschlossen werden
        file_output_opened.write("\n</corpus>")
        print(f"Der Inhalt von {success_counter} URL(s) ist nun in der Datei {file_output}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Websites")
    parser.add_argument("url_list_file", type=str, help="File mit einer Liste von URLs, die gescrapt werden")
    parser.add_argument("output_file", type=str, help="Name der Output-Datei, z.B. out.xml")

    args = parser.parse_args()
    scrape_websites(args.url_list_file, args.output_file)
