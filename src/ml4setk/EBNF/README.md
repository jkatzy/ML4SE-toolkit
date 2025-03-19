# How to use that?
1. **Examples:** Inside of the examples folder, there are example EBNF files for different languages. You can also generate it by yourself.
2. **tree-sitter-ebnf:** Needed to be fixed, there's still some bugs to it.
3. **ebnf.ipynb:** Here is the example of how to use the converter and visualizationer. You can follow the steps and change the code inside to make it visualized.

# How to run tree-sitter-ebnf-converter?
Please go to the `EBNF/tree-sitter-ebnf-generator` folder. In src/js, run 
```
npm install
```
and then you can found a `node_modules` folder. 
After that, still in the same `EBNF/tree-sitter-ebnf-generator` folder, run the following command:
```
node src/js/tree_sitter_to_ebnf_new.js examples/lua/grammar.js > examples/lua/yourname.ebnf
```
PS: You can change LUA to any language you want to generate the EBNF grammar. And you can choose the name by yourself.
If you want the ebnf grammar to show in CLI, please run:
```
node src/js/tree_sitter_to_ebnf_new.js examples/lua/grammar.js
```


