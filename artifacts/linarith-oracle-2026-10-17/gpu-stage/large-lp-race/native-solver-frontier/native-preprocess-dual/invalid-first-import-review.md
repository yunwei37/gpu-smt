# First ablation import-selection fault, preserved

The first artifact wrapper changed only the first BatchOracle literal, which
sets a global default. Runner.cell still overwrote it with the AST BatchOracle
import. Its complete64source/29.13s cell is therefore an AST run, not the
planned native-preprocessing ablation. Source selection was inspected before
accepting the result. No native-frontend or contribution conclusion is valid.
Raw cells and first entrypoint/receipt remain under invalid-first-import-selection.
No other session/capture was interrupted. The corrected patch targets the
single per-method .get(name,...) import fallback and asserts that exact match.
