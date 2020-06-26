import os
import subprocess
from os import environ
import shutil
from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.GenomeFileUtilClient import GenomeFileUtil
from installed_clients.WorkspaceClient import Workspace
from installed_clients.ReadsUtilsClient import ReadsUtils
from installed_clients.SetAPIServiceClient import SetAPI
from installed_clients.DataFileUtilClient import DataFileUtil
from pprint import pprint,pformat

try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

class LoadreadsUtils:

    def __init__(self, scratch):
       self.scratch = scratch
       self.callback_url = os.environ['SDK_CALLBACK_URL']
       config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
       self.cfg = {}
       config = ConfigParser()
       config.read(config_file)
       for nameval in config.items('kb_Bwa'):
           self.cfg[nameval[0]] = nameval[1]

       self.srv_wiz_url = self.cfg['srv-wiz-url']
       pass 

    def loadSingleEndReads(self, single_end_fastq, params):
        if hasattr(self.__class__, 'se_reads_ref'):
            return self.__class__.se_reads_ref

        fq_path = os.path.join(self.scratch, 'extracted_WT_rep1.fastq')
        #shutil.copy(os.path.join('data', 'bt_test_data', 'extracted_WT_rep1.fastq'), fq_path)
        shutil.copy(single_end_fastq, fq_path)
        ru = ReadsUtils(self.callback_url)
        se_reads_ref = ru.upload_reads({'fwd_file': fq_path,
                                        'wsname': params["workspace_name"],
                                        'name': 'test_readsSE',
                                        'sequencing_tech': 'artificial reads'})['obj_ref']
        self.__class__.se_reads_ref = se_reads_ref
        print('Loaded SingleEndReads: ' + se_reads_ref)
        return se_reads_ref

    def loadPairedEndReads(self, fwd_reads, rev_reads, params):
        if hasattr(self.__class__, 'pe_reads_ref'):
            return self.__class__.pe_reads_ref
        # return '23735/3/1'
        fq_path1 = os.path.join(self.scratch, 'reads_1.fq')
        fq_path2 = os.path.join(self.scratch, 'reads_2.fq')
        shutil.copy(fwd_reads, fq_path1)
        shutil.copy(fwd_reads, fq_path2)
        #shutil.copy(os.path.join('data', 'bt_test_data', 'reads_1.fq'), fq_path1)
        #shutil.copy(os.path.join('data', 'bt_test_data', 'reads_2.fq'), fq_path2)

        ru = ReadsUtils(self.callback_url)
        pe_reads_ref = ru.upload_reads({'fwd_file': fq_path1, 'rev_file': fq_path2,
                                        'wsname' : params["workspace_name"],
                                        'name': 'test_readsPE',
                                        'sequencing_tech': 'artificial reads'})['obj_ref']
        self.__class__.pe_reads_ref = pe_reads_ref
        print('Loaded PairedEndReads: ' + pe_reads_ref)
        return pe_reads_ref

    def loadGenome(self, test_gbk_file, params):
        if hasattr(self.__class__, 'genome_ref'):
            return self.__class__.genome_ref

        #test_gbk_file = os.path.join("data", "bt_test_data", "at_chrom1_section.gbk")

        gbk_file = os.path.join(self.scratch, os.path.basename(test_gbk_file))
        shutil.copy(test_gbk_file, gbk_file)

        genome_ref = self.gfu.genbank_to_genome({
            "file": {
                "path": gbk_file
            },
            "genome_name": 'my_test_genome',
            "workspace_name": params["workspace_name"],
            "source": "Ensembl",
            "type": "User upload",
            "generate_ids_if_needed": 1
        }).get('genome_ref')

        self.__class__.genome_ref = genome_ref
        print('Loaded Genome: ' + genome_ref)
        return genome_ref

    def loadAssembly(self, assembly_file, params):
        if hasattr(self.__class__, 'assembly_ref'):
            return self.__class__.assembly_ref
        # return '23735/1/1'
        fasta_path = os.path.join(self.scratch, 'Ptrichocarpa_v3.1.assembly.fna')

        shutil.copy(assembly_file, fasta_path)
        #shutil.copy(os.path.join('/kb/module/test/data', 'Ptrichocarpa_v3.1.assembly.fna'), fasta_path)
        au = AssemblyUtil(self.callback_url)
        assembly_ref = au.save_assembly_from_fasta({'file': {'path': fasta_path},
                                                    'workspace_name': params["workspace_name"],
                                                    'assembly_name': 'test_assembly'
                                                    })
        self.__class__.assembly_ref = assembly_ref
        print('Loaded Assembly: ' + assembly_ref)
        return assembly_ref

    def loadSampleSet(self, fwd_reads, rev_reads, params ):
        if hasattr(self.__class__, 'sample_set_ref'):
            return self.__class__.sample_set_ref
        # return '23735/4/1'
        pe_reads_ref = self.loadPairedEndReads(fwd_reads, rev_reads, params)
        sample_set_name = 'TestSampleSet'
        sample_set_data = {'Library_type': 'PairedEnd',
                           'domain': "Prokaryotes",
                           'num_samples': 3,
                           'platform': None,
                           'publication_id': None,
                           'sample_ids': [pe_reads_ref, pe_reads_ref, pe_reads_ref],
                           'sampleset_desc': None,
                           'sampleset_id': sample_set_name,
                           'condition': ['ss1', 'ss2', 'ss3'],
                           'source': None
                           }
        ss_obj = self.getWsClient().save_objects({'workspace': params["workspace_name"],
                                                  'objects': [{'type': 'KBaseRNASeq.RNASeqSampleSet',
                                                               'data': sample_set_data,
                                                               'name': sample_set_name,
                                                               'provenance': [{}]
                                                               }]
                                                  })
        ss_ref = "{}/{}/{}".format(ss_obj[0][6], ss_obj[0][0], ss_obj[0][4])
        print('Loaded SampleSet: ' + ss_ref)
        return ss_ref

    def loadReadsSet(self, fwd_reads, rev_reads, params):
        if hasattr(self.__class__, 'reads_set_ref'):
            return self.__class__.reads_set_ref
        pe_reads_ref = self.loadPairedEndReads(fwd_reads, rev_reads, params)
        reads_set_name = 'TestReadsSet'
        # create the set object

        reads_set_data = {
            'description': 'Reads Set for testing Bwa',
            'items': [{
                'ref': pe_reads_ref,
                'label': 'rs1'
             }]
        }
        # test a save
        set_api = SetAPI(self.srv_wiz_url)
        res = set_api.save_reads_set_v1({
            'data': reads_set_data,
            'output_object_name': reads_set_name,
            'workspace': params["workspace_name"]
        })
        reads_set_ref = res['set_ref']

        # reads_set_ref = '5264/52/1'
        print('Loaded ReadsSet: ' + reads_set_ref)
        return reads_set_ref
