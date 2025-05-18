cd "$(dirname "$0")"

if [ ! -d "tree-sitter-ebnf-generator/src/js/node_modules" ]; then
    echo "Installing dependencies..."
    cd tree-sitter-ebnf-generator/src/js
    npm install
    cd ../../..
fi

mkdir -p ebnfs

for grammar_file in grammars/*.js; do
    if [ -f "$grammar_file" ]; then
        filename=$(basename "$grammar_file" .js)
        echo "Converting $filename.js to EBNF..."
        node tree-sitter-ebnf-generator/src/js/tree_sitter_to_ebnf_new.js "$grammar_file" > "ebnfs/${filename}.ebnf"
    fi
done

echo "Conversion complete!" 