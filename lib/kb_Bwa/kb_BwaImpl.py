# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
from pprint import pprint
from kb_Bwa.util.BwaIndexBuilder import BwaIndexBuilder
from kb_Bwa.util.BwaAligner import BwaAligner
from kb_Bwa.util.BwaRunner import BwaRunner

from installed_clients.KBaseReportClient import KBaseReport
#END_HEADER


class kb_Bwa:
    '''
    Module Name:
    kb_Bwa

    Module Description:
    A KBase module: kb_Bwa
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/man4ish/kb_Bwa.git"
    GIT_COMMIT_HASH = "90da33585c5d7568a85322052dd36d7d0219a0c7"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspace_url = config['workspace-url']
        self.srv_wiz_url = config['srv-wiz-url']
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def align_reads_to_assembly_app(self, ctx, params):
        """
        :param params: instance of type "AlignReadsParams" -> structure:
           parameter "input_ref" of String, parameter
           "assembly_or_genome_ref" of String, parameter "output_name" of
           String, parameter "output_workspace" of String, parameter
           "output_obj_name_suffix" of String, parameter
           "output_alignment_suffix" of String, parameter "condition_label"
           of String, parameter "phred33" of String, parameter "phred64" of
           String, parameter "local" of String, parameter "very-fast" of
           String, parameter "fast" of String, parameter "very-sensitive" of
           String, parameter "sensitive" of String, parameter
           "very-fast-local" of String, parameter "very-sensitive-local" of
           String, parameter "fast-local" of String, parameter
           "fast-sensitive" of String, parameter "quality_score" of String,
           parameter "alignment_type" of String, parameter "trim5" of Long,
           parameter "trim3" of Long, parameter "np" of Long, parameter
           "preset_options" of String, parameter "minins" of Long, parameter
           "maxins" of Long, parameter "orientation" of String, parameter
           "concurrent_njsw_tasks" of Long, parameter
           "concurrent_local_tasks" of Long
        :returns: instance of type "AlignReadsResult" -> structure: parameter
           "reads_alignment_ref" of String, parameter
           "read_alignment_set_ref" of String, parameter "report_name" of
           String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN align_reads_to_assembly_app
        print('Running align_reads_to_assembly_app() with params=')
        pprint(params)
        bwa_aligner = BwaAligner(self.shared_folder, self.workspace_url,
                                         self.callback_url, self.srv_wiz_url,
                                         ctx.provenance())
        result = bwa_aligner.align(params)
        print(result)
        #END align_reads_to_assembly_app

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method align_reads_to_assembly_app return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]


    def align_one_reads_to_assembly(self, ctx):
        """
        aligns a single reads object to produce
        """
        # ctx is the context object
        #BEGIN align_one_reads_to_assembly
        #END align_one_reads_to_assembly
        pass

    def get_bwa_index(self, ctx, params):
        """
        :param params: instance of type "GetBwaIndex" -> structure: parameter
           "ref" of String, parameter "output_dir" of String, parameter
           "ws_for_cache" of String
        :returns: instance of type "GetBwaIndexResult" -> structure:
           parameter "output_dir" of String, parameter "from_cache" of type
           "boolean" (This example function accepts any number of parameters
           and returns results in a KBaseReport), parameter "pushed_to_cache"
           of type "boolean" (This example function accepts any number of
           parameters and returns results in a KBaseReport)
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN get_bwa_index
        bwaIndexBuilder = BwaIndexBuilder(self.shared_folder, self.workspace_url,
                                          self.callback_url, self.srv_wiz_url,
                                          ctx.provenance())
        result = bwaIndexBuilder.get_index(params)
        #END get_bwa_index

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method get_bwa_index return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def run_kb_Bwa(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_kb_Bwa



        report = KBaseReport(self.callback_url)
        report_info = report.create({'report': {'objects_created':[],
                                                'text_message': "report submitted"},
                                                'workspace_name': params['workspace_name']})
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }
        #END run_kb_Bwa

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_kb_Bwa return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
