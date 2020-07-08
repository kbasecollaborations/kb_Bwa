import os.path
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

        p = subprocess.Popen(command, cwd=cwd, shell=False)
        exitCode = p.wait()

        if (exitCode == 0):
            print('Success, exit code was: ' + str(exitCode))
        else:
            raise ValueError('Error running command: ' + ' '.join(command) + '\n' +
                             'Exit Code: ' + str(exitCode))
