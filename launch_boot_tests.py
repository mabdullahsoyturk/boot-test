#!/usr/bin/env python3

#This is a job launch script for boot tests

import os
import sys
from uuid import UUID

from gem5art.artifact.artifact import Artifact
from gem5art.run import gem5Run
from gem5art.tasks.tasks import run_gem5_instance

packer = Artifact.registerArtifact(
    command = '''wget https://releases.hashicorp.com/packer/1.4.3/packer_1.4.3_linux_amd64.zip;
    unzip packer_1.4.3_linux_amd64.zip;
    ''',
    typ = 'binary',
    name = 'packer',
    path =  'disk-image/packer',
    cwd = 'disk-image',
    documentation = 'Program to build disk images. Downloaded sometime in August from hashicorp.'
)

experiments_repo = Artifact.registerArtifact(
    command = 'git clone https://github.com/mabdullahsoyturk/boot-tests',
    typ = 'git repo',
    name = 'boot-tests',
    path =  './',
    cwd = '../',
    documentation = 'main experiments repo to run full system boot tests with gem5'
)

gem5_repo = Artifact.registerArtifact(
    command = 'git clone https://gem5.googlesource.com/public/gem5',
    typ = 'git repo',
    name = 'gem5',
    path =  'gem5/',
    cwd = './',
    documentation = 'cloned gem5 master branch from googlesource (Nov 18, 2019)'
)

m5_binary = Artifact.registerArtifact(
    command = 'make -f Makefile.x86',
    typ = 'binary',
    name = 'm5',
    path =  'gem5/util/m5/m5',
    cwd = 'gem5/util/m5',
    inputs = [gem5_repo,],
    documentation = 'm5 utility'
)

disk_image = Artifact.registerArtifact(
    command = './packer build boot-exit/boot-exit.json',
    typ = 'disk image',
    name = 'boot-disk',
    cwd = 'disk-image',
    path = 'disk-image/boot-exit-image/boot-exit',
    inputs = [packer, experiments_repo, m5_binary,],
    documentation = 'Ubuntu with m5 binary installed and root auto login'
)

gem5_binary = Artifact.registerArtifact(
    command = '''cd gem5;
    git checkout d40f0bc579fb8b10da7181;
    scons build/X86/gem5.opt -j8
    ''',
    typ = 'gem5 binary',
    name = 'gem5',
    cwd = 'gem5/',
    path =  'gem5/build/X86/gem5.opt',
    inputs = [gem5_repo,],
    documentation = 'gem5 binary based on googlesource (Nov 18, 2019)'
)

linux_repo = Artifact.registerArtifact(
    command = '''git clone https://github.com/torvalds/linux.git;
    mv linux linux-stable''',
    typ = 'git repo',
    name = 'linux-stable',
    path =  'linux-stable/',
    cwd = './',
    documentation = 'linux kernel source code repo from Sep 23rd'
)

linuxes = ['5.2.3']
linux_binaries = {
    version: Artifact.registerArtifact(
                name = f'vmlinux-{version}',
                typ = 'kernel',
                path = f'linux-stable/vmlinux-{version}',
                cwd = 'linux-stable/',
                command = f'''git checkout v{version};
                cp ../linux-configs/config.{version} .config;
                make -j8;
                cp vmlinux vmlinux-{version};
                ''',
                inputs = [experiments_repo, linux_repo,],
                documentation = f"Kernel binary for {version} with simple "
                                 "config file",
            )
    for version in linuxes
}

if __name__ == "__main__":
    boot_types = ['init']
    num_cpus = ['1']
    cpu_types = ['atomic']
    mem_types = ['classic']

    for linux in linuxes:
        for boot_type in boot_types:
            for cpu in cpu_types:
                for num_cpu in num_cpus:
                    for mem in mem_types:
                        print('results/run_exit/vmlinux-{}/boot-exit/{}/{}/{}/{}'.
                            format(linux, cpu, mem, num_cpu, boot_type))
                        run = gem5Run.createFSRun(
                            'run_name', # Name : str
                            'gem5/build/X86/gem5.opt', # gem5_binary : str
                            'config-boot-tests/run_exit.py', # run_script : str
                            'results/run_exit/vmlinux-{}/boot-exit/{}/{}/{}/{}'.format(linux, cpu, mem, num_cpu, boot_type), # outdir
                            gem5_binary, # gem5 artifact  
                            gem5_repo,   # gem5_git_artifact 
                            experiments_repo, # run script git artifact
                            os.path.join('linux-stable', 'vmlinux'+'-'+linux), # linux_binary : str
                            'disk-image/boot-exit-image/boot-exit', # disk_image : str
                            linux_binaries[linux], # linux_binary_artifact 
                            disk_image, # disk_image_artifact
                            cpu, mem, num_cpu, boot_type, # parameters
                            timeout = 6*60*60 # 6 hours
                            )
                        run_gem5_instance.apply_async((run,))
