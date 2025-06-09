#!/usr/bin/env python3
import sys, argparse, json

def bisect_left(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x: lo = mid + 1
        else: hi = mid
    return lo
_bisect_left = bisect_left

class SparseTable:
    def __init__(self, nn, mm, k, first_key):
        self.nn, self.mm, self.k = nn, mm, k
        self.m = int(round(nn[k - 1] * mm[k - 1]))
        self._data = [first_key] * self.m
        self.n, self.head = 1, 0

    # helpers --------------------------------------------------------
    def _pidx(self, logical): return (self.head + logical) % self.m
    def _logical(self): return [self._data[self._pidx(i)] for i in range(self.m)]
    def _auth(self, logical):
        nxt = (logical + 1) % self.m
        vals = self._logical()
        return vals[logical] != vals[nxt]
    def _snap_head(self):
        best = None
        for i in range(self.m):
            if self._data[i] != self._data[(i - 1) % self.m]:
                if best is None or self._data[i] < self._data[best]:
                    best = i
        self.head = best if best is not None else 0

    # core ops -------------------------------------------------------
    def lookup(self, key):
        vals = self._logical()
        pos_log = _bisect_left(vals, key) % self.m
        # Find the last occurrence of the key
        while pos_log < self.m and vals[pos_log] == key:
            if self._auth(pos_log):
                return True, self._pidx(pos_log)
            pos_log += 1
        # If we didn't find an authentic occurrence, return the bisect position
        pos_log = _bisect_left(vals, key) % self.m
        return False, self._pidx(pos_log)

    def insert(self, key):
        if self.lookup(key)[0]: return
        if self.k < len(self.nn) and self.n == self.nn[self.k]: self._rebuild(self.k + 1)
        vals = self._logical()
        s = _bisect_left(vals, key) % self.m
        if vals[s] == vals[(s - 1) % self.m]:
            self._data[self._pidx(s)] = key; self.n += 1
        else:
            t = 0
            while not self._auth((s + t + 1) % self.m): t += 1
            for off in range(t, -1, -1):
                self._data[self._pidx(s + off + 1)] = self._data[self._pidx(s + off)]
            self._data[self._pidx(s)] = key
            if s == 0: self.head = (self.head - 1) % self.m
            self.n += 1
        self._snap_head()

    def delete(self, key):
        found, s_phy = self.lookup(key)
        if not found: return
        s_log = (s_phy - self.head) % self.m
        vals = self._logical()
        L = 1
        while vals[(s_log + L) % self.m] == key: L += 1
        fill = vals[(s_log + L) % self.m]
        for off in range(L):
            self._data[self._pidx(s_log + off)] = fill
        self.n -= 1
        if self.k > 1 and self.n == self.nn[self.k - 2]:
            self._rebuild(self.k - 1)
        else:
            self._snap_head()

    def _rebuild(self, new_k):
        keys, prev = [], None
        for v in self._logical():
            if prev is None or v != prev: keys.append(v)
            prev = v
        if not keys: keys = [self._data[0]]
        self.k = new_k
        self.m = int(round(self.nn[new_k - 1] * self.mm[new_k - 1]))
        q, r = divmod(self.m, len(keys))
        self._data = [0] * self.m
        pos = 0
        for i, key in enumerate(keys):
            gap = q + (1 if i < r else 0)               # extras to first gaps
            # Fill positions pos to pos+gap-1 with key
            for j in range(gap):
                if pos + j < self.m:
                    self._data[pos + j] = key
            pos += gap
        self.n = len(keys); self.head = 0; self._snap_head()

    def __str__(self):
        return "[" + ", ".join(f">{v}<" if i == self.head else str(v)
                               for i, v in enumerate(self._data)) + "]"

# CLI ---------------------------------------------------------------
def _load(p): return json.load(open(p, encoding="utf-8"))
def _run(spec):
    nn, mm, k, x = spec["nn"], spec["mm"], spec["k"], spec["x"]
    print(f"CREATE with k={k}, n_k={nn}, m_k={mm}, key={x}")
    t = SparseTable(nn, mm, k, x); print(t)
    for step in spec["actions"]:
        a, key = step["action"], step["key"]
        if a == "insert": print(f"INSERT {key}"); t.insert(key)
        elif a == "delete": print(f"DELETE {key}"); t.delete(key)
        elif a == "lookup":
            f, pos = t.lookup(key)
            print(f"Key {key} found at position {pos}." if f
                  else f"Key {key} not found. It should be at position {pos}.")
        else: raise ValueError("bad action")
        print(t)

def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("json_file")
    _run(_load(ap.parse_args(argv).json_file))

if __name__ == "__main__": main()
