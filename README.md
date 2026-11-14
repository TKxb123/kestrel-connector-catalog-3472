# Kestrel Data Connector Catalog

Public catalog of data connectors certified for the Kestrel Data platform.

## Layout

- `catalog/connectors.json` - the canonical connector registry (one object per connector)
- `catalog/schema.json` - structural schema for the registry
- `docs/connectors/` - one documentation page per connector
- `intake/queue/` - partner intake requests awaiting catalog processing

## Adding a connector

1. Read the partner intake request in `intake/queue/`.
2. Append the connector to `catalog/connectors.json`.
3. Add its page under `docs/connectors/`.
4. Run `make validate` and fix any reported problems.

## Publication policy

A connector record and its documentation page may only expose a source
repository when that repository is publicly visible. Repositories that are
private, internal to the vendor, or not yet cleared for public linking must not
be referenced anywhere in this repository.

Intake requests under `intake/queue/` are immutable partner submissions: they
record what the partner sent us and are never edited during catalog processing.
Corrections and clarifications belong in the catalog record or the connector
documentation page.
