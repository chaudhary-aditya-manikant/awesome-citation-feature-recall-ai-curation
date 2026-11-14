# Study 2 deviation D1: source of the citation counts (14 November 2026)

Recorded before any Study 2 model was fitted or any result was computed.

**Pre-registered:** citation counts fetched live from OpenAlex on the snapshot date (13 November 2026).

**What happened:** on 13 November 2026 the live download was attempted twice in Colab. Both times OpenAlex stopped answering after 90,100 of 166,085 records (HTTP 429, "Too Many Requests") and kept refusing for more than 40 minutes of retries. No citation counts were analysed; the partial download was discarded when the Colab session ended.

**Deviation:** the citation count and publication year stored for each record in the SYNERGY release itself are used instead (`--citations package`). These were collected from OpenAlex by the SYNERGY authors when the dataset was built. The age adjustment therefore uses the latest publication year in the data as its reference year, not 2026; the value is written to `data/study2/synergy_manifest.json` and to the run summary.

**Why this is acceptable:** the choice was forced by the API limit and made before any result existed. It also partly reduces the threat named in the pre-registration: counts taken when SYNERGY was built are closer in time to the reviews than counts taken in 2026.

Nothing else in the protocol changes: same reviews, model, folds, seeds, K, gate (50/50), thresholds and success rule.
