<!-- Generated from README.template.md by scripts/update_readme.py. Edit the template, not this file. -->
<div align="center">

# Vaidik Garg

Student developer · Java server work &amp; full-stack web

</div>

I'm a student who builds full-stack web projects and sends fixes to open source projects. **{{ MERGED_COUNT }}** so far, in Apache HugeGraph and Apache Fineract.

On [Apache HugeGraph](https://github.com/apache/hugegraph) I work on the Store module's query iterators: hashing `BackendColumn` by its bytes so union and intersection match identical rows, keeping limit-dedup keys intact through id-only projections, holding on to pending rows in the dedup iterators across query batches, and closing `MultiListIterator`'s sub-iterators when a query is cancelled early or a close fails. I reported most of these bugs as issues before fixing them.

On the [Apache Fineract back-office UI](https://github.com/apache/fineract-backoffice-ui) (Angular) I build and fix admin screens: editing scheduler jobs, configuring the SMS gateway, approving share dividends, and getting dates right in client records and the birth-date picker.

Outside upstream work I'm building [Study Vault](https://github.com/vaidikgarg-bit/study-vault), a course notes hub with generated quizzes and flashcards, on FastAPI and SQLite with a Tailwind front end.

## Upstream work

{{ UPSTREAM_TABLE }}

## Open PRs

Open pull requests in upstream projects (refreshed automatically).

{{ OPEN_PRS }}

## Stats

<p align="center">
  <img src="assets/stats.svg" alt="Upstream contribution stats"/>
  <img src="assets/languages.svg" alt="Languages in my pull requests"/>
</p>

## Tools

Java · Python · TypeScript · JavaScript · Angular · FastAPI · SQLite · RocksDB · Tailwind CSS · HTML/CSS · GitHub Actions · Git

---

<sub>Auto-updated {{ UPDATED }} · [workflow](.github/workflows/update-readme.yml)</sub>
