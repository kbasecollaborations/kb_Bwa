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

    typedef structure {
        string input_ref;
        string assembly_or_genome_ref;
        string output_name;
        string output_workspace;
        string output_obj_name_suffix;
        string output_alignment_suffix;
    } AlignReadsParams;

    typedef structure {
        string reads_alignment_ref;
        string read_alignment_set_ref;
        string report_name;
        string report_ref;
    } AlignReadsResult;

    funcdef align_reads_to_assembly_app(AlignReadsParams params)
        returns (AlignReadsResult result) authentication required;

    /* aligns a single reads object to produce */
    funcdef align_one_reads_to_assembly()
        returns () authentication required;


    funcdef get_bwa_index(GetBwaIndex params)
        returns(GetBwaIndexResult result) authentication required;

    funcdef run_kb_Bwa(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
