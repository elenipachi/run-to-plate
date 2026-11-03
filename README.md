# Run-to-Plate

A training-aware nutrition planner for runners. Log runs (manually or via GPX upload)
and get daily calorie, macro and meal targets that keep your weight steady.

## Run locally

    python3 -m http.server 3000

Then open http://localhost:3000

## Deploy on Codesphere

The `ci.yml` serves `index.html` on port 3000. Create a workspace from this repo,
open the CI pipeline and start the Run stage.

Profile and runs are stored in the browser (localStorage) only.
