<a name="top"></a>
# API Documentation v0.1.0



<h2>Notes</h2>
<ul>
<li>All API responses will have the same 3 top-level keys which are never omitted: <code>data</code>, <code>error</code>, <code>meta</code>.</li>
<li>Request/response properties are all in <code>snake_case</code> not <code>camelCase</code>.</li>
</ul>


# Table of contents

- [System](#System)
  - [Health Check](#Health-Check)

___


# System

## Health Check
[Back to top](#top)

<p>Authentication not required. This endpoint is used for healthcheck in <code>docker-compose.yml</code>. <p>Note that there is no <code>/api</code> prefix so that other middleware need not be loaded. In production, this endpoint should be blocked by Nginx or the load balancer so that it can only be called within the host machine, private network or office VPN, and not from the public Internet.</p></p>

```
GET /healthcheck
```

### Headers - `Header`

| Name    | Type      | Description                          |
|---------|-----------|--------------------------------------|
| Content-Type | `string` | <p>application/json</p> |

### Examples

Example usage:

```curl
curl --location --request GET "http://localhost:10000/healthcheck"
--header "Content-Type: application/json"
```

### Success response

#### Success response - `Success 200`

| Name     | Type       | Description                           |
|----------|------------|---------------------------------------|
| data | `object` | <p>All properties for success response put in here.</p> |
| data.message | `string` | <p>Short message.</p> |
| error | `null` | <p>This will be set to null for success response.</p> |
| meta | `object` | <p>Metadata such as status code and pagination.</p> |
| meta.status_code | `number` | <p>HTTP status code for success response.</p> |
| meta.request_id | `string` | <p>Unique ID computed for each request to group all audit records created for a request, e.g. for database access.</p> |
| meta.version | `string` | <p>Application version.</p> |

### Success response example

#### Success response example - `Success:`

```application/json
HTTP/1.1 200 OK
{
  "data": {
    "message": "OK",
    "timestamp": "2024-11-28T00:10:30Z"
  },
  "error": null,
  "meta": {
    "status_code": 200,
    "request_id": "1631679055974-89d413c2-6e44-440d-ab3c-9767a91a3f50",
    "version": "v0.10.0-develop-f94fda8-20211122T0156Z"
  }
}
```

### Error response

#### Error response - `Error`

| Name     | Type       | Description                           |
|----------|------------|---------------------------------------|
| data | `null` | <p>This will be set to null for error response.</p> |
| error | `object` | <p>All properties for error response put in here.</p> |
| error.message | `string` | <p>Error message.</p> |
| meta | `object` | <p>Metadata such as status code and pagination.</p> |
| meta.status_code | `number` | <p>HTTP status code for error response.</p> |
| meta.request_id | `string` | <p>Unique ID computed for each request to group all audit records created for a request, e.g. for database access.</p> |
| meta.version | `string` | <p>Application version.</p> |

### Error response example

#### Error response example - `Error (not allowed action on record):`

```application/json
HTTP/1.1 403 Forbidden
{
  "data": null,
  "error": {
    "message": "Forbidden from <action name> action on <resource name> resource."
  },
  "meta": {
    "status_code": 400,
    "request_id": "1631175138159-ac98f1c3-df0e-40b1-81f9-3c03bcdf6135",
    "version": "v0.10.0-develop-f94fda8-20211122T0156Z"
  }
}
```

