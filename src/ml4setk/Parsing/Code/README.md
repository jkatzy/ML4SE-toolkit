# Code Parsing

`TreeSitterQuery` exposes Tree-sitter captures through the same
`QueryMatch(prefix, suffix, match)` contract used elsewhere in the toolkit.

## Notes

- This module is optional and requires the `treesitter` extra.
- Rules are supplied in Tree-sitter query syntax, for example
  `(comment) @comment` for Python comments.
- Dependency failures are deferred until `TreeSitterQuery` is instantiated so
  importing the package stays lightweight.
