import sys
import unittest
from graph import Graph

#let's write output to a file, not terminal
class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()

    #AddVertex(...)
    def test_AddVertex_AddOne(self):
        self.graph.AddVertex((1, 'test'))
        self.assertEqual(1, len(self.graph.adj_list))
        self.assertEqual(1, len(self.graph.payloads))

    def test_AddVertex_AddTwoUnconnected(self):
        self.graph.AddVertex((1, 'test'))
        self.graph.AddVertex((2, 'test'))
        self.assertEqual(2, len(self.graph.adj_list))
        self.assertEqual(2, len(self.graph.payloads))

    def test_AddVertex_AddTwoConnected(self):
        node_00 = (1, 'test')
        self.graph.AddVertex(node_00)
        node_01 = (2, 'test')
        self.graph.AddVertex(node_01, 1) #hmmm is this a sign that passing a whole node makes more sense to the user?
        self.assertTrue(1 in self.graph.adj_list[2])
        self.assertTrue(2 in self.graph.adj_list[1])

    def test_AddVertex_ConnectToSelf(self):
        self.graph.AddVertex((1, 'test'), 1)
        self.assertFalse(1 in self.graph.adj_list[1])
    
    def test_AddVertex_ConnectToListDistinct(self):
        add_us = []
        for ii in range(10):
            add_us.append(ii)
            self.graph.AddVertex((ii, 'test'))
        self.graph.AddVertex((11, 'test'), add_us)

        for ii in range(10):
            self.assertTrue(ii in self.graph.adj_list[11])
        self.assertEqual(10, len(self.graph.adj_list[11]))

    #RemoveVertex(...)
    def test_RemoveVertex_RemoveOne(self):
        self.graph.AddVertex((1, 'test'))
        self.graph.RemoveVertex(1)
        self.assertEqual(0, len(self.graph.adj_list))
        self.assertEqual(0, len(self.graph.payloads))

    def test_RemoveVertex_RemoveDoesNotExist(self):
        self.graph.AddVertex((1, 'test'))
        self.graph.RemoveVertex(2)
        self.assertEqual(1, len(self.graph.adj_list))
        self.assertEqual(1, len(self.graph.payloads))

    def test_RemoveVertex_RemoveTwoUnconnected(self):
        self.graph.AddVertex((1, 'test'))
        self.graph.AddVertex((2, 'test'))
        self.graph.RemoveVertex(1)
        self.graph.RemoveVertex(2)
        self.assertEqual(0, len(self.graph.adj_list))
        self.assertEqual(0, len(self.graph.payloads))

    def test_RemoveVertex_RemoveTwoConnected(self):
        self.graph.AddVertex((1, 'test'))
        self.graph.AddVertex((2, 'test'), 1)
        self.graph.RemoveVertex(1)
        self.graph.RemoveVertex(2)
        self.assertEqual(0, len(self.graph.adj_list))
        self.assertEqual(0, len(self.graph.payloads))

    def test_RemoveVertex_RemoveTwoConnectedStackOrder(self):
        self.graph.AddVertex((1, 'test'))
        self.graph.AddVertex((2, 'test'), 1)
        self.graph.RemoveVertex(2)
        self.graph.RemoveVertex(1)
        self.assertEqual(0, len(self.graph.adj_list))
        self.assertEqual(0, len(self.graph.payloads))

#allows us to run just this set of tests but also run these tests from elsewhere
if __name__ == '__main__':
    unittest.main()