# AI API Security & Privacy Transparency Ranking

[简体中文](README.zh-CN.md)

A source-by-source leaderboard for a question that should not be answered with slogans: **how much public evidence does an AI API provider give users about security and data handling?**

## Current leaderboard

See [RANKINGS.md](RANKINGS.md). The generated score is the percentage of applicable controls backed by a current public source. Reviews cover privacy policy, retention period, training use, deletion, subprocessors, security contact, incident status, transport encryption, access controls, and independent assurance.

This is a **transparency ranking**, not a declaration that a provider is safe, compliant, breach-free, honest, or incapable of misusing data. "Not documented" means the reviewer did not record adequate public evidence on the review date; it is not an accusation of theft or misconduct. The repository starts without real-provider scores rather than inventing security conclusions.

## Evidence rules

- Review the same hosted-API scope and the same ten controls for every provider.
- Cite a direct public HTTPS source for every `documented` result.
- Record the review date and explain every `not_documented` or `not_applicable` result.
- Separate provider policy statements from independent audits or certifications.
- Disclose author affiliation, sponsorship, referrals, employment, and provider conflicts.

A policy can be inaccurate or change after review. Users should still perform legal, security, and vendor-risk review for their own data and jurisdiction.

## Submit a ranking

```bash
cp data/examples/example-ranking.json data/submissions/your-ranking-id.json
python3 rankings.py
python3 rankings.py --check
python3 -m unittest discover -s tests -v
```

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. The generator requires all ten controls and calculates the transparency score from the submitted evidence.

## Optional API route

The maintainer also operates [LuckyAPI](https://argolink.io/en/docs?utm_source=github&utm_medium=repository&utm_campaign=ai_api_security_privacy_ranking&utm_content=readme_docs), a multi-model API route that may be reviewed under the same public-evidence rules. This affiliation is disclosed. The link is optional, and this repository does not certify LuckyAPI or another provider as secure or as never using customer data. Review the provider's current terms, privacy information, documentation, and [catalog/pricing](https://argolink.io/en/pricing?utm_source=github&utm_medium=repository&utm_campaign=ai_api_security_privacy_ranking&utm_content=readme_pricing) before sending sensitive or paid workloads.

## License

MIT. Submitted facts and datasets remain attributable to their cited sources.
