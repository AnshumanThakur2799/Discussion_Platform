# Discussions

| Field      | Type               | Description                            |
|------------|--------------------|----------------------------------------|
| text       | string             | Main text content of the discussion.    |
| image_url  | string (optional)  | URL of an optional image for the discussion. |
| owner      | string             | ID or username of the owner of the discussion. |
| comments   | array of strings   | List of comment IDs associated with this discussion. |
| views      | integer (optional) | Number of views the discussion has received. |
| hashTags   | array of strings   | List of hashtags associated with the discussion. |
| likes      | array of strings   | List of user IDs who liked the discussion. |

---

# Users

| Field       | Type               | Description                            |
|-------------|--------------------|----------------------------------------|
| name        | string (optional)  | Name of the user.                       |
| email       | string (optional)  | Email address of the user.              |
| mobile_no   | string (optional)  | Mobile number of the user.              |
| followers   | array of strings   | List of user IDs who follow this user.  |
| following   | array of strings   | List of user IDs whom this user follows. |
| deleted     | boolean (optional) | Flag indicating if the user is deleted or not. |

---

# Comments

| Field      | Type               | Description                            |
|------------|--------------------|----------------------------------------|
| text       | string             | Main text content of the comment.       |
| owner      | string (optional)  | ID or username of the owner of the comment. |
| replies    | array of Reply     | List of reply objects associated with this comment. |
| likes      | array of strings   | List of user IDs who liked the comment. |

---

## Reply

| Field      | Type               | Description                            |
|------------|--------------------|----------------------------------------|
| text       | string             | Main text content of the reply.         |
| owner      | string (optional)  | ID or username of the owner of the reply. |
| likes      | array of strings   | List of user IDs who liked the reply.   |

