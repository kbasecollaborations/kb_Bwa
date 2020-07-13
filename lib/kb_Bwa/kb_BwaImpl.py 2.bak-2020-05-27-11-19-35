# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
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
    GIT_COMMIT_HASH = "5cd4cb691be7b7579a7e3ccd7fabd5cb1ada833e"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_kb_Bwa(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_kb_Bwa
        report = KBaseReport(self.callback_url)
        report_info = report.create({'report': {'objects_created':[],
                                                'text_message': params['parameter_1']},
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

    def get_bwa_index(self, ctx, params):
        """
        :param params: instance of type "GetBowtie2Index" (Provide a
           reference to either an Assembly or Genome to get a Bowtie2 index.
           output_dir is optional, if provided the index files will be saved
           in that directory.  If not, a directory will be generated for you
           and returned by this function.  If specifying the output_dir, the
           directory must not exist yet (to ensure only the index files are
           added there). Currently, Bowtie2 indexes are cached to a WS
           object.  If that object does not exist, then calling this function
           can create a new object.  To create the cache, you must specify
           the ws name or ID in 'ws_for_cache' in which to create the cached
           index.  If this field is not set, the result will not be cached.
           This parameter will eventually be deprecated once the big file
           cache service is implemented.) -> structure: parameter "ref" of
           String, parameter "output_dir" of String, parameter "ws_for_cache"
           of String
        :returns: instance of type "GetBowtie2IndexResult" (output_dir - the
           folder containing the index files from_cache - 0 if the index was
           built fresh, 1 if it was found in the cache pushed_to_cache - if
           the index was rebuilt and successfully added to the cache, this
           will be set to 1; otherwise set to 0) -> structure: parameter
           "output_dir" of String, parameter "from_cache" of type "boolean"
           (A boolean - 0 for false, 1 for true. @range (0, 1)), parameter
           "pushed_to_cache" of type "boolean" (A boolean - 0 for false, 1
           for true. @range (0, 1))
        """
        # ctx is the context object
        # return variables are: result
        # BEGIN get_bowtie2_index
        print('Running get_bowtie2_index() with params=')
        pprint(params)
        bwaIndexBuilder = BwaIndexBuilder(self.scratch_dir, self.workspace_url,
                                                  self.callback_url, self.srv_wiz_url,
                                                  ctx.provenance())
        result = bwaIndexBuilder.get_index(params)
        # END get_bowtie2_index

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method get_bowtie2_index return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
