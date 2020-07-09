import os.path
import os
import subprocess


class BwaRunner:

    BWA_PATH = 'bwa'

    def __init__(self, scratch_dir):
        self.scratch_dir = scratch_dir
        self.valid_commands = ['index', 'aln', 'samse', "mem -t 32 -M -R '@RG\tID:sample_1\tLB:sample_1\tPL:ILLUMINA\tPM:HISEQ\tSM:sample_1'", 'pemerge', 'fastmap', 'sampe', 'bwasw']

    def run(self, command, options, cwd=None):
        ''' options is an array of command-line parameters passed to the RQCFilter App '''
        '''if command not in self.valid_commands:
            raise ValueError('Invalid bwa command: ' + str(command))'''


        command = [command] + options
        command.insert(0, self.BWA_PATH)

        print('In working directory: ' + ' '.join(command))
        print('Running: ' + ' '.join(command))

        print(command)

        if not cwd:
          cwd = self.scratch_dir
 
        cmd = ' '.join(command)

        os.system(cmd)   #TODO : need to remove system command 
        '''
        #command = ["bwa", "mem", "-t 32 -M -R '@RG\tID:sample_1\tLB:sample_1\tPL:ILLUMINA\tPM:HISEQ\tSM:sample_1'", "/kb/module/work/tmp/bwa_index_159417983426/test_assembly", "/kb/module/work/tmp/136f92bb-3068-4cbc-9f64-0a6f17c2f080.rev.fastq", "/kb/module/work/tmp/cfe08852-4d2b-42a9-a7ad-10d5bd93192a.fwd.fastq", ">", "/kb/module/work/tmp/bwa_alignment_output_15941803403611/reads_alignment.sam"]
               
        p = subprocess.Popen(command, cwd=cwd, shell=False)
        exitCode = p.wait()

        if (exitCode == 0):
            print('Success, exit code was: ' + str(exitCode))
        else:
            raise ValueError('Error running command: ' + ' '.join(command) + '\n' +
                             'Exit Code: ' + str(exitCode))
        '''                     
