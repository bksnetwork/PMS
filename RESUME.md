# PMS Resume — 2026-09-27 01:42 ET

## Exact restart point
Paused immediately after the **Trapinch family** audit/transfer. Resume with **Swablu**.

Current game checkpoint:
- Pokémon storage: **1,088 / 1,325** (237 free)
- Stardust: **594,642**
- Confirmed transfers tracked in this cleanup: **228**
- Completed duplicate-family audits tracked: **17**
- Trapinch Candy: **94**, XL: **1**
- Existing Vibrava CP735 needs 100 candy for Flygon, so do not evolve yet.

## Collector-first rules
1. Maintain a living collection: at least one actual copy of each owned species/stage.
2. Keep enough base-stage reserves to fill missing evolutions without losing the base form.
3. Preserve meaningful forms/variants, shiny, costume, Shadow/Purified, Lucky, @special/legacy, old/rare, research-reserved, useful PvE and useful PvP Pokémon.
4. Gender duplicates are only automatically required when visually/Pokédex/evolution-path distinct; otherwise gender can still be retained when useful/desired.
5. Never transfer merely because the Pokédex is registered, IVs are low, or !evolvenew matches.
6. Transfer only confirmed surplus after family audit.
7. For each family, check 3*/4*, shiny/shadow/costume/@special, and PvP-IV search before selecting surplus.
8. Search strings shown to the user should always be in a copy-friendly code block.

## Families completed in this session
See `public/data.json -> cleanup.families` for counts and keeper notes. Completed:
Drifloon, Bulbasaur, Gastly, Shroomish, Taillow, Surskit, Wingull, Aron, Meditite, Electrike, Plusle, Minun, Gulpin, Wailmer, Numel, Spoink, Trapinch.

Latest:
- Spoink: 6 transferred; kept CP444 protected/future Grumpig, CP163 PvP-IV candidate, CP18 protected living copy.
- Trapinch: 9 transferred; kept CP716, CP525 future evolution reserve, Vibrava CP735. Flygon missing.

## Remaining event/duplicate families supplied by user
**11 remaining:**
1. Swablu
2. Barboach
3. Corphish
4. Anorith
5. Feebas
6. Castform
7. Shuppet
8. Spheal
9. Cherubi
10. Darumaka
11. Phantump

After those, reassess storage and run a new largest-family/duplicate scan rather than blindly continuing.

## Known research/evolution reservations
- Dratini: Jump-Start evolution; preserve base + later-stage needs.
- Feebas: A Thousand-Year Slumber; do not transfer/evolve blindly.
- Magikarp: A Mythical Discovery; 400-candy evolution requirement.
- Eevee: A Ripple in Time requires buddy walking + Espeon during day; confirm silhouette before evolving.
- Grimer: Let's GO, Meltan requires evolution; user currently has no Grimer.
- Finding Your Voice: evolve 15; stack planned living-Dex evolutions.
- Power-up tasks should be stacked across active research rather than spending Stardust independently.
- Numel CP669 and Surskit CP556 are tagged/reserved for the evolution run.

## Data/workbook direction
PMS is the long-term source of truth. Track per Pokémon when verified:
Dex number, species, form, gender, CP, HP, appraisal/IV evidence, types, weight, height, catch date/location, moves, power-up cost, evolution cost/requirements, second charged move cost, shiny/Shadow/Purified/costume/Lucky/special status, tags, collector purpose, PvE/PvP role, research reservation, and action decision.

Never invent missing fields. Resource totals are family/account snapshots, not intrinsic Pokémon attributes.

## Website/data work
The website should consume `public/data.json` as the current data source. The data file was synced through the Trapinch checkpoint. Continue improving:
- dashboard should show live storage checkpoint and transfer total;
- Families/Cleanup pages should render every audited family and remaining queue;
- My Pokémon should render all verified detailed records, not only the first Drifloon records;
- Research page should render the known reservations/stacking plan from data;
- add a Resume/Next Action area so a future chat can immediately see the restart point;
- remove stale hard-coded fallback data from app.js or keep it synchronized automatically;
- header storage pill must not remain hard-coded/stale;
- event/calendar data must be verified before publishing rather than retaining stale event assumptions.

## Data integrity note
The cleanup transfer total is reconstructed from confirmed family transfer counts. If a later audit finds an earlier family count was only selected rather than actually transferred, correct both the family record and aggregate immediately. Storage screenshots are the stronger checkpoint.

## Restart instruction for next ChatGPT session
Read this file and `public/data.json` first. Do not repeat completed searches. Start with Swablu and continue the same conservative family-audit workflow. Keep copy buttons/copy-friendly search blocks in every search instruction.
