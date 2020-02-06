#!/usr/bin/env python3
from pymongo import MongoClient

db = MongoClient().artifact_database

linuxes = ['5.2.3']
boot_types = ['init', 'systemd']
num_cpus = ['1', '2', '4', '8']
cpu_types = ['atomic']
mem_types = ['classic']

for linux in linuxes:
    for boot_type in boot_types:
        for cpu in cpu_types:
            for num_cpu in num_cpus:
                for mem in mem_types:
                    print('/home/muhammet/Desktop/boot-tests/results/run_exit/vmlinux-{}/boot-exit/{}/{}/{}/{}'.format(linux, cpu, mem, num_cpu, boot_type))
                    for i in db.artifacts.find({'outdir':'/home/muhammet/Desktop/boot-tests/results/run_exit/vmlinux-{}/boot-exit/{}/{}/{}/{}'.format(linux, cpu, mem, num_cpu, boot_type)}):
                        print(i)
