#!/bin/bash
# Download public reference data for validate.py into downloads/<date>/.
#   bash validation/fetch_sources.sh [first_season] [last_season]
# Sources: Baseball Savant (custom, batted-ball, pitch-arsenal leaderboards),
# MLB Stats API (official season hitting), FanGraphs via baseballr (EV90, wOBA).
set -euo pipefail

FIRST=${1:-2023}
LAST=${2:-2026}
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$HERE/downloads/$(date +%Y-%m-%d)"
mkdir -p "$OUT"

SEL="pa,ab,hit,double,triple,home_run,strikeout,walk,k_percent,bb_percent,batting_avg,slg_percent,on_base_percent,woba,xwoba,xba,xslg,exit_velocity_avg,launch_angle_avg,sweet_spot_percent,barrel_batted_rate,hard_hit_percent,z_swing_percent,oz_swing_percent,whiff_percent,groundballs_percent,flyballs_percent,linedrives_percent,popups_percent,pull_percent,opposite_percent,sprint_speed,pitch_count"

for y in $(seq "$FIRST" "$LAST"); do
  echo "season $y"
  curl -sf "https://baseballsavant.mlb.com/leaderboard/custom?year=$y&type=batter&filter=&min=q&selections=$SEL&chart=false&csv=true" \
    -o "$OUT/savant_custom_$y.csv"
  curl -sfL "https://baseballsavant.mlb.com/leaderboard/batted-ball?gameType=Regular&seasonStart=$y&seasonEnd=$y&type=batter&min=q&csv=true" \
    -o "$OUT/savant_battedball_$y.csv"
  curl -sf "https://baseballsavant.mlb.com/leaderboard/pitch-arsenal-stats?type=batter&pitchType=&year=$y&team=&min=1&csv=true" \
    -o "$OUT/savant_arsenal_$y.csv"
  curl -sf "https://statsapi.mlb.com/api/v1/stats?stats=season&group=hitting&season=$y&sportId=1&playerPool=ALL&limit=5000" \
    -o "$OUT/statsapi_hitting_$y.json"
  sleep 1
done

# FanGraphs blocks plain HTTP clients; baseballr (as in the pipeline) works.
Rscript -e "
suppressMessages(library(baseballr))
for (y in $FIRST:$LAST) {
  x <- fg_batter_leaders(startseason = y, endseason = y, qual = 'y')
  keep <- intersect(c('Season','xMLBAMID','PlayerName','PA','wOBA','EV','EV90','maxEV','HardHit_pct','Barrel_pct'), names(x))
  write.csv(x[, keep], file.path('$OUT', sprintf('fangraphs_%d.csv', y)), row.names = FALSE)
}"

ls -la "$OUT"
