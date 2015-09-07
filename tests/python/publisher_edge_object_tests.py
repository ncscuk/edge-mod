
import unittest
import mock
from publisher_edge_object import PublisherEdgeObject


class PublisherEdgeObjectTests(unittest.TestCase):

    ok_ids = {
        'http://www.namespace-1.com': 'Alias_1:dummy-id-1234',
        'http://www.namespace-2.com': 'Alias_2:dummy-id-5678'
    }

    empty_alias_id = {
        'http://www.namespace-3.com': 'dummy-id-9999'
    }

    malformed_id = {
        'http://www.namespace-4.com': 'Alias_4:xyz:dummy-id-abc'
    }

    @staticmethod
    def stix_scanner_setup(ids):
        def mock_scanner(query, filter):
            for edge_namespace, edge_id in ids.iteritems():
                yield mock.Mock(id_=edge_id, id_ns=edge_namespace)
        return mock_scanner

    @mock.patch('publisher_edge_object.STIXScanner')
    def test_GetNamespaces_NamespacesOK_ReturnsCorrectValues(self, mock_stix_scanner):
        patcher = mock.patch('publisher_edge_object.PublisherEdgeObject.__bases__', (mock.MagicMock,))
        with patcher:
            patcher.is_local = True
            mock_stix_scanner.side_effect = PublisherEdgeObjectTests.stix_scanner_setup(PublisherEdgeObjectTests.ok_ids)
            edge_object_under_test = PublisherEdgeObject(None)
            edge_object_under_test.id_ = None
            edge_object_under_test.filters = None
            namespaces = edge_object_under_test.ns_dict()
            self.assertEqual(namespaces, {
                'http://www.namespace-1.com': 'Alias_1',
                'http://www.namespace-2.com': 'Alias_2'
            })

    @mock.patch('publisher_edge_object.STIXScanner')
    def test_GetNamespaces_NoAlias_ReturnsNothing(self, mock_stix_scanner):
        patcher = mock.patch('publisher_edge_object.PublisherEdgeObject.__bases__', (mock.MagicMock,))
        with patcher:
            patcher.is_local = True
            mock_stix_scanner.side_effect = PublisherEdgeObjectTests.stix_scanner_setup(
                PublisherEdgeObjectTests.empty_alias_id)
            edge_object_under_test = PublisherEdgeObject(None)
            edge_object_under_test.id_ = None
            edge_object_under_test.filters = None
            namespaces = edge_object_under_test.ns_dict()
            self.assertEqual(namespaces, {})

    @mock.patch('publisher_edge_object.STIXScanner')
    def test_GetNamespaces_MalformedID_ThrowsException(self, mock_stix_scanner):
        patcher = mock.patch('publisher_edge_object.PublisherEdgeObject.__bases__', (mock.MagicMock,))
        with patcher:
            patcher.is_local = True
            mock_stix_scanner.side_effect = PublisherEdgeObjectTests.stix_scanner_setup(
                PublisherEdgeObjectTests.malformed_id)
            edge_object_under_test = PublisherEdgeObject(None)
            edge_object_under_test.id_ = None
            edge_object_under_test.filters = None
            self.assertRaises(Exception, edge_object_under_test.ns_dict)


if __name__ == '__main__':
    unittest.main()
