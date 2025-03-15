#!/bin/bash

if ! test -f ./adv.png; then
    echo "Failed: adv.png does not exist"
    exit
fi

res=`python3 face-dist.py --image ./adv.png --compare-embedding "$(cat ./test/woz.embedding)"`

if (( $(echo "0.75 > $res" |bc -l) )); then
    echo "Passed"
else
    echo "Failed: adversarial face does not classify as Wozniak: $res"
fi

