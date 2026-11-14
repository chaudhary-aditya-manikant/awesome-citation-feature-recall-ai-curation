# Study 2 note: which SYNERGY collection (13 November 2026)

Recorded before any Study 2 model was fitted or any result was computed.

The pre-registration names the SYNERGY benchmark (26 systematic reviews, 169,288 records, 2,834 inclusions). On the first Colab run, the `synergy-dataset` package downloaded its new default collection, **SYNERGY+ version 3.0**, a different and larger set in which many records have no OpenAlex id. The first reviews read from it returned no usable records, and the fetch was stopped. No labels, citations or results were inspected.

To match the pre-registration, the fetch script sets `SYNERGY_SET=synergy` (the original SYNERGY collection, as documented by the package). The collection and version actually used are written to `data/study2/synergy_manifest.json`. Nothing else in the protocol changes.
