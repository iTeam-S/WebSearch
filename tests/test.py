import os
import sys
import unittest

import websearch

sys.path.insert(0, os.path.dirname('/'.join(__file__.split('/')[:-1])))


class TestCaseModule(unittest.TestCase):

    def test1_pages(self):
        pages = websearch.WebSearch('iTeam-$').pages[:5]
        # Verification de nombres de resultats
        self.assertTrue(len(pages))
        # verification lien
        for page in pages:
            self.assertTrue(page.startswith('http'))

    def test2_images(self):
        images = websearch.WebSearch('Madagascar').images[:5]
        # Verification de nombres de resultats
        self.assertTrue(len(images))
        # verification lien
        for image in images:
            self.assertTrue(image.startswith('http'))

    def test3_pdf(self):
        pdfs = websearch.WebSearch('Math 220').pdf[:2]
        # Verification de nombres de resultats
        self.assertTrue(len(pdfs))
        # verification lien
        for pdf in pdfs:
            self.assertTrue(pdf.startswith('http'))

    def test4_word(self):
        words = websearch.WebSearch('python').docx[:3]
        # Verification de nombres de resultats
        self.assertTrue(len(words))
        # Verification lien
        for word in words:
            self.assertTrue(word.startswith('http'))

    def test5_excel(self):
        excels = websearch.WebSearch('datalist').xlsx[:3]
        # Verification de nombre de résultats
        self.assertTrue(len(excels))
        # Verification lien
        for excel in excels:
            self.assertTrue(excel.startswith('http'))

    def test6_powerpoint(self):
        powerpoints = websearch.WebSearch('Communication').pptx[:3]
        # Verification de nombre de résultats
        self.assertTrue(len(powerpoints))
        # Verification lien
        for powerpoint in powerpoints:
            self.assertTrue(powerpoint.startswith('http'))

    def test7_odt(self):
        documents = websearch.WebSearch('Finance').odt[:3]
        # Verification de nombre de résultats
        self.assertTrue(len(documents))
        # Verification lien
        for doc in documents:
            self.assertTrue(doc.startswith('http'))

    def test8_ods(self):
        documents = websearch.WebSearch('Commerce').ods[:1]
        # Verification de nombre de résultats
        self.assertTrue(len(documents))
        # Verification lien
        for doc in documents:
            self.assertTrue(doc.startswith('http'))

    def test9_kml(self):
        maps = websearch.WebSearch('Madagascar').kml[:1]
        # Verification de nombre de résultats
        self.assertTrue(len(maps))
        # Verification lien
        for map in maps:
            self.assertTrue(map.startswith('http'))

    def test10_custom(self):
        web = websearch.WebSearch('Biologie')
        documents = web.custom('ps', 'application/postscript')[:1]
        # Verification de nombre de résultats
        self.assertTrue(len(documents))
        # Verification lien
        for doc in documents:
            self.assertTrue(doc.startswith('http'))

    def test11_odp(self):
        documents = websearch.WebSearch('Renaissance').odp[:1]
        # Verification de nombre de résultats
        self.assertTrue(len(documents))
        # Verification lien
        for doc in documents:
            self.assertTrue(doc.startswith('http'))


if __name__ == '__main__':
    runner = unittest.TestCase()
    runner.run()
