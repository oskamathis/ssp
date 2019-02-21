#!/usr/local/bin/fish

vegeta attack -rate=600 -duration=60s -targets=vegeta/vegeta.txt
| tee vegeta/result.bin

cat vegeta/result.bin | vegeta plot > vegeta/result.html
