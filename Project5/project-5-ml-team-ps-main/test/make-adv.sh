#!/bin/bash

python3 face-adv.py --image ./test/biden.png --goal ./test/prime.png --out ./test/biden-as-prime.png --threshold 0.75 > /dev/null 2>&1

if ! test -f ./test/biden-as-prime.png; then
    echo "Failed: did not create output image"
    exit
fi

res=`python3 face-dist.py --image ./test/biden-as-prime.png --compare-embedding "$(cat ./test/prime.emb)"`

if (( $(echo "0.75 > $res" |bc -l) )); then
    echo "Passed"
else
    echo "Failed: Did not make adversarial face: $res"
fi

