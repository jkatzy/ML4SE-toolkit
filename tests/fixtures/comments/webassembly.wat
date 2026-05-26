(; block comment ;)
;; multi line comment part 1
;; multi line comment part 2
(module
  ;; single line comment
  (func (export "add") (param i32 i32) (result i32)
    local.get 0
    local.get 1
    i32.add))
