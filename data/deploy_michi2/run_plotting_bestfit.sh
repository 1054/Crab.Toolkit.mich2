#!/bin/bash
#
sm << EOF
macro read pChisq.sm plotChisq \
"flux_obsframe.dat" \
"FSPS.Padova.BaSeL.Z0.0190.EBV.lib.SED" \
"DL07.HiExCom.SPAH.lib.SED" "DL07.LoExCom.SPAH.lib.SED" \
"fit.out"
quit
EOF

