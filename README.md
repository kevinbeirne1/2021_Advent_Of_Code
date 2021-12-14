# 2021 Advent of Code

Repo for my solutions to the problems for the 2021 Advent of Code challenge
There are 2 problems released each day, from 1st December to the 25th. 

## Contents
- [Problem Overview](#problem-overview)

## Problem Overview
An extremely brief description of what each days problems are asking for. 
The individual files for each day have the full text of the problem description


### 01DEC21 - Sonar Sweep
1. Given an array of numbers count the number of times that numbers[ i ] > numbers[ i + 1]
2. With the same array of numbers count the number of times that group numbers[ i : i + 3] > numbers[ i + 1 : i + 4]
### 02DEC21 - Dive!
1. Given an array of `direction number` calculate a final position vector
2. With same array, directions have different affects
### 03DEC21 - Binary Diagnostic
1. Array of binary numbers - get the most common bit at each position, and it's bit inverse
2. With same array, at each bit position exclude the numbers that have the most/least common bit at that position.
### 04DEC21 - Giant Squid
1. Array of bingo boards and drawn numbers, multiply the last drawn number by the sum of the non called numbers in winning board
2. Same array, get the same product for the last winning board
### 05DEC21 - Hydrothermal Venture
1. Array of vent vectors, calculate the number of nodes where horizontal/vertical vectors that overlap 
2. Same array, now include diagonal vectors
### 06DEC21 - Lanternfish
1. Array of times till fish births (with fixed period for birth), calculate the population after 80 days
2. Same array, calculate the population after 256 days
### 07DEC21 - The Treachery of Whales
1. Array of nodes. Find the minimum of the distances from each node to a single other node 
2. Same array, distance value increases at greater rate when further away. Calculate the new minimum node position
### 08DEC21 - Seven Segment Search
1. Array of strings, that correspond to the numbers 0-9 in 7 segment display, and 4 digit output. Count the number of times 1, 4, 7, 8 appear in output
2. Same array, decode the all the outputs and calculate the sum
### 09DEC21 - Smoke Basin 
1. Array of numbers, find the numbers that are less than all surrounding digits and sum them
2. Same array, find the three largest basins (areas enclosed by 9) and multiply their sizes
### 10DEC21 - Syntax Scoring
1. Array of strings containing various parentheses. In each string find the first invalid closing bracket
2. Same array, find the brackets that are required to created a valid completed string
### 11DEC21 - Dumbo Octopus
1. Array of numbers. Increment all the numbers in the grid, any number that would become 10 it 'flashes' and becomes 0 and increments all the surrounding numbers. Sum the number of flashes
2. Same array. Calculate the number of iterations that's needed for all the numbers to synchronise their flashes
### 12DEC21 - Passage Pathing
1. Array of strings, mapping out connections of nodes. Find all possible paths, where lower case nodes can only be visited once
2. Same array. Find all paths, when lower case can be visited twice

---
[2021 Advent of Code](https://adventofcode.com/2021/)

[Advent of Code Website](https://adventofcode.com/)