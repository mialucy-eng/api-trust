# Contributing security/privacy transparency rankings

Pull requests are welcome from independent developers, providers, and researchers when the relationship is disclosed.

1. Copy `data/examples/example-ranking.json` into `data/submissions/<id>.json`; the filename must match `id`.
2. Replace every fictional value and review the same hosted-API scope and all ten controls for every provider.
3. Cite a direct, stable public HTTPS source for every `documented` control. Explain every `not_documented` and `not_applicable` result.
4. Disclose affiliation and all material conflicts.
5. Run `python3 rankings.py`, `python3 rankings.py --check`, and `python3 -m unittest discover -s tests -v`.
6. Commit the source JSON and generated `RANKINGS.md`, then open a pull request.

Do not include private security reports, vulnerability details without coordinated disclosure, customer data, credentials, cookies, account exports, or authenticated screenshots. Do not turn missing public documentation into an accusation of theft, fraud, breach, noncompliance, or malicious conduct. This repository ranks documented evidence coverage only.
