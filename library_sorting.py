#!/usr/bin/env python3
"""
library_sorting.py
------------------
Sparse “library–sorting” table, as specified in *library_sorting.pdf*.

Usage:
    python library_sorting.py <test-case.json>
"""

import sys
import argparse
import json


# ---------------------------------------------------------------------#
# Helpers
# ---------------------------------------------------------------------#
def bisect_left(a, x):
    """Minimal binary-search (leftmost insertion point)."""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


# ---------------------------------------------------------------------#
# Core data structure
# ---------------------------------------------------------------------#
class SparseTable:
    """Cyclic, uniformly-gapped ordered array with amortised O(log m) updates."""

    def __init__(self, n_seq, m_seq, k, first_key):
        self.n_seq = n_seq                # n_k values
        self.m_seq = m_seq                # m_k values
        self.k = k                        # current level (1-based)
        self.m = int(round(n_seq[k - 1] * m_seq[k]))
        self._data = [first_key] * self.m
        self.n = 1                        # authentic keys
        self.head = 0                     # logical index 0

    # index helpers ---------------------------------------------------
    def _pidx(self, logical):
        """Logical → physical index."""
        return (self.head + logical) % self.m

    def _logical(self):
        """Array in logical order."""
        return [self._data[self._pidx(i)] for i in range(self.m)]

    def _auth(self, logical):
        """True iff logical slot holds an authentic key."""
        prev = (logical - 1) % self.m
        v = self._logical()
        return v[logical] != v[prev]

    def lookup(self, key):
        arr = self._logical()
        pos = bisect_left(arr, key) % self.m
        found = pos < self.m and arr[pos] == key and self._auth(pos)
        return found, pos

    def insert(self, key):
        if self.lookup(key)[0]:
            return
        if self.n == self.n_seq[self.k]:
            self._rebuild(self.k + 1)

        arr = self._logical()
        s = bisect_left(arr, key) % self.m

        if arr[s] == arr[(s - 1) % self.m]:          # dummy slot
            self._data[self._pidx(s)] = key
            self.n += 1
            return

        # authentic slot – shift consecutive authentics right
        t = 0
        while not self._auth((s + t + 1) % self.m):
            t += 1
        for off in range(t, -1, -1):
            src = self._pidx(s + off)
            dst = self._pidx(s + off + 1)
            self._data[dst] = self._data[src]

        self._data[self._pidx(s)] = key
        if s == 0:
            self.head = (self.head - 1) % self.m
        self.n += 1

    def delete(self, key):
        found, s = self.lookup(key)
        if not found:
            return

        arr = self._logical()
        L = 1
        while arr[(s + L) % self.m] == key:
            L += 1
        next_key = arr[(s + L) % self.m]

        for off in range(L):
            self._data[self._pidx(s + off)] = next_key
        self.n -= 1

        if self.k >= 2 and self.n == self.n_seq[self.k - 2]:
            self._rebuild(self.k - 1)

    def _rebuild(self, new_k):
        keys = [v for i, v in enumerate(self._logical()) if self._auth(i)]
        keys.sort()
        self.k = new_k
        self.m = int(round(self.n_seq[new_k - 1] * self.m_seq[new_k]))
        q, r = divmod(self.m, len(keys))

        self._data = [0] * self.m
        pos = 0
        for i, v in enumerate(keys):
            self._data[pos] = v
            gap = q + (1 if i < r else 0)
            for j in range(1, gap):
                self._data[pos + j] = v
            pos += gap

        self.head = 0
        self.n = len(keys)

    def __str__(self):
        a = self._logical()
        return "[" + ", ".join([f">{a[0]}<"] + [str(v) for v in a[1:]]) + "]"


# ---------------------------------------------------------------------#
# CLI glue
# ---------------------------------------------------------------------#
def load_spec(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def run_case(spec):
    table = SparseTable(spec["nn"], spec["mm"], spec["k"], spec["x"])
    print(table)
    for step in spec["actions"]:
        action, key = step["action"], step["key"]
        if action == "insert":
            table.insert(key)
        elif action == "delete":
            table.delete(key)
        elif action == "lookup":
            found, pos = table.lookup(key)
            msg = (
                f"Key {key} found at position {pos}."
                if found else
                f"Key {key} not found. It should be at position {pos}."
            )
            print(msg)
        else:
            raise ValueError(f"Unknown action {action}")
        print(table)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Sparse library-sorting table")
    ap.add_argument("json_file", help="test description file")
    run_case(load_spec(ap.parse_args(argv).json_file))


if __name__ == "__main__":
    main()
