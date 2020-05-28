/*
A KBase module: kb_Bwa
*/

module kb_Bwa {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */

typedef int boolean;

typedef structure {
        string ref;
        string output_dir;
        string ws_for_cache;
    } GetBwaIndex;


    typedef structure {
        string output_dir;
        boolean from_cache;
        boolean pushed_to_cache;
    } GetBwaIndexResult;

    funcdef get_bwa_index(GetBwaIndex params)
        returns(GetBwaIndexResult result) authentication required;

    funcdef run_kb_Bwa(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
