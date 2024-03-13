#!/usr/bin/env python3

from csv import reader as csv_reader
import sys

if len(sys.argv) != 2:
    sys.exit(f"Usage: ${sys.argv[0]} [tid-count.csv]")

with open(sys.argv[1], mode="r", encoding="utf-8") as tid_count_file:
  tid_count = csv_reader(tid_count_file, delimiter=",")
  tid_count_map: dict[str, int] = { tid: int(count) for tid, count in tid_count}

with open("slave-master.csv", mode="r", encoding="utf-8") as slave_master_file:
  slave_master = csv_reader(slave_master_file, delimiter=",")
  slave_master_map: dict[str, str] = { slave: master for slave, master in slave_master}

for slave, master in slave_master_map.items():
  if slave in tid_count_map and master in tid_count_map:
    slave_count = tid_count_map[slave]
    tid_count_map[master] += slave_count
    del tid_count_map[slave]

with open(sys.argv[1], mode="w+", encoding="utf-8") as tid_count_file:
  for tid, count in tid_count_map.items():
    print(tid, count, sep=',', file=tid_count_file)