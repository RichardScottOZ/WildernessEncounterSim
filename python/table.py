#!/usr/bin/env python3
"""
Generic text game table read from CSV file.

Row and column numbering is 1-indexed.
Table in CSV file must be rectangular (every row & column same size).
Null values can be represented by a single dash ("-").

@author   Daniel R. Collins (dcollins@superdan.net)
@since    2021-12-05
Ported to Python by GitHub Copilot
"""

import csv
from dice import Dice


class Table:
    """Generic game table loaded from CSV file."""
    
    # Null entry value
    NULL_ENTRY = "-"
    
    def __init__(self, filename):
        """
        Constructor.
        @param filename CSV file to read
        """
        self.table = self._read_csv_file(filename)
    
    @staticmethod
    def _read_csv_file(filename):
        """
        Read CSV file into 2D array.
        @param filename File to read
        @return 2D array of strings
        """
        table = []
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                table.append(row)
        return table
    
    def get_num_rows(self):
        """Get the number of rows (excluding header)."""
        return len(self.table) - 1
    
    def get_num_cols(self):
        """Get the number of columns (excluding first column)."""
        return len(self.table[0]) - 1 if self.table else 0
    
    def get_row_name(self, index):
        """
        Get title of a row.
        @param index 1-indexed row number
        """
        return self.table[index][0]
    
    def get_col_name(self, index):
        """
        Get title of a column.
        @param index 1-indexed column number
        """
        return self.table[0][index]
    
    def get_row_from_name(self, name):
        """
        Get index of row from name.
        @param name Row name to find
        @return 1-indexed row number, or -1 if not found
        """
        for i in range(1, len(self.table)):
            if self.table[i][0] == name:
                return i
        return -1
    
    def get_col_from_name(self, name):
        """
        Get index of column from name.
        @param name Column name to find
        @return 1-indexed column number, or -1 if not found
        """
        for i in range(1, len(self.table[0])):
            if self.table[0][i] == name:
                return i
        return -1
    
    def get_random_entry_on_row(self, index):
        """
        Get uniformly random entry in a given row.
        @param index 1-indexed row number
        @return Random non-null entry
        """
        max_attempts = 1000
        attempts = 0
        while attempts < max_attempts:
            roll = Dice.roll(self.get_num_cols())
            entry = self.table[index][roll]
            if entry != self.NULL_ENTRY:
                return entry
            attempts += 1
        raise ValueError(f"No non-null entries found in row {index} after {max_attempts} attempts")
    
    def get_random_entry_on_col(self, index):
        """
        Get uniformly random entry in a given column.
        @param index 1-indexed column number
        @return Random non-null entry
        """
        max_attempts = 1000
        attempts = 0
        while attempts < max_attempts:
            roll = Dice.roll(self.get_num_rows())
            entry = self.table[roll][index]
            if entry != self.NULL_ENTRY:
                return entry
            attempts += 1
        raise ValueError(f"No non-null entries found in column {index} after {max_attempts} attempts")
    
    def get_entry(self, row, col):
        """
        Get entry given row and column.
        @param row 1-indexed row number
        @param col 1-indexed column number
        @return Entry at given position
        """
        return self.table[row][col]
