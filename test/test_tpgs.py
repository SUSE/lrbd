
from lrbd import entries, TPGs, Common, Runtime
from nose.tools import  *
import tempfile
import unittest
import mock
import logging

class TPGsTestCase(unittest.TestCase):

    def setUp(self):
        Common.config = { 
            "pools": [ 
                { "pool": "rbd", 
                  "gateways": [
                    { "host": "igw1", "tpg": [ 
                        { "image": "archive" } 
                        ] 
                    } ] 
                } ] }


    @mock.patch('lrbd.addresses')
    def test_tpgs(self, mock_subproc_addresses):
        class mock_TPGs(TPGs):

            def _add(self):
                pass

            def _remote(self):
                pass

            def _add_target(self):
                pass

            def disable_auto_add_default_portal(self):
                pass

        class Portal_Index(object):
            def portals(self):
                pass

        _pi = Portal_Index()
        self.t = mock_TPGs(None, _pi, None)
        assert ('addresses' in Runtime.config and
            'portals' in Runtime.config)

    def test_add_none(self):
        class mock_TPGs(TPGs):

            def _add(self):
                pass

            def _check_portal(self):
                pass

            def disable_auto_add_default_portal(self):
                pass


        class Portal_Index(object):
            def portals(self):
                pass

        _pi = Portal_Index()
        self.t = mock_TPGs(None, _pi, None)
        assert not self.t.cmds

    def test_add(self):
        Common.config = { 
            "iqns": [ "iqn.xyz" ],
            "pools": [ 
                { "pool": "rbd", 
                  "gateways": [
                    { "host": "igw1", "tpg": [ 
                        { "image": "archive", "portal": "portal1" } 
                        ] 
                    } ] 
                } ] }
        class mock_TPGs(TPGs):

            def _remote(self):
                pass

            def _check_portal(self, name):
                pass

            def _add_host(self, entry, target):
                pass

            def disable_auto_add_default_portal(self):
                pass

        class Portal_Index(object):
            def portals(self):
                pass
            def add(self, target, image):
                pass

        class TPG_Counter(object):
            def reset_all(self):
                pass

            def add(self, target):
                pass

        _pi = Portal_Index()
        _tc = TPG_Counter()
        logging.disable(logging.DEBUG)
        self.t = mock_TPGs(_tc, _pi, None)
        assert (self.t.cmds == [])

    def test_check_portal(self):
        Common.config['portals'] = [ { "name": "portal1" } ]
        class mock_TPGs(TPGs):

            def _add(self):
                pass

            def _remote(self):
                pass

            def disable_auto_add_default_portal(self):
                pass

        class Portal_Index(object):
            def portals(self):
                pass

        _pi = Portal_Index()
        self.t = mock_TPGs(None, _pi, None)
        assert self.t._check_portal("portal1") == None

    @raises(ValueError)
    def test_check_portal_undefined(self):
        Common.config['portals'] = [ { "name": "portal1" } ]
        class mock_TPGs(TPGs):

            def _add(self):
                pass

            def _remote(self):
                pass

            def disable_auto_add_default_portal(self):
                pass

        class Portal_Index(object):
            def portals(self):
                pass

        _pi = Portal_Index()
        self.t = mock_TPGs(None, _pi, None)
        self.t._check_portal("portal2")

    @mock.patch('glob.glob')
    def test_cmd(self, mock_subproc_glob):
        class mock_TPGs(TPGs):

            def _add(self):
                pass

            def _remote(self):
                pass

            def disable_auto_add_default_portal(self):
                pass

        class Portal_Index(object):
            def portals(self):
                pass

        _pi = Portal_Index()
        self.t = mock_TPGs(None, _pi, None)
        mock_subproc_glob.return_value = []
        result = self.t._cmd("iqn.xyz", "2")
        assert result == ['targetcli', '/iscsi/iqn.xyz', 'create 2']

    @mock.patch('glob.glob')
    def test_cmd_returns_empty(self, mock_subproc_glob):
        class mock_TPGs(TPGs):

            def _add(self):
                pass

            def _remote(self):
                pass

            def disable_auto_add_default_portal(self):
                pass

        class Portal_Index(object):
            def portals(self):
                pass

        _pi = Portal_Index()
        self.t = mock_TPGs(None, _pi, None)
        mock_subproc_glob.return_value = "/some/path"
        result = self.t._cmd("iqn.xyz", "2")
        assert result == []

    @mock.patch('lrbd.Popen')
    def test_create(self, mock_popen):

        mock_popen.return_value.returncode = 0

        class mock_TPGs(TPGs):

            def _add(self):
                pass

            def _remote(self):
                pass

            def disable_auto_add_default_portal(self):
                pass

        class Portal_Index(object):
            def portals(self):
                pass

        class TargetcliDispatcher:

             def queue_cmd(self, cmd):
                 pass

             def flush_close(self):
                 pass

        _pi = Portal_Index()
        self.t = mock_TPGs(None, _pi, None)
        self.t.cmds = [ [ "targetcli", "hello" ] ]
        self.t.create()

        assert mock_popen.called





