import os
import sys
import unittest
sys.path.insert(0, os.path.dirname('/'.join(__file__.split('/')[:-1])))
import websearch


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

if __name__ == '__main__':
    runner = unittest.TestCase()
    runner.run()