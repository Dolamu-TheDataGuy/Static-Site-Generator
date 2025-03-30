from htmlnode import HTMLNode
import unittest

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a text node")
        node2 = HTMLNode("p", "This is a text node")
        node3 = HTMLNode("p", "This is a text node", [HTMLNode("a", "www.google.com")])
        node4 = HTMLNode("p", "This is good", props={"class": "bold"})
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        
if __name__ == "__main__":
    unittest.main()