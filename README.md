# ClipSync — Cross-Device Clipboard Synchronization

**ClipSync** is a Python-based clipboard synchronization project designed to transfer text between connected devices over a network. The goal is to make copying text on one device and accessing it on another simple, fast, and reliable.

The project follows a modular client-server architecture, separating network communication, message validation, clipboard operations, and database persistence into independent components.

> **Project status:** In development. The initial focus is a Python client-server implementation with structured messages and persistent connection and message metadata. Mobile integration, QR-based pairing, and other advanced features are planned extensions rather than assumed completed features.

---

## Table of Contents

- [1. Project Overview](#1-project-overview)
- [2. Problem Statement](#2-problem-statement)
- [3. Project Objectives](#3-project-objectives)
- [4. Key Features](#4-key-features)
- [5. Technologies and Tools](#5-technologies-and-tools)
- [6. Core Concepts and Terminology](#6-core-concepts-and-terminology)
- [7. System Architecture](#7-system-architecture)
- [8. Project Directory Structure](#8-project-directory-structure)
- [9. Client and Server Responsibilities](#9-client-and-server-responsibilities)
- [10. Communication Protocol](#10-communication-protocol)
- [11. Message Format](#11-message-format)
- [12. Database Design](#12-database-design)
- [13. Data Flow](#13-data-flow)
- [14. Installation and Setup](#14-installation-and-setup)
- [15. Running the Project](#15-running-the-project)
- [16. Configuration](#16-configuration)
- [17. Security Considerations](#17-security-considerations)
- [18. Error Handling and Reliability](#18-error-handling-and-reliability)
- [19. Testing Strategy](#19-testing-strategy)
- [20. Development Roadmap](#20-development-roadmap)
- [21. Learning Outcomes](#21-learning-outcomes)
- [22. Contributing](#22-contributing)
- [23. License](#23-license)

---

## 1. Project Overview

ClipSync is a lightweight clipboard synchronization system intended to connect devices and exchange clipboard text without depending on cloud clipboard services or third-party messaging applications.

The initial version focuses on a Python-based client-server system. The server manages incoming connections and coordinates communication, while clients read clipboard content, send messages, receive incoming content, and update their local clipboards.

The system uses TCP sockets for network communication, JSON for message representation, Pydantic for message validation, and SQLite for persistent metadata storage.

### Design principles

- **Modularity:** Keep networking, database operations, validation, and clipboard logic separate.
- **Simplicity:** Start with text-only clipboard synchronization.
- **Reliability:** Handle message boundaries, disconnections, and malformed messages explicitly.
- **Maintainability:** Use clear interfaces between modules.
- **Extensibility:** Keep the architecture ready for future mobile clients, pairing, and secure communication.

## 2. Problem Statement

Copying text between a laptop and a phone often requires sending a message to yourself, opening a cloud service, or manually transferring the text.

ClipSync aims to simplify this workflow by providing a dedicated communication mechanism between paired devices.

The project explores how a practical application can combine:

1. Network programming and TCP communication.
2. Structured message serialization and validation.
3. Clipboard integration.
4. Relational database design.
5. Connection and message lifecycle tracking.
6. Modular software architecture.

## 3. Project Objectives

The primary objectives are:

- Establish communication between a client and a server using TCP sockets.
- Transfer variable-length text messages reliably.
- Define a structured message format with identifiers, timestamps, message types, and sender information.
- Validate incoming messages before processing them.
- Store device, connection, and message metadata in SQLite.
- Separate database configuration from data-access logic.
- Handle invalid input, socket failures, and client disconnections.
- Build a foundation for bidirectional synchronization between devices.

## 4. Key Features

|          Feature          |           Scope              |
|---------------------------|------------------------------|
| TCP client-server communication | Initial implementation |
| Structured JSON messages | Initial implementation |
| Pydantic message validation | Initial implementation |
| SQLite metadata persistence | Initial implementation |
| SQLAlchemy database access | Initial implementation |
| Device and connection tracking | Planned for database integration |
| Message history and delivery status | Planned for database integration |
| Bidirectional clipboard synchronization | Core application goal |
| Automatic reconnection | Future enhancement |
| QR-based device pairing | Future enhancement |
| Android client using Kotlin | Future enhancement |
| Encrypted network communication | Security enhancement |

Feature status should be updated as the implementation evolves. A feature appearing in this document does not, by itself, mean that it is already implemented.

## 5. Technologies and Tools

### 5.1 Python

Python is the primary language for the initial client-server implementation.

It is used to coordinate networking, validate messages, interact with the clipboard, and communicate with the database.

### 5.2 `socket` — TCP networking

Python's built-in `socket` module provides low-level network communication.

ClipSync uses TCP sockets to establish connections and exchange bytes between the client and server.

Important operations include:

- `socket()` — creates a socket.
- `bind()` — associates a server socket with a local address and port.
- `listen()` — enables a socket to accept incoming connections.
- `accept()` — accepts an incoming connection.
- `connect()` — connects a client to a server.
- `sendall()` — sends all supplied bytes unless an error occurs.
- `recv()` — receives available bytes from a connection.
- `close()` — closes a socket.

**Important:** TCP provides an ordered byte stream, not individual application messages. ClipSync therefore needs a framing protocol to identify where one message ends and the next begins.

### 5.3 SQLite

SQLite is a relational database engine that stores data in a local database file.

It is appropriate for an early ClipSync implementation because it does not require a separate database server.

The database can store:

- Device records.
- Connection history.
- Message metadata.
- Message delivery states.
- Event timestamps.

SQLite is separate from the network protocol: sending a message does not automatically persist it. The application must explicitly save the relevant metadata.

### 5.4 SQLAlchemy 2.0

SQLAlchemy is a Python SQL toolkit and Object Relational Mapper (ORM).

The ORM allows application code to work with Python model objects instead of manually writing SQL for every operation.

For example, a `Device` Python object can represent a row in the `devices` table.

Core responsibilities include:

- Defining database models.
- Configuring the database engine.
- Managing sessions and transactions.
- Inserting and querying records.
- Updating message and connection statuses.

SQLAlchemy does not replace SQLite. SQLite stores the data; SQLAlchemy provides the Python interface for interacting with it.

### 5.5 Pydantic 2

Pydantic validates Python data against declared schemas and converts supported input into typed Python objects.

ClipSync can use Pydantic to validate message fields such as:

- Message identifier.
- Message type.
- Protocol version.
- Sender device identifier.
- Message content.
- Creation timestamp.

Validation helps reject malformed or incomplete messages before the application processes them.

Pydantic validates data structure and types; it does not authenticate a device or encrypt a message.

### 5.6 JSON

JavaScript Object Notation (JSON) is a text-based data interchange format.

It represents structured data using objects, arrays, strings, numbers, booleans, and null values.

ClipSync uses JSON to represent application messages. JSON text is encoded as UTF-8 bytes before transmission through a TCP socket.

### 5.7 UUID

A Universally Unique Identifier (UUID) is a 128-bit identifier commonly used to distinguish records and messages.

ClipSync can use UUIDs to identify:

- Devices.
- Connections.
- Messages.

For example, a message ID lets the application refer to a particular message independently of its content or database row position.

A UUID is an identifier, not a secret, authentication credential, or encryption key.

### 5.8 UTC timestamps

Coordinated Universal Time (UTC) provides a consistent time reference across devices and locations.

Storing timestamps in UTC avoids ambiguity caused by local time zones and daylight-saving changes.

ClipSync can record timestamps such as:

- `created_at`: when a message was created.
- `received_at`: when a message was received.
- `connected_at`: when a connection started.
- `disconnected_at`: when a connection ended.

An ISO 8601 representation such as `2026-10-15T17:00:00Z` indicates a UTC timestamp.

### 5.9 Length-prefixed message framing

Length-prefixed framing is a protocol technique in which each message is preceded by a field describing the message's byte length.

TCP does not preserve application-level message boundaries. A single `recv()` call may return only part of a message or bytes from multiple messages.

A length prefix allows the receiver to determine how many bytes belong to the current message.

ClipSync's protocol can use a fixed-width length header followed by the JSON payload. Both client and server must agree on the header size, byte order, and encoding.

### 5.10 Clipboard integration

The clipboard interface reads and writes text in the operating system's clipboard.

On a Python desktop client, a library such as `pyperclip` can provide cross-platform clipboard access where supported.

Clipboard integration must be implemented separately from socket communication. Network code should transmit text; clipboard code should interact with the operating system.

### 5.11 Logging

Python's built-in `logging` module records diagnostic information about application behavior.

Useful log events include:

- Server startup.
- Client connection and disconnection.
- Invalid message validation.
- Database failures.
- Network timeouts.
- Message processing errors.

Logs should not expose clipboard contents, authentication secrets, or other sensitive information.

### 5.12 Future technologies

The following technologies may be introduced as the project expands:

| Technology | Purpose |
|---|---|
| `asyncio` | Asynchronous network operations |
| `qrcode` | Generating pairing QR codes |
| `cryptography` | Cryptographic operations for secure communication |
| `zeroconf` | Discovering devices on a local network |
| Kotlin | Native Android client development |
| Android `ClipboardManager` | Reading and writing Android clipboard content |
| WebSocket | Alternative application-level communication protocol |
| Docker | Packaging and isolating development services |

These are possible extensions, not dependencies required by the initial TCP implementation.

## 6. Core Concepts and Terminology

### Client-server architecture

A client initiates a connection and requests or exchanges data. A server listens for incoming connections and coordinates communication.

In ClipSync, the client is responsible for its local clipboard and the server provides the communication endpoint.

The architecture can later be extended to support multiple clients.

### TCP connection

Transmission Control Protocol (TCP) provides a reliable, ordered byte stream between two network endpoints.

TCP handles packet retransmission and ordering, but it does not define ClipSync's message structure, application-level delivery confirmation, or device authentication.

### Socket

A socket is a programming interface to a network communication endpoint.

A TCP connection is identified by the endpoints involved, including their IP addresses and port numbers. In Python, the socket object provides methods for establishing and using that connection.

### IP address and port

An IP address identifies a network interface or host within an IP network. A port identifies an application endpoint on a host.

The initial client-server implementation may require the client to know the server's reachable address and listening port. Automatic discovery and QR-based pairing can reduce this manual setup later.

### Serialization and deserialization

**Serialization** converts structured application data into a representation suitable for storage or transmission.

**Deserialization** converts the representation back into application data.

In ClipSync:

1. A Python message object is serialized into JSON.
2. The JSON is encoded into UTF-8 bytes.
3. The bytes are framed and sent over TCP.
4. The receiver extracts the payload, decodes UTF-8, parses JSON, and validates the resulting data.

### Protocol

A protocol defines the rules that communicating systems must follow.

ClipSync's application protocol defines message types, required fields, message framing, identifier formats, timestamps, and error behavior.

Both sides must follow the same rules to communicate correctly.

### Database engine, session, model, and repository

- **Engine:** Configures SQLAlchemy's connection interface to the database.
- **Session:** Manages a unit of database interaction, including changes and transactions.
- **Model:** Defines how application entities map to database tables.
- **Repository:** Encapsulates database queries and persistence operations.

Separating these responsibilities prevents networking code from becoming tightly coupled to SQL statements.

### Metadata

Metadata describes an object or event rather than necessarily containing its full content.

For example, a message record may contain its ID, sender, creation time, size, and delivery status.

A text field containing the actual clipboard contents is message content, not merely metadata. ClipSync should explicitly decide whether to persist that content.

### Delivery status

A delivery status describes how far a message has progressed through the application workflow.

Possible states include:

- `created`
- `sent`
- `received`
- `processed`
- `failed`

These states are application-defined. TCP successfully transmitting bytes does not prove that the receiving device updated its clipboard.

### Bidirectional synchronization

Bidirectional synchronization means that clipboard changes can propagate in either direction between connected devices.

A robust implementation must prevent synchronization loops. For example, text received from Device A and copied into Device B's clipboard must not be treated as an entirely new user copy and sent back to Device A indefinitely.

The implementation can use message IDs, content comparison, and origin tracking to reduce duplicate propagation.

## 7. System Architecture

The initial design separates the system into distinct layers.

```text
                 CLIPSYNC CLIENT
        +-------------------------------+
        | client/main.py                |
        | Application coordination      |
        +---------------+---------------+
                        |
             +----------+----------+
             |                     |
     +-------v-------+     +-------v-------+
     | Clipboard     |     | Protocol      |
     | Integration   |     | Serialization |
     +---------------+     +-------+-------+
                                    |
                            TCP Socket
                                    |
                                    v
                 CLIPSYNC SERVER
        +-------------------------------+
        | server/main.py                |
        | Listener and connection logic |
        +---------------+---------------+
                        |
                 +------v------+
                 | Protocol    |
                 | Validation  |
                 +------+------+
                        |
                 +------v------+
                 | Repository  |
                 +------+------+
                        |
                 +------v------+
                 | SQLAlchemy  |
                 | Engine      |
                 +------+------+
                        |
                 +------v------+
                 | SQLite      |
                 +-------------+
```

This diagram represents logical responsibilities. The exact call flow and module boundaries should match the actual implementation.

### Architectural layers

1. **Application layer:** Coordinates connection handling, clipboard operations, and message processing.
2. **Transport layer:** Sends and receives bytes over TCP.
3. **Protocol layer:** Defines framing, JSON serialization, and schema validation.
4. **Persistence layer:** Provides repositories and transaction handling.
5. **Database layer:** Stores persistent device, connection, and message records.

The separation allows each layer to evolve without rewriting the entire application.

## 8. Project Directory Structure

The following is a proposed structure for the modular Python implementation. Create only the files you need as development progresses.

```text
ClipSync/
├── client/
│   ├── __init__.py
│   ├── main.py
│   ├── connection.py
│   └── clipboard.py
│
├── server/
│   ├── __init__.py
│   ├── main.py
│   └── connection_handler.py
│
├── common/
│   ├── __init__.py
│   ├── schemas.py
│   ├── protocol.py
│   └── constants.py
│
├── database/
│   ├── __init__.py
│   ├── engine.py
│   ├── models.py
│   └── repository.py
│
├── tests/
│   ├── test_schemas.py
│   ├── test_protocol.py
│   ├── test_repository.py
│   └── test_connections.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### File responsibilities

| File | Responsibility |
|---|---|
| `client/main.py` | Coordinates the client application's lifecycle and message flow. |
| `client/connection.py` | Handles establishing and managing the client's network connection. |
| `client/clipboard.py` | Reads and updates the local clipboard. |
| `server/main.py` | Creates the listening socket and starts the server. |
| `server/connection_handler.py` | Handles communication with an accepted client. |
| `common/schemas.py` | Defines Pydantic message schemas. |
| `common/protocol.py` | Encodes, decodes, frames, and extracts application messages. |
| `common/constants.py` | Holds shared protocol constants and message-type definitions. |
| `database/engine.py` | Configures the SQLAlchemy engine and session factory. |
| `database/models.py` | Defines SQLAlchemy ORM models and relationships. |
| `database/repository.py` | Implements database queries and persistence operations. |
| `tests/` | Contains automated tests. |
| `requirements.txt` | Lists Python package dependencies. |
| `.env.example` | Documents optional environment configuration without real secrets. |

## 9. Client and Server Responsibilities

### Client

The client coordinates the local clipboard and the remote connection.

A typical workflow is:

1. Establish a TCP connection to the server.
2. Read local clipboard text when synchronization is triggered.
3. Construct a structured message.
4. Validate and serialize the message.
5. Send the framed bytes.
6. Receive messages from the server.
7. Decode and validate incoming messages.
8. Update the local clipboard when appropriate.

The client should avoid sending the same clipboard value repeatedly unless the protocol requires it.

### Server

The server provides the listening endpoint and handles client communication.

A typical workflow is:

1. Create a TCP socket.
2. Bind the socket to a configured address and port.
3. Start listening.
4. Accept client connections.
5. Receive complete framed messages.
6. Decode and validate messages.
7. Process messages and persist relevant metadata.
8. Send acknowledgements or responses where the protocol defines them.
9. Clean up resources when a client disconnects.

A listening socket and an accepted client socket have different roles. The listening socket accepts connections; the accepted socket carries data for a particular client connection.

## 10. Communication Protocol

### Message framing

TCP does not guarantee that a call to `recv()` returns one complete application message.

For example, suppose the client sends:

```text
Message A: 100 bytes
Message B: 150 bytes
```

The receiver might read 50 bytes first, then 100 bytes, then the remaining 100 bytes. Those reads do not necessarily align with the original messages.

ClipSync uses length-prefixed framing to solve this problem.

A conceptual wire format is:

```text
+----------------------+---------------------------+
| Payload length       | JSON payload              |
| Fixed-width header   | Variable-length bytes    |
+----------------------+---------------------------+
```

For example, with a four-byte unsigned big-endian length header:

```text
0000002A{"type":"clipboard","content":"Hello"}
```

The illustration is conceptual: `0000002A` represents a hexadecimal length of 42 bytes. A real implementation must encode the header as four binary bytes, and the length must equal the actual UTF-8 payload length.

The sender must:

1. Serialize the message to JSON.
2. Encode the JSON as UTF-8 bytes.
3. Calculate the payload's byte length.
4. Encode the length in the agreed header format.
5. Send the header and payload.

The receiver must:

1. Read exactly the required number of header bytes.
2. Decode the payload length.
3. Reject lengths outside the configured limit.
4. Read exactly that many payload bytes.
5. Decode and parse the JSON.
6. Validate the message schema.

A helper such as `recv_exact()` can repeatedly call `recv()` until the requested byte count is reached. If the connection closes before the count is reached, the message must be treated as incomplete.

## 11. Message Format

ClipSync uses structured JSON messages rather than sending arbitrary Python objects over the network.

### Example clipboard message

```json
{
  "protocol_version": 1,
  "message_id": "c72d9f83-2f63-4a7d-aeb2-8c6d6b79c9c1",
  "type": "clipboard",
  "sender_device_id": "4b50c5ac-4a84-42ab-9f36-829fd39d24a8",
  "created_at": "2026-10-15T17:00:00Z",
  "content_type": "text/plain",
  "content": "Text copied on another device"
}
```

This is an illustrative message contract. The actual Pydantic schema must define the accepted field names, types, required fields, and validation rules.

### Field descriptions

| Field | Meaning |
|---|---|
| `protocol_version` | Version of the application protocol. |
| `message_id` | Unique identifier for this message. |
| `type` | Identifies the operation, such as clipboard transfer or acknowledgement. |
| `sender_device_id` | Identifies the sending device. |
| `created_at` | UTC timestamp representing message creation. |
| `content_type` | Describes the payload format. |
| `content` | The clipboard text being transferred. |

### Pydantic schema

A simplified example using Pydantic 2:

```python
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ClipboardMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    protocol_version: int = Field(default=1, ge=1)
    message_id: UUID
    type: Literal["clipboard"]
    sender_device_id: UUID
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    content_type: Literal["text/plain"]
    content: str = Field(max_length=100_000)
```

The example provides basic type validation and a content-length constraint. The application should also enforce a maximum framed payload size, validate protocol compatibility, and apply its own device authorization rules.

A message schema should be designed around the application's actual protocol rather than assuming that every message contains clipboard content.

### Other message types

The protocol may later define distinct schemas for:

- `hello` — initial connection information.
- `clipboard` — text clipboard data.
- `ack` — application-level acknowledgement.
- `ping` and `pong` — connection health checks.
- `error` — a structured protocol or application error.

Each message type should have a documented purpose and clearly defined validation rules.

## 12. Database Design

ClipSync uses SQLite for local persistence and SQLAlchemy for database access.

The database is intended to record device identities, connection history, and message metadata. Clipboard text persistence should be a separate, explicit design decision.

### 12.1 `devices` table

Stores known device records.

| Column | Purpose |
|---|---|
| `id` | Primary key. |
| `device_uuid` | Unique device identifier. |
| `device_name` | Human-readable device name. |
| `device_fingerprint` | Optional identifier or fingerprint used by the device-trust design. |
| `created_at` | Time the device record was created. |
| `last_seen_at` | Most recent recorded activity. |

A fingerprint is not automatically proof of identity. Its security meaning depends on how it is generated, verified, and protected.

### 12.2 `connections` table

Stores connection sessions and their lifecycle.

| Column | Purpose |
|---|---|
| `id` | Primary key. |
| `connection_uuid` | Unique identifier for a connection session. |
| `connection_name` | Optional user-friendly connection name. |
| `local_device_id` | Reference to a device record. |
| `remote_device_id` | Reference to the connected device. |
| `status` | Connection state. |
| `connected_at` | Session start time. |
| `disconnected_at` | Session end time, if known. |
| `last_activity_at` | Most recent recorded activity. |

A connection record represents a session or relationship between endpoints, not necessarily an individual TCP packet or message.

### 12.3 `messages` table

Stores metadata for messages exchanged by the application.

| Column | Purpose |
|---|---|
| `id` | Database primary key. |
| `message_uuid` | Unique message identifier. |
| `connection_id` | Reference to the connection session. |
| `sender_device_id` | Reference to the sending device. |
| `message_type` | Application message type. |
| `created_at` | Message creation time. |
| `received_at` | Time the receiving application accepted the message. |
| `payload_size` | Payload size in bytes. |
| `delivery_status` | Application-level delivery state. |

An optional `content` column could store clipboard text, but doing so introduces privacy and retention considerations. The initial metadata design can omit that column.

### 12.4 Entity relationships

```text
devices
   |
   | 1
   |
   | N
connections
   |
   | 1
   |
   | N
messages
```

A device can participate in multiple connection sessions, and a connection session can contain multiple messages.

The sender of each message references a device record. A connection also references its participating devices.

### 12.5 SQLAlchemy engine and sessions

The database engine configures SQLAlchemy's database connectivity. A session factory creates sessions for units of database work.

The general flow is:

```text
Application
    |
    v
Repository
    |
    v
SQLAlchemy Session
    |
    v
SQLAlchemy Engine
    |
    v
SQLite Database File
```

`database/engine.py` should configure connectivity and expose a session factory. `database/models.py` should define tables and relationships, while `database/repository.py` should perform database operations.

Keep transactions short, commit successful changes, roll back failed transactions, and close sessions reliably. Do not share a single SQLAlchemy session indiscriminately across concurrent client handlers.

## 13. Data Flow

Consider a laptop sending clipboard text to a connected client.

1. **Capture:** The application obtains the clipboard text.
2. **Construct:** The client builds a message with an ID, type, sender, and timestamp.
3. **Validate:** Pydantic checks the message structure.
4. **Serialize:** The message is converted to JSON and encoded as UTF-8.
5. **Frame:** The sender prepends the payload-length header.
6. **Transmit:** TCP carries the framed bytes to the server.
7. **Parse:** The server reads the header and the complete payload.
8. **Validate again:** The server validates the received message before processing it.
9. **Persist:** The application records relevant metadata in the database.
10. **Forward or acknowledge:** The server forwards the message or sends a response according to the protocol.
11. **Apply:** The destination client validates the message and updates its clipboard.
12. **Record status:** If implemented, the application records the outcome of processing.

The ordering of persistence, forwarding, and acknowledgement must be defined explicitly. For example, acknowledging a message before committing its database record can result in an acknowledged message whose metadata was not persisted.

## 14. Installation and Setup

### Prerequisites

- Python 3.11 or a compatible supported Python version.
- Git.
- A terminal such as Windows Terminal or PowerShell.
- Two reachable devices or processes for network testing.
- A compatible clipboard integration package if clipboard synchronization is enabled.

### Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd ClipSync
```

Replace `<YOUR_REPOSITORY_URL>` with the actual repository URL.

### Create a virtual environment

On Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation because of its execution policy, use an approved local development approach or activate the environment from a supported terminal.

On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

After creating `requirements.txt`, install the declared dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Typical direct dependencies for the initial design include:

```text
SQLAlchemy>=2.0,<3.0
pydantic>=2.0,<3.0
```

Add clipboard and other packages only when the corresponding features are implemented. Python's `socket`, `json`, `uuid`, `datetime`, and `logging` modules are part of the standard library and do not need to be installed separately.

For a reproducible project, test the selected versions and pin the dependencies in the project's dependency-management workflow.

## 15. Running the Project

The following commands are illustrative. They assume that the server and client entry points exist and provide executable startup logic.

Start the server in one terminal:

```bash
python -m server.main
```

Start the client in a second terminal:

```bash
python -m client.main
```

Before running the application, ensure that the client uses the correct server address and port, that the server is listening on the expected interface, and that network rules permit the connection.

For initial testing, both programs can run on the same computer using a loopback address. Testing across two devices requires a reachable network address.

### Basic verification checklist

- [ ] The server starts and begins listening.
- [ ] The client establishes a connection.
- [ ] A valid framed message is transmitted.
- [ ] The receiver reconstructs the complete message.
- [ ] Pydantic accepts a valid message.
- [ ] Invalid messages are rejected safely.
- [ ] Database records are created when persistence is enabled.
- [ ] Client disconnection does not crash the server.
- [ ] Clipboard updates work when clipboard integration is enabled.

## 16. Configuration

Configuration should be separated from application logic.

Potential settings include:

| Setting | Purpose |
|---|---|
| `CLIPSYNC_HOST` | Address on which the server listens or the client connects. |
| `CLIPSYNC_PORT` | TCP port used by the server. |
| `CLIPSYNC_DATABASE_URL` | SQLAlchemy database URL. |
| `CLIPSYNC_MAX_MESSAGE_BYTES` | Maximum accepted framed payload size. |
| `CLIPSYNC_LOG_LEVEL` | Logging verbosity. |

These are proposed environment-variable names; the application must implement their loading and validation.

For a local SQLite database, a SQLAlchemy URL may look like:

```text
sqlite:///./clipsync.db
```

The database file's location depends on the application's working directory and configuration. A deployment should use a deliberate, persistent path.

Do not commit actual credentials, private keys, access tokens, or sensitive configuration values to version control.

## 17. Security Considerations

Clipboard content can contain passwords, authentication codes, private messages, and other sensitive information. Security must therefore be treated as a core design requirement.

### Network exposure

A server bound to `127.0.0.1` accepts connections only through the local loopback interface. A server bound to a network interface may become reachable by other machines, depending on firewall and routing rules.

Restrict access to trusted interfaces and networks.

### Authentication and pairing

A successful TCP connection does not prove that the remote device is trusted.

A future pairing flow should establish device identity and verify that subsequent messages originate from an authorized peer. QR pairing is a user interface mechanism; it must be backed by a secure verification protocol.

### Encryption

Plain TCP does not encrypt application data. Anyone able to observe unprotected traffic on the network may be able to read clipboard messages.

Before sending sensitive content over untrusted networks, implement an appropriate authenticated encryption transport or a correctly designed cryptographic protocol. Do not invent a custom encryption scheme.

### Input validation

- Validate message schemas.
- Enforce maximum payload sizes.
- Reject unsupported protocol versions and message types.
- Treat all received fields as untrusted input.
- Handle malformed JSON without terminating the server.
- Validate device permissions before forwarding or applying messages.

### Database privacy

Avoid persisting clipboard content unless there is a clear requirement. Consider retention policies, access controls, and database-file permissions.

### Logging

Log operational metadata rather than clipboard text. Never log secrets or entire sensitive payloads merely to simplify debugging.

## 18. Error Handling and Reliability

A robust implementation should account for the following conditions:

| Failure | Expected behavior |
|---|---|
| Connection refused | Report the connection failure and retry only according to policy. |
| Client disconnects | Clean up its connection and associated resources. |
| Incomplete header | Treat the connection as interrupted. |
| Incomplete payload | Reject the incomplete message and clean up safely. |
| Invalid JSON | Reject the message without crashing the server. |
| Schema validation failure | Record a safe diagnostic and reject the message. |
| Oversized payload | Reject it before allocating excessive memory. |
| Database transaction failure | Roll back the failed transaction and report the error. |
| Duplicate message ID | Apply a defined deduplication policy. |
| Clipboard access failure | Report the failure and avoid falsely marking the operation successful. |

Automatic reconnection, message retries, deduplication, and persistent delivery guarantees require explicit application logic. TCP reliability alone does not implement these features.

## 19. Testing Strategy

Tests should verify individual components before testing the complete application.

### Unit tests

- Pydantic schema validation.
- UUID and timestamp validation.
- JSON serialization and deserialization.
- Length-header encoding and decoding.
- Incomplete payload handling.
- Maximum payload enforcement.
- Repository insert, query, update, and delete operations where applicable.

### Integration tests

- Client-server communication over loopback.
- Multiple messages over one connection.
- Multiple clients connecting to the server.
- Database persistence after successful processing.
- Client disconnection and resource cleanup.
- Handling malformed or oversized messages.

### End-to-end tests

- Copy text on one device.
- Verify that the application detects the change.
- Send the message to the destination.
- Verify that the destination clipboard is updated.
- Confirm that the same text does not circulate indefinitely between clients.

Use temporary database files for database tests to avoid corrupting or modifying real development data.

## 20. Development Roadmap

### Phase 1 — Networking foundation

- Implement the TCP server and client.
- Establish connections and exchange bytes.
- Handle disconnects and socket errors.
- Implement length-prefixed message framing.

### Phase 2 — Structured messages

- Define Pydantic schemas.
- Implement JSON serialization and parsing.
- Introduce message IDs, types, and timestamps.
- Add validation and payload-size limits.

### Phase 3 — Database integration

- Configure SQLite through SQLAlchemy.
- Define device, connection, and message models.
- Implement repository methods.
- Persist connection and message metadata.
- Add transaction handling and database tests.

### Phase 4 — Clipboard synchronization

- Integrate desktop clipboard access.
- Implement text capture and remote updates.
- Prevent duplicate propagation and synchronization loops.
- Verify end-to-end behavior.

### Phase 5 — Reliability and security

- Add structured logging and error handling.
- Define acknowledgement and delivery-status semantics.
- Implement reconnection and deduplication policies.
- Design secure device pairing and encrypted transport.

### Phase 6 — Cross-device expansion

- Develop an Android client using Kotlin.
- Integrate Android clipboard APIs.
- Explore QR-based pairing and local-network discovery.
- Evaluate whether TCP remains the appropriate transport or a higher-level protocol is justified.

## 21. Learning Outcomes

ClipSync is intended to demonstrate practical understanding of:

- Python network programming.
- TCP sockets and client-server communication.
- Application-level protocol design.
- Message framing over byte streams.
- JSON serialization and Pydantic validation.
- SQLAlchemy ORM, database sessions, and transactions.
- Relational database modeling and foreign-key relationships.
- UUIDs, UTC timestamps, and event metadata.
- Modular application architecture.
- Error handling, logging, and automated testing.
- Security and privacy considerations for cross-device communication.

The project also provides a foundation for learning concurrency, asynchronous networking, mobile integration, and secure device-to-device communication.

## 22. Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make a focused change.
4. Add or update relevant tests.
5. Verify that existing functionality continues to work.
6. Open a pull request with a description of the change.

Please avoid committing local database files, virtual environments, private configuration, or clipboard contents.

## 23. License

No license has been selected yet. Add a `LICENSE` file and update this section before distributing the project.

If the project is intended to be open source, choose a license that matches the intended permissions and obligations. Do not claim that the project uses a particular license until that license has actually been added.

---

**ClipSync — Simple clipboard transfer, modular engineering, and a foundation for secure cross-device synchronization.**