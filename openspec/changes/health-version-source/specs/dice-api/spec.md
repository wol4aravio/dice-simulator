## Purpose

Capability описывает HTTP API симулятора дайсов, включая endpoint готовности сервиса и контракт версии, которую используют клиенты и операционные проверки.

## ADDED Requirements

### Requirement: Health version matches backend package metadata
The service SHALL expose `GET /health` with a `version` field equal to the backend service version declared in the backend package metadata, and the value SHALL be a semver string.

#### Scenario: Health reports package version
- **WHEN** a client requests `GET /health`
- **THEN** the response status is 200 and the body contains `status` equal to `"ok"` and `version` equal to the backend package version

#### Scenario: Health version remains semver
- **WHEN** a client requests `GET /health`
- **THEN** the `version` value in the response is a semver string
