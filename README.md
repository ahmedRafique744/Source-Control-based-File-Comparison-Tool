# Source Control Diff Engine

A file comparison tool built in Python that implements the **edit distance** algorithm from scratch. This project explores dynamic programming to find the minimum-cost sequence of edits (insertions, deletions, and replacements) required to transform one file into another.

The tool generates a human-readable diff log detailing the precise operations needed to change File A into File B, inspired by the functionality of `git diff`.

---

## About This Project

This project began as an exploration of edit distance, starting with a basic recursive implementation and evolving into a highly efficient, bottom-up dynamic programming solution.

The central feature is a **two-stage diff algorithm** optimized for comparing source code and text files:

1.  **Phase 1: Line-Level Comparison**
    The tool first runs the edit distance algorithm on the files line-by-line. This quickly identifies which lines are identical, added, deleted, or *changed*.

2.  **Phase 2: Character-Level Refinement**
    For any lines identified as *changed*, the tool performs a second pass of the edit distance algorithm *only* on that specific pair of lines.

This two-stage approach is dramatically more efficient than a naive character-by-character comparison, as it focuses computational effort only on the parts of the file that have
