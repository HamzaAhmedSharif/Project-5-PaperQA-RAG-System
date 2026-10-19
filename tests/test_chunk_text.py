"""Regression tests for rag_utils.chunk_text (zero-overlap defect fix).

Covers the overlap-window behavior: zero overlap must not repeat sentences
across chunks, positive overlap is preserved, plus input edge cases.

Run from the repository root:
    python tests/test_chunk_text.py -v

Requires the project's `rag` environment (rag_utils imports faiss and
sentence_transformers at module top level).
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import rag_utils


class TestChunkTextOverlap(unittest.TestCase):
    def test_zero_overlap_no_repeat(self):
        chunks, pages = rag_utils.chunk_text(
            [(1, "Alpha one. Beta two."), (2, "Gamma three. Delta four.")],
            chunk_size=15, overlap_sentences=0)
        self.assertEqual(chunks, ["Alpha one. Beta two.", "Gamma three. Delta four."])
        self.assertEqual(pages, [1, 2])
        for s in ["Alpha one.", "Beta two.", "Gamma three.", "Delta four."]:
            self.assertEqual(sum(c.count(s) for c in chunks), 1,
                             "sentence repeated across chunks: %r" % s)

    def test_positive_overlap_two(self):
        chunks, pages = rag_utils.chunk_text(
            [(1, "Alpha one. Beta two. Gamma three. Delta four.")],
            chunk_size=20, overlap_sentences=2)
        self.assertEqual(chunks, ["Alpha one. Beta two. Gamma three.",
                                 "Beta two. Gamma three. Delta four.",
                                 "Gamma three. Delta four."])
        self.assertEqual(pages, [1, 1, 1])

    def test_overlap_larger_than_window(self):
        chunks, pages = rag_utils.chunk_text(
            [(1, "Alpha one. Beta two. Gamma three.")],
            chunk_size=15, overlap_sentences=3)
        self.assertEqual(chunks, ["Alpha one. Beta two.",
                                 "Alpha one. Beta two. Gamma three.",
                                 "Alpha one. Beta two. Gamma three."])
        self.assertEqual(pages, [1, 1, 1])

    def test_empty_inputs(self):
        self.assertEqual(
            rag_utils.chunk_text([], chunk_size=500, overlap_sentences=0), ([], []))
        self.assertEqual(
            rag_utils.chunk_text([(1, "")], chunk_size=500, overlap_sentences=0), ([], []))
        self.assertEqual(
            rag_utils.chunk_text([(1, "   ")], chunk_size=500, overlap_sentences=0), ([], []))

    def test_final_partial_chunk(self):
        self.assertEqual(
            rag_utils.chunk_text([(1, "Alpha one. Beta two. Gamma three.")],
                                 chunk_size=100, overlap_sentences=0),
            (["Alpha one. Beta two. Gamma three."], [1]))

    def test_page_attribution_zero_overlap(self):
        self.assertEqual(
            rag_utils.chunk_text([(1, "Alpha one. Beta two."), (2, "Gamma three.")],
                                 chunk_size=15, overlap_sentences=0),
            (["Alpha one. Beta two.", "Gamma three."], [1, 2]))

    def test_punctuation_splitting(self):
        self.assertEqual(
            rag_utils.chunk_text([(1, "Wow! Really? Yes. No")],
                                 chunk_size=10, overlap_sentences=0),
            (["Wow! Really?", "Yes. No"], [1, 1]))


if __name__ == "__main__":
    unittest.main()
