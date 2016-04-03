$4 == "provides" && $5 == "no" {
    # black hole.
    gsub("\'", "", $3);
    printf("/%s/s/style=rounded/style=\"rounded\",style=\"filled\"/\n", $3);
}

$4 == "requires" && $5 == "no" {
    # miracle.
    gsub("\'", "", $3);
    printf("/%s/s/style=rounded,/style=\"rounded\", style=\"filled\", fillcolor=\"cornflowerblue\", /\n", $3);
}

$4 == "has" && $5 == "no" {
    # empty.
    gsub("\'", "", $3);
    printf("/%s/s/style=rounded/style=\"rounded\", style=\"dotted\"/\n", $3);
}


$7 == "unprovided" {
    # input?
    gsub("\'", "", $5);
    printf("/\\\"r:.*%s.*\\\"/s/fontcolor=\"BLACK\"/fontcolor=\"green\"/\n", $2);
}

$7 == "not" && $8 == "consumed" {
    # output?
    gsub("\'", "", $5);
    printf("/\\\"p:.*%s.*\"/s/labelfontcolor=\"black\"/labelfontcolor=\"red\"/\n", $2);
}

$4 == "provides" && $5 == "but" && $6 == "does" && $7 == "not" && $8 == "require" {
    # transform
    gsub("\'", "", $3);
    printf("/%s/s/style=rounded/style=rounded, fontcolor=\"blue\"/\n", $3);
}



END {
    printf("/shape=plaintext/ {\n");
    printf("}\n");
}
