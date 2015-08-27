
from lrbd import Auth, Common
from nose.tools import  *
import unittest, mock
import re, tempfile

class AuthTestCase(unittest.TestCase):

    def test_auth_default(self):
        del Common.config['auth']
        class mock_Auth(Auth):

            def set_noauth(self):
                return("noauth")

            def set_discovery_off(self):
                return("discovery off")
            
        self.a = mock_Auth()
        assert self.a.cmds == [ 'noauth', 'discovery off' ]

    def test_auth_none(self):
        Common.config['auth'] = [ { "authentication": "none" } ]
        class mock_Auth(Auth):

            def set_noauth(self):
                return("noauth")
            def select_discovery(self):
                return([ "select_discovery" ])
            
        self.a = mock_Auth()
        print self.a.cmds
        assert self.a.cmds == ['noauth', 'select_discovery']

    def test_auth_tpg(self):
        Common.config['auth'] = [ { "authentication": "tpg" } ]
        class mock_Auth(Auth):

            def select_tpg(self):
                return([ "tpg" ])
            def select_discovery(self):
                return([ "select_discovery" ])
            
        self.a = mock_Auth()
        assert self.a.cmds == ['tpg', 'select_discovery']

    def test_auth_acls(self):
        Common.config['auth'] = [ { "authentication": "acls" } ]
        class mock_Auth(Auth):

            def select_acls(self):
                return([ "acls" ])
            def select_discovery(self):
                return([ "select_discovery" ])
            
        self.a = mock_Auth()
        assert self.a.cmds == ['acls', 'select_discovery']

    @raises(ValueError)
    def test_auth_invalid(self):
        Common.config['auth'] = [ { "authentication": "invalid" } ]
            
        self.a = Auth()

    def test_select_discovery_default(self):
        del Common.config['auth']
        class mock_Auth(Auth):

            def set_noauth(self):
                return("noauth")
            
            def set_discovery_off(self):
                return("discovery off")

        self.a = mock_Auth()
        assert self.a.cmds == [ 'noauth', 'discovery off' ]

    def test_select_discovery_off(self):
        Common.config['auth'] = [ { "authentication": "none" } ]
        class mock_Auth(Auth):

            def set_noauth(self):
                return("noauth")
            def set_discovery_off(self):
                return("discovery off")
            
        self.a = mock_Auth()
        assert self.a.cmds == [ 'noauth', 'discovery off' ]

    def test_select_discovery_off_explicit(self):
        Common.config['auth'] = [ { "authentication": "none",
                                    "discovery": { "auth": "disable" } } ]
        class mock_Auth(Auth):

            def set_noauth(self):
                return("noauth")
            def set_discovery_off(self):
                return("discovery off")
            
        self.a = mock_Auth()
        assert self.a.cmds == [ 'noauth', 'discovery off' ]

    def test_select_discovery_on(self):
        Common.config['auth'] = [ { "authentication": "none",
                                    "discovery": { "auth": "enable" } } ]
        class mock_Auth(Auth):

            def set_noauth(self):
                return("noauth")
            def set_discovery(self):
                return("discovery on")
            
        self.a = mock_Auth()
        assert self.a.cmds == [ 'noauth', 'discovery on' ]

    def test_select_discovery_on_mutual_off(self):
        Common.config['auth'] = [ { "authentication": "none",
                                    "discovery": { "auth": "enable",
                                                   "mutual": "disable" } } ]
        class mock_Auth(Auth):

            def set_noauth(self):
                return("noauth")
            def set_discovery(self):
                return("discovery on")
            
        self.a = mock_Auth()
        assert self.a.cmds == [ 'noauth', 'discovery on' ]

    def test_select_discovery_on_mutual_on(self):
        Common.config['auth'] = [ { "authentication": "none",
                                    "discovery": { "auth": "enable",
                                                   "mutual": "enable" } } ]
        class mock_Auth(Auth):

            def set_noauth(self):
                return("noauth")
            def set_discovery_mutual(self):
                return("discovery_mutual on")
            
        self.a = mock_Auth()
        assert self.a.cmds == [ 'noauth', 'discovery_mutual on' ]

    def test_select_tpg(self):
        Common.config['auth'] = [ { "authentication": "tpg",
                                    "tpg": {} } ]
        class mock_Auth(Auth):

            def set_tpg(self):
                return("tpg")
            
            def set_tpg_mode(self):
                return("tpg mode")

            def set_discovery_off(self):
                return("discovery off")
            
        self.a = mock_Auth()
        assert self.a.cmds == ['tpg', 'tpg mode', 'discovery off']

    def test_select_tpg_mutual_off(self):
        Common.config['auth'] = [ { "authentication": "tpg",
                                    "tpg": { "mutual": "disable"} } ]
        class mock_Auth(Auth):

            def set_tpg(self):
                return("tpg")
            
            def set_tpg_mode(self):
                return("tpg mode")

            def set_discovery_off(self):
                return("discovery off")
            
        self.a = mock_Auth()
        assert self.a.cmds == ['tpg', 'tpg mode', 'discovery off']

    def test_select_tpg_mutual_on(self):
        Common.config['auth'] = [ { "authentication": "tpg",
                                    "tpg": { "mutual": "enable"} } ]
        class mock_Auth(Auth):

            def set_tpg_mutual(self):
                return("tpg mutual")
            
            def set_tpg_mode(self):
                return("tpg mode")

            def set_discovery_off(self):
                return("discovery off")
            
        self.a = mock_Auth()
        assert self.a.cmds == ['tpg mutual', 'tpg mode', 'discovery off']

    def test_select_acls_default(self):
        Common.config['auth'] = [ { "authentication": "acls",
                                    "acls": {} } ]
        class mock_Auth(Auth):

            def set_acls(self):
                return("acls")
            
            def set_acls_mode(self):
                return("acls mode")

            def set_discovery_off(self):
                return("discovery off")
            
        self.a = mock_Auth()
        assert self.a.cmds == ['acls mode', 'discovery off']

    def test_select_acls(self):
        Common.config['auth'] = [ { "authentication": "acls",
                                    "acls": { "initiator": "iqn.abc" } } ]
        class mock_Auth(Auth):

            def set_acls(self):
                return("acls")
            
            def set_acls_mode(self):
                return("acls mode")

            def set_discovery_off(self):
                return("discovery off")
            
        self.a = mock_Auth()
        assert self.a.cmds == ['acls', 'acls mode', 'discovery off']

    def test_select_acls_mutual_off(self):
        Common.config['auth'] = [ { "authentication": "acls",
                                    "acls": [ { "initiator": "iqn.abc",
                                              "mutual": "disable" } ] } ]
        class mock_Auth(Auth):

            def set_acls(self):
                return("acls")
            
            def set_acls_mode(self):
                return("acls mode")

            def set_discovery_off(self):
                return("discovery off")
            
        self.a = mock_Auth()
        assert self.a.cmds == ['acls', 'acls mode', 'discovery off']

    def test_select_acls_mutual_on(self):
        Common.config['auth'] = [ { "authentication": "acls",
                                    "acls": [ { "initiator": "iqn.abc",
                                              "mutual": "enable" } ] } ]
        class mock_Auth(Auth):

            def set_acls_mutual(self):
                return("acls mutual")
            
            def set_acls_mode(self):
                return("acls mode")

            def set_discovery_off(self):
                return("discovery off")
            
        self.a = mock_Auth()
        assert self.a.cmds == ['acls mutual', 'acls mode', 'discovery off']

    @mock.patch('lrbd.popen')
    def test_create(self, mock_subproc_popen):
        del Common.config['auth']
        class mock_Auth(Auth):

            def set_noauth(self):
                return("noauth")
            
            def set_discovery_off(self):
                return("discovery off")

        self.a = mock_Auth()
        self.a.create()
        assert mock_subproc_popen.called

