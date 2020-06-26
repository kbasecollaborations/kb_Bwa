# -*- coding: utf-8 -*-
import os
import time
import unittest
import shutil
from configparser import ConfigParser

from kb_Bwa.kb_BwaImpl import kb_Bwa
from kb_Bwa.kb_BwaServer import MethodContext
from kb_Bwa.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace

from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.GenomeFileUtilClient import GenomeFileUtil

class kb_BwaTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_Bwa'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_Bwa',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = kb_Bwa(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')



    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_kb_Bowtie2_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def loadGenome(self):
        if hasattr(self.__class__, 'genome_ref'):
            return self.__class__.genome_ref
        genbank_file_path = os.path.join(self.scratch, 'minimal.gbff')
        shutil.copy(os.path.join('data', 'minimal.gbff'), genbank_file_path)
        gfu = GenomeFileUtil(self.callback_url)
        genome_ref = gfu.genbank_to_genome({'file': {'path': genbank_file_path},
                                            'workspace_name': self.getWsName(),
                                            'genome_name': 'test_genome',
                                            'source': 'Ensembl',
                                            'generate_ids_if_needed': 1,
                                            'generate_missing_genes': 1
                                            })['genome_ref']
        self.__class__.genome_ref = genome_ref
        return genome_ref

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    '''
    def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        genome_ref = self.loadGenome()

        ret = self.serviceImpl.run_kb_Bwa(self.ctx, {'workspace_name': self.wsName,
                                                         'parameter_1': 'Hello World!'})
    '''

    def test_build_bowtie2_index_from_genome(self):

        # finally, try it with a genome_ref instead
        #genome_ref = self.loadGenome()
        params = {
                   'workspace': 'man4ish_gupta:narrative_1592707902187', 'assembly_or_genome_ref': '43745/33/4',
                   'output_obj_name_suffix': 'readsAlignment1', 'input_ref' :'43745/22/1',
                   'output_alignment_suffix': '_some_ext'
                  }
        #res = self.getImpl().get_bwa_index(self.getContext(), params)
        res = self.getImpl().align_reads_to_assembly_app(self.getContext(), params)



