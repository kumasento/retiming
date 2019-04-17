# retiming

![Travis CI](https://travis-ci.com/kumasento/retiming.svg?branch=master)
[![codecov](https://codecov.io/gh/kumasento/retiming/branch/master/graph/badge.svg)](https://codecov.io/gh/kumasento/retiming)


A Python implementation of the paper "Retiming Synchronous Circuitry" by Leiserson et al.

## Install

Use `environment.yml` and Anaconda3.

## Overview

This repository contains a `retiming` module that consists of the following sub-modules:

1. `circuit`: utilities to construct a graph representing a circuit
2. `transform`: transformations on a circuit graph, including _retime_