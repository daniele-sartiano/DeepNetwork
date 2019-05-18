#!/usr/bin/env python

from reader import FlowReader


def main():
    f = FlowReader([1,2,3,4])
    f.read()

if __name__ == '__main__':
    main()
